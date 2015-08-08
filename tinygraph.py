"Make very very small graphs"

import argparse
import math
import sys

import PIL.Image
import xpm


def tiny_graph(
        height, values, foreground=(0, 0, 0),
        background=(255, 255, 255), point_size=1, border=2,
        area=False):
    "Produce a pil file containing a tiny graph of the values"
    canvas = TinyCanvas(len(values), height, point_size, background=background, border=border, area=area)
    canvas.tiny_line(values, colour=foreground)
    return canvas

class TinyCanvas(object):
    def __init__(self, num_points, height, point_size=1, background=(255, 255, 255), border=2, area=False):
        self.point_size = point_size
        self.background = background
        self.height = height
        self.border = border
        self.area = area
        self.image = PIL.Image.new(
            "RGB",
            (num_points * self.point_size + 2 * self.border, height),
            color=background)

    def tiny_line(self, values, colour=(0, 0, 0)):
        "Add aline to the canvas"
        width, _height = self.image.size
        if width != len(values) * self.point_size + 2 * self.border:
            raise Exception("Length must match number of values")
        M = max(values)
        m = min(values)

        pixels_high = int(self.height - 2 * self.border) // self.point_size
        transform = CombinedTransform(
            ScaleTransform(m, M),
            PixelateTransform(pixels_high),
            BlockTransform(self.point_size),
            BorderTransform(self.border),
            PixelGravityTransform(self.image.size[1]))

        for index, value in enumerate(values):
            point_x, point_y = transform.parameter_to_target(index, value)
            if self.area:
                self.colour_bar(point_x, point_y, colour)
            else:
                self.colour_point(point_x, point_y, colour)

    def colour_bar(self, point_x, point_y, colour):
        for x in range(point_x, point_x + self.point_size):
            for y in range(point_y, self.height - self.border):
                self.image.putpixel((x, y), colour)

    def _index_to_point_x(self, index):
        return index * self.point_size + self.border

        point_y = int(scale * effective_height
            // self.point_size * self.point_size)

        if point_y == effective_height:
            point_y = effective_height - self.point_size

        return point_y + self.border

    def colour_point(self, x0, y0, colour):
        for x_offset in range(self.point_size):
            for y_offset in range(self.point_size):
                self.image.putpixel(
                    (x0 + x_offset, y0 - y_offset),
                    colour)

    def save(self, path, fmt=None):
        self.image.save(path, format=fmt)

class Transform(object):
    def parameter_to_target(self, x, y):
        raise NotImplementedError()

class BorderTransform(object):
    def __init__(self, border_size):
        self.border_size = border_size

    def parameter_to_target(self, x, y):
        return x + self.border_size, y + self.border_size

class BlockTransform(object):
    def __init__(self, pixel_size):
        self.pixel_size = pixel_size

    def parameter_to_target(self, x, y):
        return x * self.pixel_size, y * self.pixel_size

class ScaleTransform(object):
    def __init__(self, ymin, ymax):
        self.ymin = ymin
        self.ymax = ymax

    def parameter_to_target(self, x, y):
        return x, (float(y) - self.ymin) / (self.ymax - self.ymin)

class PixelateTransform(object):
    def __init__(self, pixels_high):
        self.pixels_high = pixels_high

    def parameter_to_target(self, x, y):
        pixel_y = math.floor(y * self.pixels_high)
        if pixel_y == self.pixels_high:
            pixel_y = self.pixels_high - 1
        return x, int(pixel_y)

class CombinedTransform(object):
    def __init__(self, *transforms):
        self.transforms = transforms

    def parameter_to_target(self, x, y):
        result = x, y
        for transform in self.transforms:
            result = transform.parameter_to_target(*result)
        return result

class PixelGravityTransform(object):
    def __init__(self, height):
        self.height = height

    def parameter_to_target(self, x, y):
        result = x, self.height - y
        return result


if __name__ == '__main__':
    PARSER = argparse.ArgumentParser(description='''Draw a tiny graph. Supports XPM well because several tools seem to use this.''')
    PARSER.add_argument('values', type=float, nargs='+',
                       help='values')
    PARSER.add_argument('-o', '--output', type=str,
        help='where to save file')
    PARSER.add_argument('-p', '--point-size', type=int,
        help='how big rendered poitns should be', default=1)
    PARSER.add_argument('-H', '--height', type=int,
        help='height of image in pixels', default=10)
    PARSER.add_argument('-f', '--format', type=str,
        help='what format to save in', default=None)
    args = PARSER.parse_args()
    graph = tiny_graph(args.height, args.values, point_size=args.point_size)

    if args.output is None:
        if args.format is None:
            print xpm.pil_save(graph.image)
        elif args.format.lower() == 'xpm':
            graph.save(sys.stdout, args.format)
        else:
            graph.save(sys.stdout, args.format)
    elif args.format.lower() == 'xpm' or args.output.endswith('.xpm'):
        # Pil cannot write xpm at the moment
        with open(args.output, 'w') as f:
            f.write(xpm.pil_save(graph.image))
    else:
        graph.save(args.output, args.format)
