import unittest
from individ_creator import *


class IndividCreatorTests(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(IndividCreatorTests, self).__init__(*args, **kwargs)
        self.path_file_owl = "res/tree.owl"
        self.path_project = "res/android-chess/app/src/main/java/jwtc/chess/"

    def test_10(self):
        classes = get_classesAST(self.path_project)
        self.assertEqual(type(classes), type(dict()), "The Classes should be placed in a dictionary")
        self.assertEqual(len(classes), 10, "There are missing classes")

    def test_11(self):
        onto = get_ontology(self.path_file_owl).load()
        tree = jl.parse.parse("class A { int x, y; }")
        populate_ontology(onto, {node.name: node for _, node in tree if type(node) is jl.tree.ClassDeclaration})
        a = onto['ClassDeclaration'].instances()[0]
        self.assertEqual(a.body[0].is_a[0].name, "FieldDeclaration", "Should be a FieldDeclaration definition")
        self.assertEqual(a.body[0].jname[0], 'x', "jname should be equal to x")
        self.assertEqual(a.body[1].is_a[0].name, "FieldDeclaration", "Should be a FieldDeclaration definition")
        self.assertEqual(a.body[1].jname[0], 'y', "jname should be equal to y")

    def test_12(self):
        tree = javalang.parse.parse("class A { int x, y; public A() { } public int getX() { return x;} }")
        onto = populate_ontology(get_ontology(self.path_file_owl).load(),
                                 {node.name: node for _, node in tree if type(node) is jl.tree.ClassDeclaration})
        a = onto['ClassDeclaration'].instances()[1]
        self.assertEqual(a.body[0].is_a[0].name, "MethodDeclaration", "Should be a MethodDeclaration definition")
        self.assertEqual(a.body[0].jname[0], 'getX', "jname should be equal to getX")
        self.assertEqual(a.body[1].is_a[0].name, "FieldDeclaration", "Should be a FieldDeclaration definition")
        self.assertEqual(a.body[1].jname[0], 'x', "jname should be equal to x")
        self.assertEqual(a.body[2].is_a[0].name, "FieldDeclaration", "Should be a FieldDeclaration definition")
        self.assertEqual(a.body[2].jname[0], 'y', "jname should be equal to y")
        self.assertEqual(a.body[3].is_a[0].name, "ConstructorDeclaration", "Should be a MethodDeclaration definition")
        self.assertEqual(a.body[3].jname[0], 'A', "jname should be equal to A")






print("########")
unittest.main()
