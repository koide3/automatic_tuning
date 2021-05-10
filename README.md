# automatic_tuning

This repository provides a hyper parameter tuning framework for LiDAR odometry algorithms. It automatically repeats a trial and error loop while sampling different parameter sets using SMBO powered by *[Optuna](https://github.com/optuna/optuna)*. The evaluation environment is encapsulated as a docker environment that enables us to run multiple evaluation trials in parallel to accelerate the optimization process.

# Example usage

## 1. Build LeGO-LOAM docker image

```bash
cd automatic_tuning/scripts
./build_docker.sh
```

## 2. LeGO-LOAM docker image test (this step can be skipped)
```bash
cd automatic_tuning/scripts
./run_docker.sh

pwd
# /automatic_tuning/scripts

ls
# csv2tum.py  loam_config_base.yaml  log  optimize.py  optuna_lego.db  run.sh

ls /root/catkin_ws/src
# CMakeLists.txt  LeGO-LOAM-BOR
```

## 3. Optimization

We assume that you have KITTI 00 rosbag placed at ```~/datasets/kitti/bags/00.bag``` (that can be produced with [kitti2bag](https://github.com/SMRT-AIST/kitti2bag)) and [KITTI ground truth data in TUM format](data/poses.tar.gz) at ```~/datasets/kitti/poses/00_tum.txt```. Here, we minimize 100m RTE of LeGO-LOAM on KITTI 00 sequence by running the collowing command as an example.

```bash
cd automatic_tuning/scripts
./run_docker.sh python3 optimize_kitti.py
```

To speed up the optimization process, the above command can be run in parallel on several terminals. docker allows us to run multiple trial instances in completely separated environments, and Optuna takes care of synchronization of trials.

You can monitor the optimization progress with:

```bash
cd automatic_tuning/scripts
watch -n 10 tail -n 15 lego/log/log_00.log

# A new study created in RDB with name: lego
# [1604306020.385885239] Start trial 0
# Trial 0 finished with value: 3.635361 and parameters: {...}. Best is trial 0 with value: 3.635361.
# [1604306112.639330387] Start trial 2
# Trial 2 finished with value: 2.224538 and parameters: {...}. Best is trial 1 with value: 1.991202.
# [1604306207.153521061] Start trial 4
# ...
```

All the estimated trajectories and configuration files will be saved at ```scripts/lego/results``` as zip files.

After the parameter optimization, the RTE (100m) decreased from ```2.245886``` to ```1.934585```.

# Papers
- Automatic Hyper-Parameter Tuning for Black-box LiDAR Odometry, Kenji Koide, Masashi Yokozuka, Shuji Oishi, Atsuhiko Banno, ICRA2021
- Adaptive Hyper-Parameter Tuning for Black-box LiDAR Odometry, Kenji Koide, Masashi Yokozuka, Shuji Oishi, Atsuhiko Banno, IROS2021 (under review)
