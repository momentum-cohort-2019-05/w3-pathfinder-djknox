from pathfinder import ElevationMap, ElevationMapPainter, GreedyAlgorithm

elevation_map = ElevationMap('elevation_small.txt')
elevation_map_painter = ElevationMapPainter(elevation_map)

def test_file_can_be_read_into_a_2d_list():
    # the first value in elevation_small is 4713
    # the last value in elevation_small is 3948
    assert(elevation_map.elevation_data[0][0] == 4713)
    assert(elevation_map.elevation_data[-1][-1] == 3948)


def test_max_elevation_can_be_found():
    # 5648 is the max elevation in elevation_small.txt
    assert(elevation_map_painter.find_max_elevation() == 5648)


def test_min_elevation_can_be_found():
    # 3139 is the max elevation in elevation_small.txt
    assert(elevation_map_painter.find_min_elevation() == 3139)


def test_alpha_value_can_be_calculated():
    # max elevation should be 255
    assert(elevation_map_painter.calculate_alpha_value(elevation_map_painter.max_elevation) == 255)
    # min elevation should be 0
    assert(elevation_map_painter.calculate_alpha_value(elevation_map_painter.min_elevation) == 0)


def test_next_pixel_can_be_found_with_greedy_algorithm():
    # 11 3  146
    # 43 8 54
    # 2  8  43
    # 48 10 112
    # 74 9  28
    two_d_list = [[11, 3, 146], [43, 8, 54], [2, 8, 43], [48, 10, 112], [74, 9, 28]]
    greedy_algorithm = GreedyAlgorithm(two_d_list)
    start_row = 2
    start_column = 0
    next_pixel_row, next_pixel_column = greedy_algorithm.greedy_walk_to_next_pixel(start_row, start_column)

    assert(next_pixel_row == 2)
    assert(next_pixel_column == start_column + 1)
    assert(two_d_list[next_pixel_row][next_pixel_column] == 8)