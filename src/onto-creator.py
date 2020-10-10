from sys import argv, exit
from ast import *
from owlready2 import *
from types import new_class


class Class:
    def __init__(self, name, super_classes, properties):
        self.name = name
        self.super_classes = super_classes
        self.properties = properties


def get_classes(python_file_name):
    return [Class(node.name, [node_base.id for node_base in node.bases], [elt.s for elt in node.body[0].value.elts])
            for node in walk(parse(open(python_file_name, "r").read())) if type(node) is ClassDef]


def start(python_file_name):
    ontology_file_name = "res/tree.owl"
    ontology_file = get_ontology("http://test.org/tree.owl")
    with ontology_file:
        for current_class in get_classes(python_file_name):
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


def test():
    onto = get_ontology("res/tree.owl").load()
    cd = onto["ClassDeclaration"]
    assert cd.name == "ClassDeclaration"
    assert len(cd.is_a) == 1
    assert cd.is_a[0].name == 'TypeDeclaration'
    print("Test 1: passed")


if len(argv) < 2:
    print("Please give as input the path of the python class file to create the ontology")
    exit(1)
if argv[1] == 'test':
    test()
else:
    start(argv[1])
