from PIL import Image

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


def find_max_elevation(elevation_data):
    """
    Given a two-dimensional array, return the highest value in the array.
    """
    max_value = max(elevation_data[0])
    for row in elevation_data:
        for column in row:
            if column > max_value:
                max_value = column
    return max_value
    

def find_min_elevation(elevation_data):
    """
    Given a two-dimensional array, return the lowest value in the array.
    """
    min_value = min(elevation_data[0])
    for row in elevation_data:
        for column in row:
            if column < min_value:
                min_value = column
    return min_value


def calculate_alpha_value(min_elevation, max_elevation, elevation_value):
    """
    Given a minimum elevation value, a maximum elevation value, and a single elevation value, calculate and return the alpha value (opacity setting in RGBA).
    """
    return int(((elevation_value - min_elevation) / (max_elevation - min_elevation)) * 255)


def draw_elevation_map_grey_scale(elevation_data):
    """
    Given a 2d array of elevation data, draw an elevation map in greyscale and save as 'map.png'.        
    """
    print("Drawing an elevation map in greyscale...")

    image_width = len(elevation_data[0])
    image_height = len(elevation_data)
    min_elevation = find_min_elevation(elevation_data)
    max_elevation = find_max_elevation(elevation_data)

    image = Image.new('L', (image_width, image_height))
    for row in elevation_data:
        for column in row:
            row_index = elevation_data.index(row)
            column_index = elevation_data[row_index].index(column)
            alpha_value = calculate_alpha_value(min_elevation, max_elevation, column)
            image.putpixel((column_index, row_index), alpha_value)
    image.save('map.png')

    print("Done drawing!")


def draw_elevation_map_rgba(elevation_data):
    """
    Given a 2d array of elevation data, draw an elevation map in RGBA and save as 'map.png'.
    """
    print("Drawing elevation map in RGBA...")

    image_width = len(elevation_data[0])
    image_height = len(elevation_data)
    min_elevation = find_min_elevation(elevation_data)
    max_elevation = find_max_elevation(elevation_data)

    image = Image.new('RGBA', (image_width, image_height), (0, 0, 0, 0))
    for row in elevation_data:
        for column in row:
            row_index = elevation_data.index(row)
            column_index = elevation_data[row_index].index(column)
            alpha_value = calculate_alpha_value(min_elevation, max_elevation, column)
            image.putpixel((column_index, row_index), (255, 255, 255, alpha_value))
    image.save('map.png')

    print("Done drawing!")


if __name__ == "__main__":
    # Read the data from elevation_small.txt into an appropriate data structure to get the elevation data.
    with open('elevation_small.txt') as file:
        elevation_data = read_elevation_data_into_2d_list(file)

    # Using the Pillow library, create an elevation map from the data. Higher elevations should be brighter; lower elevations darker.
    draw_elevation_map_rgba(elevation_data)

    # TODO:
    # make map.png look like exactly like example in README (?)
    # add the ability to start from the left edge of the map on any row (y-position) and calculate and draw a path across the map, using the greedy algorithm