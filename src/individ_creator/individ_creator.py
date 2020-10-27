from sys import argv, exit
import javalang as jl
import javalang.tree
from owlready2 import *


# class Class:
#     def __init__(self, name, classAST):
#         self.name = name
#         self.classAST = classAST

def start(project_path):
    ontology = populate_ontology(get_ontology("res/tree.owl").load(), get_classesAST(project_path))
    ontology.save(file="res/tree2.owl", format="rdfxml")


def get_classesAST(project_path):
    # PARSING PROJECT FILES TO DICTIONARY {class_name : ClassDeclaration}
    # TODO: refactor with possibly comprehension and better structure
    # TODO : remove dictionary to avoid overriding DatabaseHelper
    class_declarations = {}
    for file in os.listdir(project_path):
        if file.endswith(".java"):
            java_file = open(project_path + '/' + file, "r")
            for _, node in jl.parse.parse(java_file.read()):
                if type(node) is jl.tree.ClassDeclaration:
                    print(node.name)
                    class_declarations[node.name] = node
            java_file.close()
    print()
    return class_declarations


def populate_ontology(ontology, class_declarations):
    with ontology:
        for class_name, classAST in class_declarations.items():
            print(class_name)
            class_declaration = ontology["ClassDeclaration"]()
            class_declaration.jname = [class_name]

            for method in classAST.methods:
                if type(method) is javalang.tree.MethodDeclaration:
                    declaration = add_new_declaration(method, "MethodDeclaration", class_declaration, ontology)
                    add_parameter_declaration(method, declaration, ontology)
                    add_statement_declaration(method, declaration, ontology)

            for field in classAST.fields:
                if type(field) is javalang.tree.FieldDeclaration:
                    for decl in field.declarators:
                        add_new_declaration(decl, "FieldDeclaration", class_declaration, ontology)

            for constructor in classAST.constructors:
                if type(constructor) is javalang.tree.ConstructorDeclaration:
                    declaration = add_new_declaration(constructor, "ConstructorDeclaration", class_declaration, ontology)
                    add_parameter_declaration(constructor, declaration, ontology)
                    add_statement_declaration(constructor, declaration, ontology)
    return ontology


def add_new_declaration(node, declaration_type, class_declaration, ontology):
    declaration = ontology[declaration_type]()
    declaration.jname = [node.name]
    class_declaration.body.append(declaration)
    return declaration


def add_parameter_declaration(node, declaration, ontology):
    for parameter in node.parameters:
        formal_declaration = ontology["FormalParameter"]()
        formal_declaration.jname = [parameter.name]
        declaration.parameters.append(formal_declaration)


def add_statement_declaration(node, declaration, ontology):
    if node.body is not None:
        for _, statement in node:
            statement_base = type(statement).__bases__[0]
            if statement_base is javalang.tree.Statement:
                statement_type = type(statement).__name__
                declaration.body.append(ontology[statement_type]())


statement_types = set()
if __name__ == "__main__":
    if len(argv) < 2:
        print("Please give as input the path of the java class files to create the ontology")
        exit(1)
    start(argv[1])
