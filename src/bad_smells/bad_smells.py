from sys import argv
import rdflib.plugins.sparql as sq
from owlready2 import *


class ClassSmell:
    def __init__(self, row):
        self.class_name = str(row.class_name)
        self.counter = int(row.counter)


class MethodSmell(ClassSmell):
    def __init__(self, row):
        super().__init__(row)
        self.method_name = str(row.method_name)


def start(owl_path):
    world = World()
    world.get_ontology(owl_path).load()
    graph = world.as_rdflib_graph()
    print_queries(run_queries(graph))


def prepare_query(string):
    return sq.prepareQuery(string, initNs={"tree": "http://my.onto.org/tree.owl#"})


def query_long(query_type, graph):
    # >= 20
    query = f""" SELECT ?class_name ?method_name (COUNT(*) AS ?counter) 
        WHERE {{ 
        ?c a tree:ClassDeclaration .
        ?c tree:jname ?class_name .
        ?c tree:body ?m .
        ?m a tree:{query_type}Declaration .
        ?m tree:jname ?method_name . 
        ?m tree:body ?statements .
        }} GROUP BY ?m"""

    return [MethodSmell(row) for row in graph.query(prepare_query(query)) if (int(row.counter) >= 20)]


def query_large_class(graph):
    # >= 10 methods
    query = f""" SELECT ?class_name (COUNT(*) AS ?counter) 
        WHERE {{
        ?c a tree:ClassDeclaration .
        ?c tree:jname ?class_name .
        ?c tree:body ?m .
        ?m a tree:MethodDeclaration .
        }} GROUP BY ?c"""

    return [ClassSmell(row) for row in graph.query(prepare_query(query)) if (int(row.counter) >= 10)]


def query_with_switch(query_type, graph):
    # >= 1 switch statement in method/constructor body
    query = f""" SELECT ?class_name ?method_name (COUNT(*) AS ?counter) 
        WHERE {{
        ?c a tree:ClassDeclaration . 
        ?c tree:jname ?class_name . 
        ?c tree:body ?m .
        ?m a tree:{query_type}Declaration .
        ?m tree:jname ?method_name .
        ?m tree:body ?s . 
        ?s a tree:SwitchStatement
        }} GROUP BY ?m"""

    return [MethodSmell(row) for row in graph.query(prepare_query(query)) if (int(row.counter) >= 1)]


def query_with_long_parameter_list(query_type, graph):
    # >= 5 parameters
    query = f""" SELECT ?class_name ?method_name (COUNT(*) AS ?counter) 
        WHERE {{ 
        ?c a tree:ClassDeclaration .
        ?c tree:jname ?class_name .
        ?c tree:body ?m .
        ?m a tree:{query_type}Declaration .
        ?m tree:jname ?method_name . 
        ?m tree:parameters ?param .
        }} GROUP BY ?m"""

    return [MethodSmell(row) for row in graph.query(prepare_query(query)) if (int(row.counter) >= 5)]


def query_data_class(graph):
    # class with only setters and getters
    query0 = f""" SELECT ?class_name (COUNT(*) AS ?counter) 
        WHERE {{
        ?c a tree:ClassDeclaration .
        ?c tree:jname ?class_name .
        ?c tree:body ?m .
        ?m a tree:MethodDeclaration .
        }} GROUP BY ?c"""

    query1 = f""" SELECT ?class_name (COUNT(*) as ?counter) 
        WHERE {{ ?c a tree:ClassDeclaration .
        ?c tree:jname ?class_name .
        ?c tree:body ?m .
        ?m a tree:MethodDeclaration .
        ?m tree:jname ?method_name .
        FILTER regex(?method_name , "^(get|set)", "i") .
        }} GROUP BY ?c"""

    large_class = [ClassSmell(row) for row in graph.query(prepare_query(query0)) if row.counter]
    get_and_set = [ClassSmell(row) for row in graph.query(prepare_query(query1)) if row.counter]
    return [method for large in large_class for method in get_and_set
            if large.class_name == method.class_name and large.counter == method.counter]


def run_queries(graph):
    return {
        "LongMethod": query_long("Method", graph),
        "LongConstructor": query_long("Constructor", graph),
        "LargeClass": query_large_class(graph),
        "MethodWithSwitch": query_with_switch("Method", graph),
        "ConstructorWithSwitch": query_with_switch("Constructor", graph),
        "MethodWithLongParameterList": query_with_long_parameter_list("Method", graph),
        "ConstructorWithLongParameterList": query_with_long_parameter_list("Constructor", graph),
        "DataClass": query_data_class(graph)
    }


def print_queries(queries):
    for key in queries:
        if len(queries[key]) == 0:
            print("No bad smell found for " + key)
        else:
            print(key, ":")
            for element in queries[key]:
                string = '\t' + str(element.class_name) + ' '
                if type(element) == MethodSmell:
                    string += str(element.method_name) + ' '
                string += str(element.counter)
                print(string)
        print()


if __name__ == "__main__":
    start(argv[1] if len(argv) > 1 else "res/tree2.py")
