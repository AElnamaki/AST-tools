# Very simple AST analysis tool for the dci_fbw_p23_e07 Class 
# Date : okt 2023
# Written by: Elnamaki 
import pydot
import ast
import os
import termcolor
from prettytable import PrettyTable

def traverse_ast(node, parent, graph):
    current_node = pydot.Node(node.__class__.__name__, style="filled", fillcolor=get_node_color(node.__class__.__name__),
                             shape=get_node_shape(node.__class__.__name__), fontsize=10)
    if isinstance(node, ast.Name):
        # Add the variable name as an attribute to the node
        current_node.set_label(node.id)
    
    if isinstance(node, ast.FunctionDef):
        # Add the function name as an attribute to the node
        current_node.set_label(node.id)
    
    if isinstance(node, ast.If):
        # Add additional information for If nodes
        additional_info = "Conditional statement with " + str(len(node.orelse)) + " alternate path(s)."
        current_node.set_label(additional_info)
    graph.add_node(current_node)
    # Add explanations for specific node types
    explanations = {

        "Module": "This node is the root of the AST.",
        "Expr": "A single Python expression.",
        "Name": "A Python variable or function name.",
        "Const": "A Python literal value, such as a string, number, or boolean.",
        "BinOp": "Such as addition, subtraction, or multiplication.",
        "UnaryOp": "Such as negation or inversion.","Call": "A function call.",
        "Subscript": "A subscripting operation, such as list[0].",
        "Attribute": "An attribute access, such as obj.attr",
        "AugAssign": "An augmented assignment operation, such as x += 1.",
        "Assign": " A simple assignment operation, such as x = 1.",
        "IfExp": "A conditional expression, such as x if y else z.",
        "Lambda": "A lambda expression, such as lambda x: x + 1.",
        "ClassDef": "A class definition, such as class MyClass: ...",
        "For": "A for loop, such as for i in range(10): ..",
        "While": "A while loop, such as while x < 10: ...",
        "Try": "A try/except block, .",
        "With": "A with statement, such as with open('myfile.txt', 'r') as f: .",
        "AugAssign": "Augments a variable in place.",
        "BinOp": "Binary operation, such as addition, subtraction, or multiplication.",
        "BoolOp": "Boolean operation, such as and, or, or not.",
        "Call": "Calls a function.",
        "Compare": "Comparison operation, such as greater than, less than, or equal to.",
        "For": "For loop.",
        "FunctionDef": "Defines a function.",
        "If": "Conditional statement.",
        "Import": "Imports a module.",
        "ImportFrom": "Imports a module from a specific package.",
        "List": "Creates a list.",
        "Name": "A variable name.",
        "Num": "A numeric literal.",
        "Str": "A string literal.",
        "Subscript": "Subscribes a list or tuple.",
        "UnaryOp": "Unary operation, such as negation or inversion.",
        "With": "With statement."
        }
    if node.__class__.__name__ in explanations:
        graph.add_edge(pydot.Edge(pydot.Node(explanations[node.__class__.__name__], shape="note"),
                                  current_node, style="dashed"))

    if parent is not None:
        graph.add_edge(pydot.Edge(parent, current_node, label=get_edge_label(node)))
    for child in ast.iter_child_nodes(node):
        traverse_ast(child, current_node, graph)

def get_node_color(node_type):
    if node_type == "Assign":
        return "lightblue"
    elif node_type == "AugAssign":
        return "lightgreen"
    elif node_type == "BinOp":
        return "lightgray"
    elif node_type == "BoolOp":
        return "yellow"
    elif node_type == "Call":
        return "orange"
    elif node_type == "Compare":
        return "red"
    elif node_type == "For":
        return "purple"
    elif node_type == "FunctionDef":
        return "black"
    elif node_type == "If":
        return "pink"
    elif node_type == "Import":
        return "teal"
    elif node_type == "ImportFrom":
        return "blue"
    elif node_type == "List":
        return "limegreen"
    elif node_type == "Name":
        return "cyan"
    elif node_type == "Num":
        return "magenta"
    elif node_type == "Str":
        return "gold"
    elif node_type == "Subscript":
        return "silver"
    elif node_type == "UnaryOp":
        return "gray"
    elif node_type == "With":
        return "brown"
    else:
        return "white"

def get_node_shape(node_type):
    if node_type == "Assign":
        return "ellipse"
    elif node_type == "AugAssign":
        return "box"
    elif node_type == "BinOp":
        return "diamond"
    elif node_type == "BoolOp":
        return "ellipse"
    elif node_type == "Call":
        return "ellipse"
    elif node_type == "Compare":
        return "ellipse"
    elif node_type == "For":
        return "ellipse"
    elif node_type == "FunctionDef":
        return "ellipse"
    elif node_type == "If":
        return "ellipse"
    elif node_type == "Import":
        return "ellipse"
    elif node_type == "ImportFrom":
        return "ellipse"
    elif node_type == "List":
        return "ellipse"
    elif node_type == "Name":
        return "ellipse"
    elif node_type == "Num":
        return "ellipse"
    elif node_type == "Str":
        return "ellipse"
    elif node_type == "Subscript":
        return "ellipse"
    elif node_type == "UnaryOp":
        return "ellipse"
    elif node_type == "With":
        return "ellipse"
    else:
        return "ellipse"

def get_edge_label(node):
    # Features logic for edge labels . 
    return ""


def highlight_nodes(graph, node_types):
    for node in graph.get_nodes():
        if node.get_name() in node_types:
            node.set_fillcolor("yellow")

def identify_skipping_operations(ast_tree):
    skipping_operations = set()
    for node in ast.walk(ast_tree):
        if isinstance(node, ast.Continue) or isinstance(node, ast.Break):
            skipping_operations.add(type(node).__name__)
    return skipping_operations

def generate_summary(ast_tree):
    summary = {"Total Nodes": 0}
    for node in ast.walk(ast_tree):
        node_type = type(node).__name__
        summary["Total Nodes"] += 1
        summary[node_type] = summary.get(node_type, 0) + 1
    return summary

try:
    file_path = input("Enter the path to the Python file: ")

    if os.path.isfile(file_path) and file_path.lower().endswith('.py'):
        with open(file_path, "r") as f:
            source_code = f.read()

        ast_tree = ast.parse(source_code)
        graph = pydot.Dot(graph_type='digraph', rankdir="TB", fontname="Helvetica")

        # Add title node
        title = pydot.Node("AST Visualization", style="filled", fillcolor="lightgreen",
                           shape="box", fontsize=12)
        graph.add_node(title)

        traverse_ast(ast_tree, title, graph)
        highlight_nodes(graph, ["FunctionDef", "If"])
        file_name = 'file_graph.png'
        
        # Check if file with the same name already exists
        count = 1
        while os.path.exists(file_name):
            count += 1
            file_name = f'file_graph{count}.png'

        graph.write_png(file_name)

        summary = generate_summary(ast_tree)
        print("The graph is successfully generated as ", file_name)
        table = PrettyTable()
        table.field_names = ["Node Type", "Count"]
        for key, value in summary.items():
            table.add_row([termcolor.colored (key, "red"), termcolor.colored(value, "green")])
        
        print("\nSummary about your code:")
        print(table)
        
        
        skipping_operations = identify_skipping_operations(ast_tree)
        if skipping_operations:
            print("\nSkipping Operations Detected:")
            for op in skipping_operations:
                print(f"- {op}")
        else:
            print("\nNo skipping operations detected in the code.")
            
    else:
        print("Error: Please provide a valid Python file with a '.py' extension.")
except FileNotFoundError:
    print("Error: File not found. Please check the file path and try again.")
except Exception as e:
    print(f"An error occurred: {e}")
