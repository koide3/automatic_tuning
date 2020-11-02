# List of Tuned Parameters

## LeGO-LOAM
| Parameter                        | Range      | Baseline | Optimized |
|----------------------------------|:----------:|:--------:|:---------:|
| segment_theta                    | 10 - 60    | 60.0     | 48.56     |
| segment_valid_line_num           | 2 - 100    | 5        | 4         |
| segment_valid_point_num          | 2 - 100    | 3        | 4         |
| edge_threshold                   | 0.01 - 1.0 | 0.1      | 0.683     |
| surf_threshold                   | 0.01 - 1.0 | 0.1      | 0.889     |
| nearest_feature_search_distance  | 1 - 25     | 5        | 7.027     |

## hdl_graph_slam
| Parameter                        | Range       | Baseline | Optimized |
|----------------------------------|:-----------:|:--------:|:---------:|
| keyframe_delta_trans             | 0.0 - 30.0  | 1.0      | 8.485     |
| keyframe_delta_angle             | 0.0 - 30.0  | 1.0      | 0.323     |
| reg_max_correspondence_distance  | 0.25 - 10.0 | 2.0      | 2.950     |
| reg_correspondence_randomness    | 10 - 50     | 20       | 24        |

## SuMa
| Parameter                        | Range        | Baseline | Optimized |
|----------------------------------|:------------:|:--------:|:---------:|
| min_radius                       | 0.0 - 0.5    | 0.0      | 0.052     |
| max_radius                       | 0.5 - 3.0    | 1.0      | 0.951     |
| max_angle                        | 45.0 - 135.0 | 90.0     | 94.439    |
| map-max-distance                 | 0.1 - 0.5    | 0.2      | 0.253     |
| map-max-angle                    | 15.0 - 60.0  | 45.0     | 25.165    |
| sigma_angle                      | 0.25 - 3.0   | 1.0      | 1.613     |
| sigma_distance                   | 0.25 - 3.0   | 1.0      | 1.308     |
