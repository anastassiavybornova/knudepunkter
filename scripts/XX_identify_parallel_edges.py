# SCRIPT TO IDENTIFY PARALLEL EDGES AND PARALLEL EDGES ON SAME ROAD

### *********
### CUSTOM SETTINGS
### *********

### indicate which layers to display

display_input = True
display_output = True

### NO CHANGES BELOW THIS LINE

# define homepath variable (where is the qgis project saved?)
homepath = QgsProject.instance().homePath()
exec(open(homepath + "/src/plot_func.py").read())

from qgis.core import *

import geopandas as gpd
import pandas as pd
from shapely.geometry import Point, LineString
from src import graphedit

output_file_edges = (
    homepath + "/data/processed/workflow_steps/network_parallel_edges.gpkg"
)
output_file_nodes = (
    homepath + "/data/processed/workflow_steps/nodes_for_parallel_edges.gpkg"
)


# load data
nodepath = (
    homepath
    + "/data/raw/folkersma_digital/2023-08-01 Cycling network Denmark shapefiles/node.shp"
)
edgepath = (
    homepath
    + "/data/raw/folkersma_digital/2023-08-01 Cycling network Denmark shapefiles/stretch.shp"
)


# load data (VSC version)
# nodepath = "../data/raw/folkersma_digital/2023-08-01 Cycling network Denmark shapefiles/node.shp"
# edgepath = "../data/raw/folkersma_digital/2023-08-01 Cycling network Denmark shapefiles/stretch.shp"
# output_file = "../data/processed/workflow_steps/network_parallel_edges.gpkg"

nodes = gpd.read_file(nodepath)
edges = gpd.read_file(edgepath)

nodes.to_crs("EPSG:25832", inplace=True)
edges.to_crs("EPSG:25832", inplace=True)

# create distinct column names for unique id
edges["edge_id"] = edges.id
nodes["node_id"] = nodes.id

# assign edges initial start and end nodes
edges = graphedit.assign_edges_start_end_nodes(edges, nodes)

# find all child nodes with parents that are not dead ends
child_nodes = nodes[(nodes.refmain.notna()) & (nodes.deadend == 0)]

edges["modified"] = False

# assign edges from child nodes with parents to parent nodes
for ix, row in child_nodes.iterrows():
    # ID of this child node
    this_node_id = row.node_id

    # geometry of the child nodes parent node
    parent_geom = nodes.loc[
        nodes.node_id == int(child_nodes.loc[ix, "refmain"])
    ].geometry.values[0]

    # all edges which have this child node as their start node
    edges_start = edges.loc[edges.u == this_node_id]

    # all edges which have this child node as their end node
    edges_end = edges.loc[edges.v == this_node_id]

    for ix, row in edges_start.iterrows():
        # get coordinate in edge linestring
        edge_coords = list(row.geometry.coords)

        # replace start coordinate (child node) with geometry of parent node
        edge_coords[0] = parent_geom.coords[0]

        # create new linestring from updated coordinates
        new_linestring = LineString(edge_coords)

        # update edge geometry
        edges.loc[ix, "geometry"] = new_linestring

        # mark edge as modified
        edges.loc[ix, "modified"] = True

    for ix, row in edges_end.iterrows():
        # get coordinate in edge linestring
        edge_coords = list(row.geometry.coords)

        # replace end coordinate (child node) with geometry of parent node
        edge_coords[-1] = parent_geom.coords[0]

        # create new linestring from updated coordinates
        new_linestring = LineString(edge_coords)

        # update edge geometry
        edges.loc[ix, "geometry"] = new_linestring

        # mark edge as modified
        edges.loc[ix, "modified"] = True

# drop old u,v columns
edges.drop(["u", "v"], axis=1, inplace=True)

# find new start and end nodes
edges = graphedit.assign_edges_start_end_nodes(edges, nodes)

# find edges with same start and end node (but could still be on different roads!)
edges["key"] = 0

# Set u to be to be the smaller one of u,v nodes (based on node id) - to identify parallel edges between u,v / v,u matches
graphedit.order_edge_nodes(edges)

edges = graphedit.find_parallel_edges(edges)

# child_node_ids = nodes.loc[nodes.ismain == 0]["node_id"].to_list()

# # Identify parallel edges on same roads that should be excluded from e.g. length computation
# # Based on parent-child node classification
# parallel_edges = []
# grouped_edges = edges.groupby(["u", "v"])
# assert len(grouped_edges) == len(edges.loc[edges.key == 0])

# for nodes_ids, group in grouped_edges:
#     if (
#         nodes_ids[0] in child_node_ids
#         and nodes_ids[1] in child_node_ids
#         and len(group) > 1
#     ):
#         parallel_edges.append(group["length"].idxmin())

# edges["parallel"] = 0
# edges.loc[parallel_edges, "parallel"] = 1

# assert len(edges.loc[edges.parallel == 1]) == len(parallel_edges)

# delete modified edges whith same u and v
edges.drop(
    edges.loc[(edges.u == edges.v) & (edges.modified == True)].index, inplace=True
)

nodes_in_use_ids = set(edges.u.to_list() + edges.v.to_list())
nodes_in_use = nodes.loc[nodes.node_id.isin(nodes_in_use_ids)]

assert len(nodes.loc[nodes.ismain == True]) == len(
    nodes_in_use.loc[nodes_in_use.ismain == True]
)

# Export
nodes_in_use.to_file(output_file_nodes)
edges.to_file(output_file_edges)

# Remove temporary layers from project if they exist already
remove_existing_layers(["input edges", "input nodes", "parallel edges", "output nodes"])

if display_input:
    # input data
    input_edges = QgsVectorLayer(edgepath, "input edges", "ogr")
    QgsProject.instance().addMapLayer(input_edges)
    draw_recent_simple_line_layer(color="purple", width=0.5)

    input_nodes = QgsVectorLayer(nodepath, "input nodes", "ogr")
    QgsProject.instance().addMapLayer(input_nodes)

    draw_categorical_layer(
        "input nodes",
        "ismain",
        outline_width=0.0,
        alpha=200,
        marker_size=2,
    )

    zoom_to_layer("input data")

if display_output:
    parallel_edges = QgsVectorLayer(output_file_edges, "parallel edges", "ogr")
    QgsProject.instance().addMapLayer(parallel_edges)

    draw_categorical_layer("parallel edges", "key", alpha=180, line_style="solid")

    # parallel_edges = QgsVectorLayer(output_file, "parallel edges (same road)", "ogr")
    # QgsProject.instance().addMapLayer(parallel_edges)

    # draw_categorical_layer(
    #     "parallel edges (same road)", "parallel", alpha=180, line_style="solid"
    # )

    output_nodes = QgsVectorLayer(output_file_nodes, "output nodes", "ogr")
    QgsProject.instance().addMapLayer(output_nodes)

    draw_categorical_layer(
        "output nodes",
        "ismain",
        outline_width=0.0,
        alpha=200,
        marker_size=4,
    )

    zoom_to_layer("parallel edges")

if display_input and display_output:
    group_layers(
        "Find parallel edges",
        [
            "input edges",
            "input nodes",
            "output nodes",
            "parallel edges",
        ],
        remove_group_if_exists=True,
    )

if display_input == False and display_output == True:
    group_layers(
        "Find parallel edges",
        ["parallel edges", "output nodes"],
        remove_group_if_exists=True,
    )

if display_input == True and display_output == False:
    group_layers(
        "Find parallel edges",
        [
            "input edges",
            "input nodes",
        ],
        remove_group_if_exists=True,
    )

# Method below only works if it is a topological network - otherwise, it will return too few or too many nodes


# def find_nearest_points(row, nodes):
#     line_geom = row.geometry

#     dist_df = pd.DataFrame(nodes.distance(line_geom), columns=["dist"])

#     nodes_index = dist_df.loc[dist_df.dist == 0.0].index.to_list()
#     if len(nodes_index) > 2:
#         print(len(nodes_index))

#     return nodes_index


# edges["nearest_nodes"] = edges.apply(
#     lambda x: find_nearest_points(row=x, nodes=nodes), axis=1
# )
