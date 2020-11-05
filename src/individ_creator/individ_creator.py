from collections import defaultdict
from sys import argv, exit
import javalang as jl
import javalang.tree
from owlready2 import *


def start(project_path):
    ontology = populate_ontology(get_ontology("res/tree.owl").load(), get_classesAST(project_path))
    ontology.save(file="res/tree2.owl", format="rdfxml")


def get_classesAST(project_path):
    class_declarations = defaultdict()
    for file in os.listdir(project_path):
        if file.endswith(".java"):
            java_file = open(project_path + '/' + file, "r")
            for _, node in jl.parse.parse(java_file.read()):
                if type(node) is jl.tree.ClassDeclaration:
                    class_declarations.setdefault(node.name, []).append(node)
            java_file.close()
    return class_declarations


def populate_ontology(ontology, class_declarations):
    with ontology:
        for class_name, classesAST in class_declarations.items():
            for classAST in classesAST:
                class_declaration = ontology["ClassDeclaration"]()
                class_declaration.jname = [class_name]

                for method in classAST.methods:
                    if type(method) is javalang.tree.MethodDeclaration:
                        declaration = add_new_declaration(method, "Method", class_declaration, ontology)
                        add_other_declarations(method, declaration, ontology)

                for field in classAST.fields:
                    if type(field) is javalang.tree.FieldDeclaration:
                        for decl in field.declarators:
                            add_new_declaration(decl, "Field", class_declaration, ontology)

                for constructor in classAST.constructors:
                    if type(constructor) is javalang.tree.ConstructorDeclaration:
                        declaration = add_new_declaration(constructor, "Constructor", class_declaration, ontology)
                        add_other_declarations(constructor, declaration, ontology)
    return ontology


def add_new_declaration(node, declaration_type, class_declaration, ontology):
    declaration = ontology[declaration_type + "Declaration"]()
    declaration.jname = [node.name]
    class_declaration.body.append(declaration)
    return declaration


def add_other_declarations(node, declaration, ontology):
    for parameter in node.parameters:
        formal_declaration = ontology["FormalParameter"]()
        formal_declaration.jname = [parameter.name]
        declaration.parameters.append(formal_declaration)

    if node.body is not None:
        for _, statement in node:
            if type(statement).__bases__[0] is javalang.tree.Statement:
                declaration.body.append(ontology[type(statement).__name__]())


if __name__ == "__main__":
    if len(argv) < 2:
        print("Please give as input the path of the java class files to create the ontology")
        exit(1)
    start(argv[1])
