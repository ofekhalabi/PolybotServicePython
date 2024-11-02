import random
from cgitb import reset
from pathlib import Path
from matplotlib.image import imread, imsave


def rgb2gray(rgb):
    r, g, b = rgb[:, :, 0], rgb[:, :, 1], rgb[:, :, 2]
    gray = 0.2989 * r + 0.5870 * g + 0.1140 * b
    return gray


class Img:

    def __init__(self, path):
        """
        Do not change the constructor implementation
        """
        self.path = Path(path)
        self.data = rgb2gray(imread(path)).tolist()

    def save_img(self):
        """
        Do not change the below implementation
        """
        new_path = self.path.with_name(self.path.stem + '_filtered' + self.path.suffix)
        imsave(new_path, self.data, cmap='gray')
        return new_path

    def blur(self, blur_level=16):

        height = len(self.data)
        width = len(self.data[0])
        filter_sum = blur_level ** 2

        result = []
        for i in range(height - blur_level + 1):
            row_result = []
            for j in range(width - blur_level + 1):
                sub_matrix = [row[j:j + blur_level] for row in self.data[i:i + blur_level]]
                average = sum(sum(sub_row) for sub_row in sub_matrix) // filter_sum
                row_result.append(average)
            result.append(row_result)

        self.data = result

    def contour(self):
        for i, row in enumerate(self.data):
            res = []
            for j in range(1, len(row)):
                res.append(abs(row[j-1] - row[j]))

            self.data[i] = res

    def rotate(self):
        # Create a new list for the rotated image
        rotated = []
        for i in range(len(self.data[0])):  # Iterate over columns
            new_row = []  # New row for the rotated image
            for j in range(len(self.data) - 1, -1, -1):  # Iterate over rows in reverse
                new_row.append(self.data[j][i])  # Append the pixel to the new row
            rotated.append(new_row)  # Add the new row to the rotated image
        self.data = rotated  # Update the data with the rotated image


    def salt_n_pepper(self):
        res = []
        for i in self.data :
            new_row = []
            for pixel in i:
                # Generate a random number between 0 and 1 for pixel
                random_number = random.random()
                if random_number < 0.2:
                    new_row.append(255)
                elif random_number > 0.8 :
                    new_row.append(0)
                else :
                    new_row.append(pixel)

            res.append(new_row)
        self.data = res

    def concat(self, other_img, direction='horizontal'):
        res = []
        direct_width = len(self.data[0])
        direct_height = len(self.data)
        other_img_width = len(other_img.data[0])
        other_img_height = (len(other_img.data))
        if direct_height == other_img_height and direct_width == other_img_width :
            if direction == 'vertical':
                res = self.data
                for row in other_img.data:
                    res.append(row)

            if direction == 'horizontal' :
                for i in range(len(self.data)):
                    res.append((self.data[i] + other_img.data[i]))

        else:
            raise RuntimeError("the dimensions are not compatible")
        self.data = res

    def segment(self):
        res = []
        for row in self.data:
            new_row = []
            for pixel in row:
                if pixel > 100:
                    new_row.append(255)
                else:
                    new_row.append(0)
            res.append(new_row)
        self.data = res

my_img = Img('/home/ofekh/PycharmProjects/PolybotServicePython/image.jpg')
another_img = Img('/home/ofekh/PycharmProjects/PolybotServicePython/image.jpg')
my_img.segment()
my_img.save_img()

