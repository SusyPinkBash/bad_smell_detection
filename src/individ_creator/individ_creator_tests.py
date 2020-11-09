import unittest
from individ_creator import *
from owlready2 import destroy_entity


class IndividCreatorTests(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(IndividCreatorTests, self).__init__(*args, **kwargs)
        self.path_file_owl = "res/tree.owl"
        self.path_project = "res/android-chess/app/src/main/java/jwtc/chess/"

    def create_ontology(self, code):
        classes = defaultdict()
        for _, node in jl.parse.parse(code):
            if type(node) is jl.tree.ClassDeclaration:
                classes.setdefault(node.name, []).append(node)
        return populate_ontology(get_ontology(self.path_file_owl).load(), classes)

    def delete_ontology(self, onto):
        for e in onto["ClassDeclaration"].instances():
            destroy_entity(e)

    def test_10(self):
        classes = get_classesAST(self.path_project)
        self.assertEqual(type(classes), type(defaultdict()), "The Classes should be placed in a dictionary")
        self.assertEqual(len(classes), 10, "There are missing classes")

    def test_11(self):
        code = "class A { int x, y; }"
        ontology = self.create_ontology(code)
        instance = ontology['ClassDeclaration'].instances()[0]
        self.assertEqual(instance.body[0].is_a[0].name, "FieldDeclaration", "Should be a FieldDeclaration definition")
        self.assertEqual(instance.body[0].jname[0], 'x', "jname should be equal to x")
        self.assertEqual(instance.body[1].is_a[0].name, "FieldDeclaration", "Should be a FieldDeclaration definition")
        self.assertEqual(instance.body[1].jname[0], 'y', "jname should be equal to y")
        self.delete_ontology(ontology)

    def test_12(self):
        code = "class A { int x, y; public A() { } public int getX() { return x;} }"
        ontology = self.create_ontology(code)
        instance = ontology['ClassDeclaration'].instances()[0]
        self.assertEqual(instance.body[0].is_a[0].name, "MethodDeclaration", "Should be a MethodDeclaration definition")
        self.assertEqual(instance.body[0].jname[0], 'getX', "jname should be equal to getX")
        self.assertEqual(instance.body[1].is_a[0].name, "FieldDeclaration", "Should be a FieldDeclaration definition")
        self.assertEqual(instance.body[1].jname[0], 'x', "jname should be equal to x")
        self.assertEqual(instance.body[2].is_a[0].name, "FieldDeclaration", "Should be a FieldDeclaration definition")
        self.assertEqual(instance.body[2].jname[0], 'y', "jname should be equal to y")
        self.assertEqual(instance.body[3].is_a[0].name, "ConstructorDeclaration",
                         "Should be a MethodDeclaration definition")
        self.assertEqual(instance.body[3].jname[0], 'A', "jname should be equal to A")
        self.delete_ontology(ontology)

    def test_13(self):
        code = "class A { int f(int x, int y) { return 0; } }"
        ontology = self.create_ontology(code)
        instance = ontology['ClassDeclaration'].instances()[0]
        self.assertEqual(instance.body[0].is_a[0].name, "MethodDeclaration", "Should be a MethodDeclaration definition")
        self.assertEqual(instance.body[0].jname[0], 'f', "jname should be equal to f")
        self.assertEqual(instance.body[0].parameters[0].jname[0], 'x', "jname should be equal to x")
        self.assertEqual(instance.body[0].parameters[1].jname[0], 'y', "jname should be equal to y")
        self.assertEqual(instance.body[0].body[0].is_a[0].name, 'ReturnStatement',
                         "name should be equal to ReturnStatement")
        self.delete_ontology(ontology)

    def test_14(self):
        code = "class A { public int sum(int[] arr) { int sum = 0; for(int i=0; i < arr.length; ++i) " \
               "{ sum += arr[i]; } return sum; }}"
        ontology = self.create_ontology(code)
        instance = ontology['ClassDeclaration'].instances()[0]
        b0 = instance.body[0]
        self.assertEqual(b0.jname[0], 'sum', "jname should be equal to sum")
        self.assertEqual(b0.parameters[0].jname[0], 'arr', "jname should be equal to arr")
        self.assertEqual(b0.parameters[0].is_a[0].name, 'FormalParameter', "Should be a FormalParameter definition")
        self.assertEqual(b0.body[0].is_a[0].name, "ForStatement", "Should be a ForStatement definition")
        self.assertEqual(b0.body[1].is_a[0].name, 'BlockStatement', "name should be equal to BlockStatement")
        self.assertEqual(b0.body[2].is_a[0].name, 'StatementExpression', "name should be equal to StatementExpression")
        self.assertEqual(b0.body[3].is_a[0].name, 'ReturnStatement', "name should be equal to ReturnStatement")
        self.delete_ontology(ontology)

    def test_15(self):
        code = "class A { public void other(int x) { while(x < 10) ++x; } public boolean test(int x, int y) " \
               "{ if (x >= y) return x; else return y; } }"
        ontology = self.create_ontology(code)
        instance = ontology['ClassDeclaration'].instances()[0]
        b0 = instance.body[0]
        self.assertEqual(b0.jname[0], 'other', "jname should be equal to other")
        self.assertEqual(b0.parameters[0].jname[0], 'x', "jname should be equal to x")
        self.assertEqual(b0.parameters[0].is_a[0].name, 'FormalParameter', "Should be a FormalParameter definition")
        self.assertEqual(b0.body[0].is_a[0].name, "WhileStatement", "Should be a WhileStatement definition")
        self.assertEqual(b0.body[1].is_a[0].name, "StatementExpression", "Should be a StatementExpression definition")

        b1 = instance.body[1]
        self.assertEqual(b1.jname[0], 'test', "jname should be equal to test")
        self.assertEqual(b1.parameters[0].is_a[0].name, 'FormalParameter', "Should be a FormalParameter definition")
        self.assertEqual(b1.parameters[1].is_a[0].name, 'FormalParameter', "Should be a FormalParameter definition")
        self.assertEqual(b1.body[0].is_a[0].name, "IfStatement", "Should be a IfStatement definition")
        self.assertEqual(b1.body[1].is_a[0].name, "ReturnStatement", "Should be a ReturnStatement definition")
        self.assertEqual(b1.body[2].is_a[0].name, "ReturnStatement", "Should be a ReturnStatement definition")

        self.delete_ontology(ontology)


unittest.main()
