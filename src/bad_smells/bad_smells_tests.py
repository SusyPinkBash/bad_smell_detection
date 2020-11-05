import unittest

import rdflib
from bad_smells import *
from individ_creator import *
from owlready2 import destroy_entity


class BadSmellsTests(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(BadSmellsTests, self).__init__(*args, **kwargs)
        self.path_file_owl = "res/tree.owl"

    def create_ontology(self, code):
        classes = defaultdict()
        for _, node in jl.parse.parse(code):
            if type(node) is jl.tree.ClassDeclaration:
                classes.setdefault(node.name, []).append(node)
        return populate_ontology(get_ontology(self.path_file_owl).load(), classes)

    def get_graph(self, ontology):
        ontology.save(file="res/test3.owl", format="rdfxml")
        graph = rdflib.Graph()
        graph.load("res/test3.owl")
        return graph

    def delete_ontology(self, onto):
        for e in onto["ClassDeclaration"].instances():
            destroy_entity(e)

    def test31(self):
        code = "class A { int f(int x) {  x++;x++;x++;x++;x++;x++;x++;x++;x++;x++;x++;x++;x++;x++;x++;x++;x++;x++;" \
               "x++;x++;x++; return x; } }"
        ontology = self.create_ontology(code)
        graph = self.get_graph(ontology)
        self.assertEqual(len(query_long("Method", graph)), 1)
        self.delete_ontology(ontology)

    def test32(self):
        code = "class A { public A(int x) {  x++;x++;x++;x++;x++;x++;x++;x++;x++;x++;x++;x++;x++;x++;x++;x++;x++;" \
               "x++;x++;x++;x++; }}"
        ontology = self.create_ontology(code)
        graph = self.get_graph(ontology)
        self.assertEqual(len(query_long("Constructor", graph)), 1)
        self.delete_ontology(ontology)

    def test33(self):
        code = "class A { void a(){} void b(){} void c(){} int d() {return 1;} void e(){} void f() {} void g(){}" \
               " void h(){} void i(){} void l(){} }"
        ontology = self.create_ontology(code)
        graph = self.get_graph(ontology)
        self.assertEqual(len(query_large_class(graph)), 1)
        self.delete_ontology(ontology)

    def test34(self):
        code = "class A { void a(){ int i = 0; switch(i){ case 1: System.out.println(); break; " \
               "case 2: System.out.println(); break; default: System.out.println(); } } }"
        ontology = self.create_ontology(code)
        graph = self.get_graph(ontology)
        self.assertEqual(len(query_with_switch("Method", graph)), 1)
        self.delete_ontology(ontology)

    def test35(self):
        code = "class A { public A() { int i = 0; switch(i){ case 1: System.out.println(); break;" \
               "case 2: System.out.println(); break; default: System.out.println(); } } }"
        ontology = self.create_ontology(code)
        graph = self.get_graph(ontology)
        self.assertEqual(len(query_with_switch("Constructor", graph)), 1)
        self.delete_ontology(ontology)

    def test36(self):
        code = "class A { void a(int x, int y, int z, String args1, String args2){ } " \
               "int b(int x, int y, int z, String args1, String args2){ } }"
        ontology = self.create_ontology(code)
        graph = self.get_graph(ontology)
        self.assertEqual(len(query_with_long_parameter_list("Method", graph)), 2)
        self.delete_ontology(ontology)

    def test37(self):
        code = "class A { public A(int x, int y, int z, String args1, String args2) { } }"
        ontology = self.create_ontology(code)
        graph = self.get_graph(ontology)
        self.assertEqual(len(query_with_long_parameter_list("Constructor", graph)), 1)
        self.delete_ontology(ontology)

    def test38(self):
        code = "class A { private int x = 0; public int getX() { return x; } public void setX(int x) {this.x = x;} }"
        ontology = self.create_ontology(code)
        graph = self.get_graph(ontology)
        self.assertEqual(len(query_data_class(graph)), 1)
        self.delete_ontology(ontology)






unittest.main()
