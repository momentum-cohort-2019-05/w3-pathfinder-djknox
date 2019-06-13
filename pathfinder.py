def read_elevation_data_into_2d_list(file):
    """
    Given a file, read each row in the data and split into a list of integers.
    Append each list to another list to create a 2d list to return.
    """
    elevation_data = []
    for row in file:
        elevations = row.split()
        elevations = [int(elevation_as_string) for elevation_as_string in elevations]
        elevation_data.append(elevations)

    return elevation_data


if __name__ == "__main__":
    # open elevation_small.txt and read into 2d list
    with open('elevation_small.txt') as file:
        elevation_data = read_elevation_data_into_2d_list(file)

    print(elevation_data[0])