from PIL import Image

# import random module for flipping a coin in the case of ties in the greedy algorithm
import random


class ElevationMap:
    """
    ElevationMap is a class for representing elevation data from a text file.
    """
    def __init__(self, elevation_data_filename):
        self.elevation_data = self.read_elevation_data_into_2d_list(elevation_data_filename)


    def read_elevation_data_into_2d_list(self, filename):
        """
        Given a file, read each row in the data and split into a list of integers.
        Append each list to another list to create a 2d list to return.
        """
        with open(filename) as file:
            elevation_data = []
            for row in file:
                elevations = row.split()
                elevations = [int(elevation_as_string) for elevation_as_string in elevations]
                elevation_data.append(elevations)

        return elevation_data


class ElevationMapPainter:
    """
    ElevationMapPainter is a class for taking an ElevationMap object and drawing an elevation map based on its data.
    """
    def __init__(self, elevation_map):
        self.elevation_data = elevation_map.elevation_data
        self.min_elevation = self.find_min_elevation()
        self.max_elevation = self.find_max_elevation()
        self.image_width = len(self.elevation_data[0])
        self.image_height = len(self.elevation_data)


    def find_max_elevation(self):
        """
        Given a two-dimensional array, return the highest value in the array.
        """
        max_value = max(self.elevation_data[0])
        for row in self.elevation_data:
            for column in row:
                if column > max_value:
                    max_value = column
        return max_value
    

    def find_min_elevation(self):
        """
        Given a two-dimensional array, return the lowest value in the array.
        """
        min_value = min(self.elevation_data[0])
        for row in self.elevation_data:
            for column in row:
                if column < min_value:
                    min_value = column
        return min_value


    def calculate_color_value(self, elevation_value):
        """
        Given an elevation value, calculate and return the color setting (between 0 and 255).
        """
        return int(((elevation_value - self.min_elevation) / (self.max_elevation - self.min_elevation)) * 255)


    def draw_elevation_map(self, filename_to_save_as='map.png'):
        """
        Given a 2d list of elevation data, draw an elevation map and save as the given filename.
        """
        print("Drawing elevation map...")

        image = Image.new('RGBA', (self.image_width, self.image_height), (0, 0, 0, 255))
        for row in range(self.image_width):
            for column in range(self.image_height):
                color_value = self.calculate_color_value(self.elevation_data[row][column])
                image.putpixel((column, row), (color_value, color_value, color_value, 255))
        image.save(filename_to_save_as)

        print("Done drawing elevation map!")
        return image


    def draw_path_of_least_resistance(self, image, pixel_row, pixel_column, filename_to_save_as='map.png'):
        """
        Given an image and a starting pixel row and column, draw a path on the image using the greedy algorithm.
        """
        print(f"Drawing path of least resistance on map, starting at pixel coordinate: ({pixel_row}, {pixel_column})...")
        
        greedy_algorithm = GreedyAlgorithm(self.elevation_data)
        for pixel in range(self.image_width - 1):
            pixel_row, pixel_column = greedy_algorithm.greedy_walk_to_next_pixel(pixel_row, pixel_column)
            image.putpixel((pixel_column, pixel_row), (0, 0, 255, 255))
        image.save(filename_to_save_as)

        print("Done drawing path of least resistance on map!")
        return image


class GreedyAlgorithm:
    """
    GreedyAlgorithm is a class for implementing an algorithm that steps through a 2d list based on least differences between element values.
    """
    def __init__(self, elevation_data):
        self.elevation_data = elevation_data

    def greedy_walk_to_next_pixel(self, start_row, start_column):
        """
        Given a start row and a start column, return the next row and next column in the list for the element that has the least difference in elevation.
        """
        current_pixel = self.elevation_data[start_row][start_column]
        next_pixel_column = start_column + 1
        forward_pixel = self.elevation_data[start_row][next_pixel_column]
        forward_top_pixel = self.elevation_data[start_row - 1][next_pixel_column]
        forward_bottom_pixel = self.elevation_data[start_row + 1][next_pixel_column]
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


if __name__ == "__main__":
    # create new ElevationMap object with the elevation data file
    elevation_map = ElevationMap('elevation_small.txt')

    # create new ElevationMapPainer object with the ElevationMap object
    elevation_map_painter = ElevationMapPainter(elevation_map)

    # Using the Pillow library, create an elevation map from the data. Higher elevations should be brighter; lower elevations darker.
    image = elevation_map_painter.draw_elevation_map()

    # given an image and a starting point, loop through all the columns with greedy_walk_to_next_pixel until get to the end
    # start at the middle pixel on the east side of the map
    pixel_row = len(elevation_map.elevation_data[0]) // 2
    pixel_column = 0
    image = elevation_map_painter.draw_path_of_least_resistance(image, pixel_row, pixel_column)


    # TODO:
    # make map.png look like exactly like example in README (?)