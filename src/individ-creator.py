from sys import argv, exit
import javalang


def start(classes):
    print(classes)


if len(argv) < 2:
    print("Please give as input the path of the java class file to create the ontology")
    exit(1)
start(argv[1])
