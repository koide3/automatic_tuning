# adaptive_tuning

## NDT odometry (toy example)

| Parameter            | Range      | Baseline | Tuned (fixed) |
| -------------------- |:----------:|:--------:|:-------------:|
| resolution           | 1.0 - 10.0 | 4.0      | 4.28          |
| keyframe_delta_trans | 0.0 - 10.0 | 4.0      | 6.08          |


## GICP odometry (KITTI)

| Parameter               | Range      | Baseline | Tuned (fixed) |
| ----------------------- |:----------:|:--------:|:-------------:|
| max_correspondence_dist | 1.0 - 10.0 | 4.0      | 4.19          |
| keyframe_delta_trans    | 1.0 - 30.0 | 4.0      | 3.71          |

## LeGO-LOAM
| Parameter                        | Range      | Baseline | Tuned (fixed) |
|----------------------------------|:----------:|:--------:|:-------------:|
| segment_theta                    | 10 - 60    | 60.0     | 48.56         |
| segment_valid_line_num           | 2 - 100    | 5        | 4             |
| segment_valid_point_num          | 2 - 100    | 3        | 4             |
| edge_threshold                   | 0.01 - 1.0 | 0.1      | 0.683         |
| surf_threshold                   | 0.01 - 1.0 | 0.1      | 0.889         |
| nearest_feature_search_distance  | 1 - 25     | 5        | 7.027         |

## SuMa
| Parameter                        | Range        | Baseline | Tuned (fixed) |
|----------------------------------|:------------:|:--------:|:-------------:|
| min_radius                       | 0.0 - 0.5    | 0.0      | 0.052         |
| max_radius                       | 0.5 - 3.0    | 1.0      | 0.951         |
| max_angle                        | 45.0 - 135.0 | 90.0     | 94.439        |
| map-max-distance                 | 0.1 - 0.5    | 0.2      | 0.253         |
| map-max-angle                    | 15.0 - 60.0  | 45.0     | 25.165        |
| sigma_angle                      | 0.25 - 3.0   | 1.0      | 1.613         |
| sigma_distance                   | 0.25 - 3.0   | 1.0      | 1.308         |

