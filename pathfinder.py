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
        
        path_finder = PathFinder(self.elevation_data)
        for pixel in range(self.image_width - 1):
            pixel_row, pixel_column = path_finder.greedy_walk_to_next_pixel(pixel_row, pixel_column)
            image.putpixel((pixel_column, pixel_row), (0, 0, 255, 255))
        image.save(filename_to_save_as)

        print("Done drawing path of least resistance on map!")
        return image


    def draw_all_paths_of_least_resistance(self, image, filename_to_save_as='map.png'):
        """
        Given an image, draw all paths starting on the left side on the image using the greedy algorithm.
        """
        print(f"Drawing all paths of least resistance on map...")
        pixel_column = 0
        for pixel_row in range(elevation_map_painter.image_height - 1):
            image = elevation_map_painter.draw_path_of_least_resistance(image, pixel_row, pixel_column)
        image.save(filename_to_save_as)

        print("Done drawing path of least resistance on map!")
        return image


class PathFinder:
    """
    PathFinder is a class that implements GreedyAlgorithm to step through a 2d list based on least differences between element values.
    """
    def __init__(self, elevation_data):
        self.elevation_data = elevation_data


    def greedy_walk_to_next_pixel(self, start_row, start_column):
        greedy_algorithm = GreedyAlgorithm(self.elevation_data, start_row, start_column)
        return greedy_algorithm.get_next_row_and_column()


class GreedyAlgorithm:
    """
    GreedyAlgorithm is a class for determining the least differences between element values.
    """
    def __init__(self, elevation_data, start_row, start_column):
        self.elevation_data = elevation_data
        self.start_row = start_row
        self.start_column = start_column
        self.next_column = self.start_column + 1


    def get_forward_top_row(self):
        return self.start_row - 1


    def get_forward_bottom_row(self):
        return self.start_row + 1


    def get_current_pixel_value(self):
        return self.elevation_data[self.start_row][self.start_column]


    def get_forward_pixel_value(self):
        return self.elevation_data[self.start_row][self.next_column]


    def get_forward_top_pixel_value(self):
        return self.elevation_data[self.get_forward_top_row()][self.next_column]

    
    def get_forward_bottom_pixel_value(self):
        return self.elevation_data[self.get_forward_bottom_row()][self.next_column]

    
    def get_difference_in_forward(self):
        return abs(self.get_current_pixel_value() - self.get_forward_pixel_value())


    def get_difference_in_forward_top(self):
        return abs(self.get_current_pixel_value() - self.get_forward_top_pixel_value())


    def get_difference_in_forward_bottom(self):
        return abs(self.get_current_pixel_value() - self.get_forward_bottom_pixel_value())


    def forward_has_the_least_difference(self):
        return self.get_difference_in_forward_top() > self.get_difference_in_forward() < self.get_difference_in_forward_bottom()


    def forward_has_tie_with_other_pixels(self):
        return self.get_difference_in_forward() == self.get_difference_in_forward_top() or self.get_difference_in_forward() == self.get_difference_in_forward_bottom()


    def forward_top_has_the_least_difference(self):
        return self.get_difference_in_forward() > self.get_difference_in_forward_top() < self.get_difference_in_forward_bottom()

    
    def forward_bottom_has_the_least_difference(self):
        return self.get_difference_in_forward_top() > self.get_difference_in_forward_bottom() < self.get_difference_in_forward()

    
    def forward_top_has_tie_with_forward_bottom(self):
        list_of_diffs = [self.get_forward_top_pixel_value(), self.get_forward_bottom_pixel_value()]
        coin_flip_result = random.randint(0, 1)
        chosen_pixel = list_of_diffs[coin_flip_result]

        if chosen_pixel is self.get_forward_top_pixel_value():
            return self.get_forward_top_row()

        elif chosen_pixel is self.get_forward_bottom_pixel_value():
            return self.get_forward_bottom_row()


    def get_next_row_and_column(self):
        """
        Return the next row and next column in the list for the element that has the least difference in elevation.
        """
        # TODO: if start_row is the first row, then don't consider the forward_top_pixel_value
        # TODO: if start_row is the last row, then don't consider the forward_bottom_pixel_value

        # if difference_in_forward has the least difference
        if self.forward_has_the_least_difference() or self.forward_has_tie_with_other_pixels():
            next_row = self.start_row
        
        # if difference_in_forward_top has the least difference
        elif self.forward_top_has_the_least_difference():
            next_row = self.get_forward_top_row()

        # if difference_in_forward_bottom has the least difference
        elif self.forward_bottom_has_the_least_difference():
            next_row = self.get_forward_bottom_row()

        # if difference_in_forward_top is tied with difference_in_forward_bottom
        elif self.get_difference_in_forward_top() == self.get_difference_in_forward_bottom():
            next_row = self.forward_top_has_tie_with_forward_bottom()

        return next_row, self.next_column


if __name__ == "__main__":
    # create new ElevationMap object with the elevation data file
    elevation_map = ElevationMap('elevation_small.txt')

    # create new ElevationMapPainer object with the ElevationMap object
    elevation_map_painter = ElevationMapPainter(elevation_map)

    # Using the Pillow library, create an elevation map from the data
    image = elevation_map_painter.draw_elevation_map()

    # given an image and a starting point, draw the path of least resistance
    image = elevation_map_painter.draw_path_of_least_resistance(image, 300, 0)

    # Starting from each location on the left-hand side of the map, plot an optimal path across the map.
    # image = elevation_map_painter.draw_all_paths_of_least_resistance(image)

    # TODO:
    # refactor greedy walk algorithm to work with pixels that are outside of the image
    # get draw_all_paths_of_least_resistance() to properly draw all paths