#!/usr/bin/python3
import csv
import sys
import numpy
import argparse
import scipy.spatial


def csv2tum(src_filename, dst_filename, convert_cam2lidar):
	data = list(csv.reader(open(src_filename, 'r'), delimiter=','))[1:]
	data = numpy.array([x for x in data if len(x) == len(data[0])])

	stamps = numpy.float64(data[:, 2]) / 1e9
	pos = numpy.float64(data[:, 5:8])
	quat = numpy.float64(data[:, 8:12])

	lidar2cam = numpy.identity(4)
	lidar2cam[:3, :3] = scipy.spatial.transform.Rotation.from_quat([-0.500, -0.500, -0.500, 0.500]).as_matrix()
	cam2lidar = numpy.linalg.inv(lidar2cam)

	for i in range(len(pos)):
		mat = numpy.identity(4)
		mat[:3, 3] = pos[i]
		mat[:3, :3] = scipy.spatial.transform.Rotation.from_quat(quat[i]).as_matrix()

		if convert_cam2lidar:
			mat = cam2lidar.dot(mat).dot(lidar2cam)

		pos[i] = mat[:3, 3]
		quat[i] = scipy.spatial.transform.Rotation.from_matrix(mat[:3, :3]).as_quat()

	with open(dst_filename, 'w') as f:
		for s, p, q in zip(stamps, pos, quat):
			tup = (s,) + tuple(p) + tuple(q)
			print(('%.9f' + ' %.6f' * 7) % tup, file=f)


if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='A script to convert CSV odometry data (rostopic echo -p) into TUM format')
	parser.add_argument('src_csv_filename')
	parser.add_argument('dst_tum_filename')
	parser.add_argument('-c', '--cam2lidar', action='store_true')
	args = parser.parse_args()

	csv2tum(args.src_csv_filename, args.dst_tum_filename, args.cam2lidar)
