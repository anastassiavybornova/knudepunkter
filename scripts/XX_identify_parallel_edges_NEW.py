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
    homepath + "/data/processed/workflow_steps/network_edges_with_parallel.gpkg"
)
output_file_nodes = (
    homepath + "/data/processed/workflow_steps/nodes_edges_parallel.gpkg"
)

output_file_edges_no_parallel = (
    homepath + "/data/processed/workflow_steps/network_edges_no_parallel.gpkg"
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

    if parent_geom.distance(row.geometry) > 100:
        continue
    else:
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

# delete modified edges whith same u and v
edges.drop(
    edges.loc[(edges.u == edges.v) & (edges.modified == True)].index, inplace=True
)

# find parallel edges of approximate same length
edges["drop"] = False
edges["length"] = edges.geometry.length

grouped = edges.groupby(["u", "v"])

for name, group in grouped:
    if len(group) > 1:
        # compare length of all members in groups pair wise
        group_lengths = group.length.to_list()

        duplicates = []
        # mark as duplicate if length difference is less than 20 %
        for i in range(len(group_lengths)):
            for j in range(i + 1, len(group_lengths)):
                if (
                    abs(
                        (
                            (group_lengths[i] - group_lengths[j])
                            / ((group_lengths[i] + group_lengths[j]) / 2)
                        )
                        * 100
                    )
                    < 8
                ):
                    duplicates.append((group_lengths[i], group_lengths[j]))

        length_of_edges_to_drop = set([min(d) for d in duplicates])

        edges.loc[
            group.loc[group.length.isin(length_of_edges_to_drop)].index, "drop"
        ] = True


# nodes used by new network edges
nodes_in_use = nodes.loc[nodes.node_id.isin(set(edges.u.to_list() + edges.v.to_list()))]

# edges without parallel edges
edges_no_parallel = edges.loc[edges["drop"] == False]

assert len(nodes.loc[nodes.ismain == True]) == len(
    nodes_in_use.loc[nodes_in_use.ismain == True]
)

# Export
assert len(edges) == len(edges.id.unique())
assert len(edges_no_parallel) == len(edges_no_parallel.id.unique())
assert len(nodes_in_use) == len(nodes_in_use.id.unique())

nodes_in_use.to_file(output_file_nodes)
edges.to_file(output_file_edges)

edges_no_parallel.to_file(output_file_edges_no_parallel)


# Remove temporary layers from project if they exist already
remove_existing_layers(["input edges", "input nodes", "output edges", "output nodes"])

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
    parallel_edges = QgsVectorLayer(output_file_edges, "output edges", "ogr")
    QgsProject.instance().addMapLayer(parallel_edges)

    draw_categorical_layer("output edges", "drop", alpha=180, line_style="solid")

    no_parallel_edges = QgsVectorLayer(
        output_file_edges_no_parallel, "output edges (without parallel edges)", "ogr"
    )
    QgsProject.instance().addMapLayer(no_parallel_edges)

    draw_recent_simple_line_layer(color="red", width=1)

    output_nodes = QgsVectorLayer(output_file_nodes, "output nodes", "ogr")
    QgsProject.instance().addMapLayer(output_nodes)

    draw_categorical_layer(
        "output nodes",
        "ismain",
        outline_width=0.0,
        alpha=200,
        marker_size=4,
    )

    zoom_to_layer("output edges")

if display_input and display_output:
    group_layers(
        "Find parallel edges",
        [
            "input edges",
            "input nodes",
            "output edges",
            "output edges (without parallel edges)",
            "output nodes",
        ],
        remove_group_if_exists=True,
    )

if display_input == False and display_output == True:
    group_layers(
        "Find parallel edges",
        ["output edges", "output edges (without parallel edges)", "output nodes"],
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
