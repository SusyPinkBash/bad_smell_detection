from sys import argv
import rdflib.plugins.sparql as sq
from owlready2 import *


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
        ?m a tree:{query_type} .
        ?m tree:jname ?method_name . 
        ?m tree:body ?statements .
        }} GROUP BY ?m"""

    return [(row.method_name, row.cnt)
            for row in graph.query(prepare_query(query))
            if (int(row.cnt) >= 20)]


def query_large_class(graph):
    # >= 10 methods
    query = f"""SELECT ?class_name (COUNT(*) AS ?cnt) 
        WHERE {{
        ?c a tree:ClassDeclaration .
       ?c tree:jname ?class_name .
       ?c tree:body ?method .
       ?method a tree:MethodDeclaration .
       }} GROUP BY ?c"""

    return [(row.class_name, row.cnt)
            for row in graph.query(prepare_query(query))
            if (int(row.cnt) >= 10)]


def query_method_with_switch(graph):
    # >= 1 switch statement in method/constructor body
    return "TODO"


def query_constructor_with_switch(graph):
    # >= 1 switch statement in method/constructor body
    return "TODO"


def query_method_with_long_parameter_list(graph):
    # >= 1 switch statement in method/constructor body
    return "TODO"


def query_constructor_with_long_parameter_list(graph):
    # >= 5 parameters
    return "TODO"


def query_data_class(graph):
    # class with only setters and getters
    return "TODO"


def run_queries(graph):
    # TODO: return all results in a dictionary
    queries = {
        # >= 20 statements
        "LongMethod": query_long("MethodDeclaration", graph),
        "LongConstructor": query_long("ConstructorDeclaration", graph),
        # >= 10 methods
        "LargeClass": query_large_class(graph),
        # >= 1 switch statement in method/constructor body
        "MethodWithSwitch": query_method_with_switch(graph),
        "ConstructorWithSwitch": query_constructor_with_switch(graph),
        # >= 5 parameters
        "MethodWithLongParameterList": query_method_with_long_parameter_list(graph),
        "ConstructorWithLongParameterList": query_constructor_with_long_parameter_list(graph),
        # class with only setters and getters
        "DataClass": query_data_class(graph)
    }
    print_queries(queries)


def print_queries(queries):
    for key in queries:
        print(key, ": ", queries[key], '\n')


if __name__ == "__main__":
    file = "res/tree2.owl" if len(argv) < 2 else argv[1]
    start(file)
