import pathfinder

file = open('elevation_small.txt')

def test_file_can_be_read_into_a_2d_list():
    elevation_data = pathfinder.read_elevation_data_into_2d_list(file)
    assert(elevation_data[0][0] == 4713)
    assert(elevation_data[-1][-1] == 3948)