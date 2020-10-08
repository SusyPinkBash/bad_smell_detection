from sys import argv, exit
from ast import *
from owlready2 import *
from types import new_class


class Class:
    def __init__(self, name, super_classes, properties):
        self.name = name
        self.super_classes = super_classes
        self.properties = properties


def start(python_file_name):
    ontology_file_name = "../res/tree.owl"
    ontology_file = get_ontology("http://test.org/tree.owl")
    classes = [Class(node.name, [node_base.id for node_base in node.bases], [elt.s for elt in node.body[0].value.elts])
               for node in walk(parse(open(python_file_name, "r").read())) if type(node) is ClassDef]
    with ontology_file:
        for current_class in classes:
            if len(current_class.super_classes) == 1:
                if current_class.super_classes[0] == "Node":
                    new_class(current_class.name, (Thing,))
                else:
                    new_class(current_class.name, (ontology_file[current_class.super_classes[0]],))
            else:
                new_class(current_class.name, (ontology_file[current_class.super_classes[0]],
                                               ontology_file[current_class.super_classes[1]],))

            for class_property in current_class.properties:
                if class_property == "body" or class_property == "parameters":
                    new_class(class_property, (ObjectProperty,))
                else:
                    new_class("jname" if class_property == "name" else class_property, (DataProperty,))

    ontology_file.save(file=ontology_file_name, format="rdfxml")


if len(argv) < 2:
    print("Please give as input the path of the python class file to create the ontology")
    exit(1)
start(argv[1])
