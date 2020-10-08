import os
from sys import argv, exit
import javalang as jl
import javalang.tree
from owlready2 import *


def start(project_path):
    # PARSING PROJECT FILES TO DICTIONARY {class_name : ClassDeclaration}
    # TODO: refactor with possibly comprehension and better structure
    class_declarations = {}
    for path, _, files in os.walk(project_path):
        if path is project_path:
            for file in [f for f in files if f.endswith(".java")]:
                full_path = path + "/" + file
                for _, node in jl.parse.parse(open(full_path, "r").read()):
                    if type(node) is jl.tree.ClassDeclaration:
                        class_declarations[node.name] = node
    print(class_declarations.keys())

    # ONTOLOGY
    ontology = get_ontology("../res/tree.owl").load()
    for class_name, declaration_node in class_declarations.items():
        ontology["ClassDeclaration"](class_name)
        # class_declaration = ontology["ClassDeclaration"]()
        # class_declaration.jname = [class_name]



    ontology.save(file="../res/tree2.owl", format="rdfxml")






if len(argv) < 2:
    print("Please give as input the path of the java class files to create the ontology")
    exit(1)
start(argv[1])
