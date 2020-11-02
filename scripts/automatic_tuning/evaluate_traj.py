#!/usr/bin/python3
import re
import subprocess


def get_traj_info(filename):
	p = subprocess.Popen(['evo_traj', 'tum', filename], shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	p.wait()
	stdout, stderr = p.communicate()

	if len(stderr):
		print(stderr.decode('utf-8'))

	result = stdout.decode('utf-8')

	found = re.findall(r'([0-9]+)\sposes', result)
	num_poses = int(found[0])

	found = re.findall(r'([0-9]+(\.[0-9]+)?)m\spath\slength', result)
	length = float(found[0][0])

	found = re.findall(r'([0-9]+(\.[0-9]+)?)s\sduration', result)
	duration = float(found[0][0])

	return {'poses': num_poses, 'length': length, 'duration': duration}


def run_evo(commands):
	p = subprocess.Popen(commands, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	p.wait()
	stdout, stderr = p.communicate()

	if len(stderr):
		print(stderr.decode('utf-8'))

	result = stdout.decode('utf-8')
	results = {}
	for item in re.findall(r'([a-z]+)\s+([0-9]+\.[0-9]+)', result):
		results[item[0]] = float(item[1])

	return results


def eval_ape(gt_filename, traj_filename, t_offset=0.0):
	ret = run_evo(['evo_ape', 'tum', gt_filename, traj_filename, '-a', '--t_offset', str(t_offset)])
	return ret


def eval_rpe(gt_filename, traj_filename, delta_unit='m', delta=100, all_pairs=True, t_offset=0.0):
	commands = ['evo_rpe', 'tum', gt_filename, traj_filename, '-a', '--delta_unit', str(delta_unit), '--delta', str(delta), '--t_offset', str(t_offset)]
	if all_pairs:
		commands += ['--all_pairs']

	ret = run_evo(commands)
	return ret


if __name__ == '__main__':
	gt_filename = '/datasets/kitti/poses/00_tum.txt'
	traj_filename = '/home/koide/workspace/lo_optuna2/eval_lego/eval/lego_aug_no1/00.txt'

	print(get_traj_info(gt_filename))
	print(eval_ape(gt_filename, traj_filename, t_offset=-1000))
	print(eval_rpe(gt_filename, traj_filename, t_offset=-1000))
