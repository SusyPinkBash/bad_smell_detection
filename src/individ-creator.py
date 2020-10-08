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
    with ontology:
        for class_name, classAST in class_declarations.items():
            class_declaration = ontology["ClassDeclaration"]()
            class_declaration.jname = [class_name]

            # print("\n##### METHODS #####")
            for method in classAST.methods:
                method_declaration = ontology["MethodDeclaration"]()
                method_declaration.jname.append(method.name)
                class_declaration.body.append(method_declaration)

            # print("##### FIELDS #####")
            for field in classAST.fields:
                for decl in field.declarators:
                    field_declaration = ontology["FieldDeclaration"]()
                    field_declaration.jname.append(decl.name)
                    class_declaration.body.append(field_declaration)

            # print("##### CONSTRUCTORS #####")
            for constructor in classAST.constructors:
                constructor_declaration = ontology["ConstructorDeclaration"]()
                constructor_declaration.jname.append(constructor.name)
                class_declaration.body.append(constructor_declaration)

            # print(class_declaration.body)

    ontology.save(file="../res/tree2.owl", format="rdfxml")


if len(argv) < 2:
    print("Please give as input the path of the java class files to create the ontology")
    exit(1)
start(argv[1])
