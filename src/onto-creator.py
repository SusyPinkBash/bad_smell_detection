import sys


def start(param):
    pass


if len(sys.argv) < 2:
    print("Please give as input the path of the python class file to create the ontology")
    sys.exit(1)


start(sys.argv[1])