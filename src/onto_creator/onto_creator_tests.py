import unittest
from onto_creator import *


class OntoCreatorTests(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(OntoCreatorTests, self).__init__(*args, **kwargs)
        self.path_file_python = "res/tree.py"
        self.path_file_owl = "res/tree.owl"

    def test_00(self):
        classes = get_classes(self.path_file_python)
        self.assertEqual(type(classes), type(list()), "Classes should be placed in an array")
        self.assertEqual(len(classes), 77, "There are missing classes")

    def test_01(self):
        onto = get_ontology(self.path_file_owl).load()
        cd = onto["ClassDeclaration"]
        self.assertEqual(cd.name, "ClassDeclaration", "Should be a ClassDeclaration definition")
        self.assertEqual(len(cd.is_a), 1, "The length of ClassDeclaration should be 1")
        self.assertEqual(cd.is_a[0].name, "TypeDeclaration", "Should be a TypeDeclaration")

    def test_02(self):
        onto = get_ontology(self.path_file_owl).load()
        cd = onto["TypeDeclaration"]
        self.assertEqual(cd.name, "TypeDeclaration", "Should be a TypeDeclaration definition")
        self.assertEqual(len(cd.is_a), 2, "The length of TypeDeclaration should be 2")
        self.assertEqual(cd.is_a[0].name, "Declaration", "Should be a Declaration")
        self.assertEqual(cd.is_a[1].name, "Documented", "Should be a Documented")

    def test_03(self):
        onto = get_ontology(self.path_file_owl).load()
        cd = onto["jname"]
        self.assertEqual(cd.name, "jname", "Should be a TypeDeclaration definition")
        self.assertEqual(cd.is_a, [owl.DatatypeProperty], "Should be an DatatypeProperty")

    def test_04(self):
        onto = get_ontology(self.path_file_owl).load()
        cd = onto["body"]
        self.assertEqual(cd.name, "body", "Should be a TypeDeclaration definition")
        self.assertEqual(cd.is_a, [owl.ObjectProperty], "Should be an ObjectProperty")


unittest.main()
