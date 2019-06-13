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


if __name__ == "__main__":
    # Read the data from elevation_small.txt into an appropriate data structure to get the elevation data.
    with open('elevation_small.txt') as file:
        elevation_data = read_elevation_data_into_2d_list(file)

    # Using the Pillow library, create an elevation map from the data. Higher elevations should be brighter; lower elevations darker.
    image_width = len(elevation_data[0])
    image_height = len(elevation_data)
    min_elevation = find_min_elevation(elevation_data)
    max_elevation = find_max_elevation(elevation_data)

    # greyscale
    # image = Image.new('L', (image_width, image_height))
    # for row in elevation_data:
    #     for column in row:
    #         row_index = elevation_data.index(row)
    #         column_index = elevation_data[row_index].index(column)
    #         alpha_value = calculate_alpha_value(min_elevation, max_elevation, column)
    #         image.putpixel((row_index, column_index), alpha_value)
    # image.save('map.png')

    image = Image.new('RGBA', (image_width, image_height), (0, 0, 0, 0))
    for row in elevation_data:
        for column in row:
            row_index = elevation_data.index(row)
            column_index = elevation_data[row_index].index(column)
            alpha_value = calculate_alpha_value(min_elevation, max_elevation, column)
            image.putpixel((row_index, column_index), (255, 255, 255, alpha_value))
    image.save('map.png')

    # TODO:
    # figure out the putpixel() part of the above loop(s) - specifically the second parameter (column)




