import csv
import itertools
import os

import click
import numpy as np


def normalize(layer_widths):
    return list((layer_widths - np.max(layer_widths)) / 2)


def vertices(layer_widths, directory, x_separation=2, y_separation=1.5, **kwargs):
    normalizing_width = normalize(layer_widths) 
    with open("{}/vertices.csv".format(directory), "w", newline="") as file:
        csv_writer = csv.writer(file, delimiter=",")
        csv_writer.writerow(
            ["id", "x", "y", "size", "color", "opacity", "label", "layer"]
        )

        for layer in range(len(layer_widths)):
            for node in range(layer_widths[layer]):
                x_pos = x_separation * layer
                y_pos = y_separation * (normalizing_width[layer] - node)
                csv_writer.writerow(["l{}n{}".format(layer, node), x_pos, y_pos])


def edges(layer_widths, directory, neuron_connections=None, **kwargs):
    normalizing_width = normalize(layer_widths)

    with open("{}/edges.csv".format(directory), "w", newline="") as file:
        csv_writer = csv.writer(file, delimiter=",")
        csv_writer.writerow(
            ["u", "v", "label", "lw", "color", "opacity", "bend", "Direct"]
        )

        for layer in range(len(layer_widths) - 1):
            first_layer_nodes = [
                "l{}n{}".format(layer, j) for j in range(layer_widths[layer])
            ]

            for n, _ in enumerate(first_layer_nodes):
                connecting_nodes = [
                    "l{}n{}".format(layer + 1, j)

                    for j in range(layer_widths[layer + 1])

                    if neuron_connections is None or abs(n - j) < neuron_connections
                ]
                edges_ = list(
                    itertools.product([first_layer_nodes[n]], connecting_nodes)
                )

                for e in edges_:
                    csv_writer.writerow(e)


def latex_file(directory):
    template = """\\documentclass[tikz]{{standalone}}
\\usepackage{{tikz-network}}

\\begin{{document}}
    \\begin{{tikzpicture}}
        \\Vertices{{{dir}/vertices.csv}}
        \\Edges{{{dir}/edges.csv}}
    \\end{{tikzpicture}}
\\end{{document}}""".format(
        dir=directory
    )
    with open("{}.tex".format(directory), "w") as file:
        file.write(template)


@click.command()
@click.argument("layer_widths", nargs=-1, type=int)
@click.option(
    "--directory",
    "-d",
    default="./network",
    type=click.Path(),
    help="Directory of data files."
)
@click.option(
    "--layer_separation",
    "-x",
    default=2,
    type=float,
    help="Scaling of distance between layers.",
)
@click.option(
    "--node_separation",
    "-y",
    default=1.5,
    type=float,
    help="Scaling of distance between nodes.",
)

# @click.option("--neuron_connections", "-c", type=int)
@click.option("--latex", "-l", is_flag=True, help="Generate latex file.")
def network(layer_widths, directory, latex, **kwargs):
    """Generate data files for visualizing Neural Networks with the LaTeX package tikz-network.

    Input an arbitrary number of LAYER_WIDTHS, the number of nodes for every layer, and csv data files will be created.
    Latex file is created with the same name as the directory, default is 'network'.
    """
    if layer_widths:
        os.makedirs(directory, exist_ok=True)
        vertices(layer_widths, directory, **kwargs)
        edges(layer_widths, directory, **kwargs)

    if latex:
        latex_file(directory)
