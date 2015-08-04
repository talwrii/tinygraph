# tingraph

Python library and command line program to produce very small graphs
without any wasted pixel for things like labels and axes. Has
good xpm support

## Usage

### Command line
    python -m tinygraph 1 2 3 4 5 > graph.xpm
    python -m tinygraph 1 2 3 4 5 -o graph.bmp
    # Big pixels on quite a large graph
    python -m tinygraph 1 2 3 4 5 -o graph.bmp -p 3 -H 20

### Python
    import tinygraph
    image = tinygraph.tiny_graph(10, [1,2,3,4,5])
    image.save('graph.xpm')
    image.save('graph.bmp')