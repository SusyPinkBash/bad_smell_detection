from sys import argv
import rdflib.plugins.sparql as sq
from owlready2 import *


class ClassSmell:
    def __init__(self, row):
        self.class_name = str(row.class_name)
        self.counter = int(row.cnt)


class MethodSmell(ClassSmell):

    def __init__(self, row):
        super().__init__(row)
        self.method_name = str(row.method_name)


def start(owl_path):
    world = World()
    ontology = world.get_ontology(owl_path).load()
    graph = world.as_rdflib_graph()
    run_queries(graph)


def prepare_query(string):
    return sq.prepareQuery(string, initNs={"tree": "http://my.onto.org/tree.owl#"})


def query_long(query_type, graph):
    # >= 20
    query = f""" SELECT ?class_name ?method_name (COUNT(*) AS ?cnt) 
        WHERE {{ 
        ?c a tree:ClassDeclaration .
        ?c tree:jname ?class_name .
        ?c tree:body ?m .
        ?m a tree:{query_type}Declaration .
        ?m tree:jname ?method_name . 
        ?m tree:body ?statements .
        }} GROUP BY ?m"""

    return [MethodSmell(row) for row in graph.query(prepare_query(query)) if (int(row.cnt) >= 20)]


def query_large_class(graph):
    # >= 10 methods
    query = f"""SELECT ?class_name (COUNT(*) AS ?cnt) 
        WHERE {{
        ?c a tree:ClassDeclaration .
       ?c tree:jname ?class_name .
       ?c tree:body ?method_name .
       ?method a tree:MethodDeclaration .
       }} GROUP BY ?c"""

    return [ClassSmell(row) for row in graph.query(prepare_query(query)) if (int(row.cnt) >= 10)]


def query_with_switch(query_type, graph):
    # >= 1 switch statement in method/constructor body
    query = f""" SELECT ?class_name ?method_name (COUNT(*) AS ?cnt) 
                WHERE {{
                ?c a tree:ClassDeclaration . 
                ?c tree:jname ?class_name . 
                ?c tree:body ?m .
                ?m a tree:{query_type}Declaration .
                ?m tree:jname ?method_name .
                ?m tree:body ?s . 
                ?s a tree:SwitchStatement
                }} GROUP BY ?m"""

    return [MethodSmell(row) for row in graph.query(prepare_query(query)) if (int(row.cnt) >= 1)]


def query_with_long_parameter_list(query_type, graph):
    # >= 5 parameters
    query = f""" SELECT ?class_name ?method_name (COUNT(*) AS ?cnt) 
                WHERE {{ 
                ?c a tree:ClassDeclaration .
                ?c tree:jname ?class_name .
                ?c tree:body ?m .
                ?m a tree:{query_type}Declaration .
                ?m tree:jname ?method_name . 
                ?m tree:parameters ?param .
                }} GROUP BY ?m"""

    return [MethodSmell(row) for row in graph.query(prepare_query(query)) if (int(row.cnt) >= 5)]


def query_constructor_with_long_parameter_list(graph):
    # >= 5 parameters
    return "TODO"


def query_data_class(graph):
    # class with only setters and getters
    query0 = f""" SELECT ?class_name (COUNT(*) AS ?cnt) 
                WHERE {{
                ?c a tree:ClassDeclaration .
                ?c tree:jname ?class_name .
                ?c tree:body ?m .
                ?m a tree:MethodDeclaration .
                }} GROUP BY ?c"""

    query1 = f""" SELECT ?class_name (COUNT(*) as ?cnt) 
                WHERE {{ ?c a tree:ClassDeclaration .
                ?c tree:jname ?class_name .
                ?c tree:body ?m .
                ?m a tree:MethodDeclaration .
                ?m tree:jname ?method_name .
                FILTER regex(?method_name , "^(get|set)", "i") .
                }} GROUP BY ?c"""

    large_class = [ClassSmell(row) for row in graph.query(prepare_query(query0)) if row.cnt]
    get_and_set = [ClassSmell(row) for row in graph.query(prepare_query(query1)) if row.cnt]
    return [method for large in large_class for method in get_and_set
            if large.class_name == method.class_name and large.counter == method.counter]


def run_queries(graph):
    # TODO: return all results in a dictionary
    queries = {
        # >= 20 statements
        "LongMethod": query_long("Method", graph),
        "LongConstructor": query_long("Constructor", graph),
        # >= 10 methods
        "LargeClass": query_large_class(graph),
        # >= 1 switch statement in method/constructor body
        "MethodWithSwitch": query_with_switch("Method", graph),
        "ConstructorWithSwitch": query_with_switch("Constructor", graph),
        # >= 5 parameters
        "MethodWithLongParameterList": query_with_long_parameter_list("Method", graph),
        "ConstructorWithLongParameterList": query_with_long_parameter_list("Constructor", graph),
        # class with only setters and getters
        "DataClass": query_data_class(graph)
    }
    print_queries(queries)


def print_queries(queries):
    for key in queries:
        print(key, ":")
        if queries[key] != "TODO":
            for element in queries[key]:
                string = '\t' + str(element.class_name) + ' '
                if type(element) == MethodSmell:
                    string += str(element.method_name) + ' '
                string += str(element.counter)
                print(string)
            print()


if __name__ == "__main__":
    file = "res/tree2.owl" if len(argv) < 2 else argv[1]
    start(file)
