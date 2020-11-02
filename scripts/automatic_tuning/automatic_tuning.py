#!/usr/bin/python3
import os
import shutil
import optuna
import logging

from abc import *

class AutomaticTuning(ABC):
	def __init__(self, study_name):
		self.study_name = study_name

		if not os.path.exists(study_name + '/log'):
			os.makedirs(study_name + '/log')

		self.log_id = 0
		while os.path.exists(study_name + '/log/log_%02d.log' % self.log_id):
			self.log_id += 1		

		logger = logging.getLogger()
		logger.setLevel(logging.INFO)
		logger.addHandler(logging.FileHandler(study_name + '/log/log_%02d.log' % self.log_id, mode='w'))
		optuna.logging.enable_propagation()

		self.study = optuna.create_study(study_name=study_name, storage='sqlite:///%s/optuna.db' % study_name, load_if_exists=True)

	def optimize(self, n_trials):
		def objective(trial):
			self.setup(trial)
			return self.run(trial)
		self.study.optimize(objective, n_trials)


	@abstractmethod
	def setup(self, trial):
		pass

	@abstractmethod
	def run(self, trial):
		pass


if __name__ == '__main__':
	class Test(AutomaticTuning):
		def setup(self, trial):
			self.x = trial.suggest_uniform('x', 0.0, 10.0)

		def run(self, trial):
			return (self.x - 4.0) ** 2

	test = Test('test')
	test.optimize(128)