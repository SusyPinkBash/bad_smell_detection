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
            for _, node in jl.parse.parse(open(project_path + '/' + file, "r").read()):
                if type(node) is jl.tree.ClassDeclaration:
                    class_declarations[node.name] = node
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


def test():
    onto = get_ontology("res/tree.owl").load()
    tree = jl.parse.parse("class A { int x, y; }")
    populate_ontology(onto, {node.name: node for _, node in tree if type(node) is jl.tree.ClassDeclaration})
    a = onto['ClassDeclaration'].instances()[0]
    assert a.body[0].is_a[0].name == 'FieldDeclaration'
    assert a.body[0].jname[0] == 'x'
    assert a.body[1].is_a[0].name == 'FieldDeclaration'
    assert a.body[1].jname[0] == 'y'
    print("Test 2: passed")


if len(argv) < 2:
    print("Please give as input the path of the java class files to create the ontology")
    exit(1)
if argv[1] == 'test':
    test()
else:
    start(argv[1])
