#!/usr/bin/python

"""Use tinygraph to make an xpm graph; store it somewhere unique ;
return the dzen2 markup to open it"""

import argparse
import os
import xpm

import tinygraph

GRAPH_DIR = os.path.join(os.environ['HOME'], '.dzengraphs')

def main():
    if not os.path.isdir(GRAPH_DIR):
        os.mkdir(GRAPH_DIR)

    PARSER = argparse.ArgumentParser(description='Produces a graph for display with dzen2')
    PARSER.add_argument('name', type=str, help='unique identifier for graph')
    PARSER.add_argument('points', type=float, nargs='+',
                    help='')
    PARSER.add_argument('--area', '-A', action='store_true', default=False,
                    help='Fill in the area under the graph')
    args = PARSER.parse_args()

    graph = tinygraph.tiny_graph(20, args.points, point_size=4, area=args.area)
    filename = os.path.join(GRAPH_DIR, args.name + '.xpm')
    with open(filename, 'w') as f:
        f.write(xpm.pil_save(graph.image))

    print "^i({})".format(filename)

if __name__ == '__main__':
	main()
