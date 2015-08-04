"Make very very small graphs"

import PIL.Image
import argparse
import xpm
import sys

def tiny_graph(
        height, values, foreground=(0, 0, 0),
        background=(255, 255, 255), point_size=1):
    "Produce a pil file containing a tiny graph of the values"
    canvas = TinyCanvas(len(values), height, point_size, background=background)
    canvas.tiny_line(values, colour=foreground)
    return canvas.image

class TinyCanvas(object):
    def __init__(self, num_points, height, point_size=1, background=(255, 255, 255)):
        self.point_size = point_size
        self.background = background
        self.height = height
        self.image = PIL.Image.new(
            "RGB",
            (num_points * self.point_size, height),
            color=background)

    def tiny_line(self, values, colour=(0, 0, 0)):
        "Add aline to the canvas"
        width, _height = self.image.size
        if width != len(values * self.point_size):
            raise Exception("Length must match number of values")
        M = max(values)
        m = min(values)

        for point_x, value in zip(
                range(0, width, self.point_size),
                values):
            scale_value = (value - m) * 1.0 / (M - m)
            point_y = self._scale_to_point_y(scale_value)
            self.colour_point(point_x, point_y, colour)

    def _scale_to_point_y(self, scale):
        effective_height = (self.height // self.point_size *
            self.point_size)
        point_y = int(scale * effective_height
            // self.point_size * self.point_size)
        if point_y == effective_height:
            point_y = self.height - self.point_size
        return point_y

    def colour_point(self, x0, y0, colour):
        for x_offset in range(self.point_size):
            for y_offset in range(self.point_size):
                self.image.putpixel(
                    (x0 + x_offset, y0 + y_offset),
                    colour)

    def save(self, path, fmt=None):
        self.image.save(path, format=fmt)

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
