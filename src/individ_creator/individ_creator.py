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
    class_declarations = {}
    for file in os.listdir(project_path):
        if file.endswith(".java"):
            java_file = open(project_path + '/' + file, "r")
            for _, node in jl.parse.parse(java_file.read()):
                if type(node) is jl.tree.ClassDeclaration:
                    class_declarations[node.name] = node
            java_file.close()
    return class_declarations


def populate_ontology(ontology, class_declarations):
    with ontology:
        for class_name, classAST in class_declarations.items():
            class_declaration = ontology["ClassDeclaration"]()
            class_declaration.jname = [class_name]

            for method in classAST.methods:
                if type(method) is javalang.tree.MethodDeclaration:
                    method_declaration = ontology["MethodDeclaration"]()
                    method_declaration.jname = [method.name]
                    class_declaration.body.append(method_declaration)

            for field in classAST.fields:
                if type(field) is javalang.tree.FieldDeclaration:
                    for decl in field.declarators:
                        field_declaration = ontology["FieldDeclaration"]()
                        field_declaration.jname = [decl.name]
                        class_declaration.body.append(field_declaration)

            for constructor in classAST.constructors:
                if type(constructor) is javalang.tree.ConstructorDeclaration:
                    constructor_declaration = ontology["ConstructorDeclaration"]()
                    constructor_declaration.jname = [constructor.name]
                    class_declaration.body.append(constructor_declaration)
    return ontology


if __name__ == "__main__":
    if len(argv) < 2:
        print("Please give as input the path of the java class files to create the ontology")
        exit(1)
    start(argv[1])
