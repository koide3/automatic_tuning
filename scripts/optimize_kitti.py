#!/usr/bin/python3
import os
import yaml
import time
import shutil
import optuna
import logging
import subprocess
from automatic_tuning import csv2tum
from automatic_tuning import evaluate_traj
from automatic_tuning import AutomaticTuning


class TuningKITTI(AutomaticTuning):
	def __init__(self, study_name):
		super().__init__(study_name)

		with open('loam_config_base.yaml', 'r') as f:
			self.config = yaml.load(f)

	# sample hyper-parameters from ```trial```
	def setup(self, trial):
		segment_theta = trial.suggest_uniform('segment_theta', 10, 60)
		segment_valid_line_num = trial.suggest_int('segment_valid_line_num', 2, 100)
		segment_valid_point_num = trial.suggest_int('segment_valid_point_num', 2, 100)
		edge_threshold = trial.suggest_uniform('edge_threshold', 0.01, 1.0)
		surf_threshold = trial.suggest_uniform('surf_threshold', 0.01, 1.0)
		nearest_feature_search_distance = trial.suggest_uniform('nearest_feature_search_distance', 1, 25)

		self.config['lego_loam']['imageProjection']['segment_theta'] = segment_theta
		self.config['lego_loam']['imageProjection']['segment_valid_line_num'] = segment_valid_line_num
		self.config['lego_loam']['imageProjection']['segment_valid_point_num'] = segment_valid_point_num
		self.config['lego_loam']['featureAssociation']['edge_threshold'] = edge_threshold
		self.config['lego_loam']['featureAssociation']['surf_threshold'] = surf_threshold
		self.config['lego_loam']['featureAssociation']['nearest_feature_search_distance'] = nearest_feature_search_distance

	# run LeGO-LOAM and evaluate trajectory error
	def run(self, trial):
		logger = logging.getLogger()
		logger.info('[%.9f] Start trial %d' % (time.time(), trial.number))

		os.makedirs('/tmp/results', exist_ok=True)

		conf_filename = '/tmp/results/loam_config.yaml'
		with open(conf_filename, 'w') as f:
			f.write(yaml.dump(self.config))

		seq_id = 0
		gt_filename = '/datasets/kitti/poses/%02d_tum.txt' % seq_id
		bag_filename = '/datasets/kitti/bags/%02d.bag' % seq_id
		traj_filename = '/tmp/results/traj_%02d.txt' % seq_id

		# run LeGO-LOAM
		self.run_lego(bag_filename, conf_filename, traj_filename)

		# chech the validity of the estimated trajectory
		gt_info = evaluate_traj.get_traj_info(gt_filename)
		traj_info = evaluate_traj.get_traj_info(traj_filename)
		if 'poses' not in traj_info or traj_info['poses'] < gt_info['poses'] * 0.9:
			logger.info('[%.9f] Too many frames dropped (gt:%d traj:%d)' % (time.time(), gt_info['poses'], traj_info['poses']))
			return 1e9

		# evaluate metric
		rpe = evaluate_traj.eval_rpe(gt_filename, traj_filename, delta_unit='m', delta=100, all_pairs=True, t_offset=-1000)

		# save estimated trajectories
		os.makedirs('%s/results' % self.study_name, exist_ok=True)
		subprocess.run(['zip', '-r', '%s/results/results_%05d.zip' % (self.study_name, trial.number), '/tmp/results'])

		return rpe['rmse']


	# run lego loam
	def run_lego(self, bag_filename, conf_filename, traj_filename):
		# run LeGO-LOAM
		# after finishing odometry estimation, there should be '/tmp/integrated_to_init.bag'
		subprocess.run(['roslaunch', 'lego_loam_bor', 'run_lego.launch', 'rosbag:=%s' % bag_filename, 'conf:=%s' % conf_filename])

		# convert bag -> csv -> TUM format
		with open('/tmp/integrated_to_init.csv', 'w') as f:
			subprocess.run(['rostopic', 'echo', '-b', '/tmp/integrated_to_init.bag', '-p', '/integrated_to_init'], stdout=f)
		csv2tum('/tmp/integrated_to_init.csv', traj_filename, convert_cam2lidar=True)


def main():
	tuning = TuningKITTI('lego')

	# you can feed "initial guess" for the first trial
	x0 = {
		'segment_theta': 60,
		'segment_valid_line_num': 5,
		'segment_valid_point_num': 3,
		'edge_threshold': 0.1,
		'surf_threshold': 0.1,
		'nearest_feature_search_distance': 5
	}
	if tuning.log_id == 0:
		tuning.study.enqueue_trial(x0)

	tuning.optimize(n_trials=128)


if __name__ == '__main__':
	main()
