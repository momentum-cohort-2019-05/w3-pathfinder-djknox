from PIL import Image

# import random module for flipping a coin in the case of ties in the greedy algorithm
import random

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
    Given a 2d list of elevation data, draw an elevation map in greyscale and save as 'map.png'.        
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

    print("Done drawing elevation map!")
    return image


def draw_elevation_map_rgba(elevation_data):
    """
    Given a 2d list of elevation data, draw an elevation map in RGBA and save as 'map.png'.
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

    print("Done drawing elevation map!")
    return image


def greedy_walk_to_next_pixel(elevation_data, start_row, start_column):
    """
    Given a 2d list, a start row, and a start column, return the next row and next column in the list for the element that has the least difference.
    """
    current_pixel = elevation_data[start_row][start_column]
    next_pixel_column = start_column + 1
    forward_pixel = elevation_data[start_row][next_pixel_column]
    forward_top_pixel = elevation_data[start_row - 1][next_pixel_column]
    forward_bottom_pixel = elevation_data[start_row + 1][next_pixel_column]
    difference_in_forward = abs(current_pixel - forward_pixel)
    difference_in_forward_top = abs(current_pixel - forward_top_pixel)
    difference_in_forward_bottom = abs(current_pixel - forward_bottom_pixel)

    # if difference_in_forward has the least difference
    if difference_in_forward_top > difference_in_forward < difference_in_forward_bottom:
        next_pixel_row = start_row

    # if difference_in_forward is tied with any other pixels
    if difference_in_forward == difference_in_forward_top or difference_in_forward == difference_in_forward_bottom:
        next_pixel_row = start_row
    
    # if difference_in_forward_top has the least difference
    if difference_in_forward > difference_in_forward_top < difference_in_forward_bottom:
        next_pixel_row = start_row - 1

    # if difference_in_forward_bottom has the least difference
    if difference_in_forward_top > difference_in_forward_bottom < difference_in_forward:
        next_pixel_row = start_row + 1

    # if difference_in_forward_top is tied with difference_in_forward_bottom
    if difference_in_forward_top == difference_in_forward_bottom:
        list_of_diffs = [forward_top_pixel, forward_bottom_pixel]
        coin_flip_result = random.randint(0, 1)
        chosen_pixel = list_of_diffs[coin_flip_result]

        if chosen_pixel == forward_top_pixel:
            next_pixel_row = start_row - 1

        elif chosen_pixel == forward_bottom_pixel:
            next_pixel_row = start_row + 1

    return next_pixel_row, next_pixel_column


def draw_path_of_least_resistance(image, elevation_data, pixel_row, pixel_column):
    """
    Given an image, a 2d list of elevation data, and a starting pixel row and column, draw the path of least resistance on the image using the greedy algorithm.
    """
    print("Drawing path of least resistance on map...")
    for pixel in range(len(elevation_data[0]) - 1):
        pixel_row, pixel_column = greedy_walk_to_next_pixel(elevation_data, pixel_row, pixel_column)
        image.putpixel((pixel_column, pixel_row), (0, 0, 255, 255))
    image.save('map_path.png')

    print("Done drawing path of least resistance on map!")
    return image


if __name__ == "__main__":
    # Read the data from elevation_small.txt into an appropriate data structure to get the elevation data.
    with open('elevation_small.txt') as file:
        elevation_data = read_elevation_data_into_2d_list(file)

    # Using the Pillow library, create an elevation map from the data. Higher elevations should be brighter; lower elevations darker.
    image = draw_elevation_map_rgba(elevation_data)

    # given a starting point, loop through all the columns with greedy_walk_to_next_pixel until get to the end
    pixel_row = 300
    pixel_column = 0
    image = draw_path_of_least_resistance(image, elevation_data, pixel_row, pixel_column)


    # TODO:
    # make map.png look like exactly like example in README (?)