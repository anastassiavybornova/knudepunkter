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
from shapely.geometry import Point
from src import graphedit

output_file = homepath + "/data/processed/workflow_steps/network_parallel_edges.gpkg"

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

# create unique id
edges["edge_id"] = edges.index
nodes["node_id"] = nodes.index

# Extract start and end coordinates of each linestring
first_coord = edges["geometry"].apply(lambda g: Point(g.coords[0]))
last_coord = edges["geometry"].apply(lambda g: Point(g.coords[-1]))

# Add start and end as columns to the gdf
edges["start_coord"] = first_coord
edges["end_coord"] = last_coord

start_coords = edges[["edge_id", "start_coord"]].copy()
start_coords.set_geometry("start_coord", inplace=True, crs=edges.crs)

end_coords = edges[["edge_id", "end_coord"]].copy()
end_coords.set_geometry("end_coord", inplace=True, crs=edges.crs)

# join start and end coors to nearest node
start_joined = start_coords.sjoin_nearest(
    nodes[["geometry", "node_id"]], how="left", distance_col="distance"
)
end_joined = end_coords.sjoin_nearest(
    nodes[["geometry", "node_id"]], how="left", distance_col="distance"
)

edges.drop(["start_coord", "end_coord"], axis=1, inplace=True)

# Merge with edges
edges = edges.merge(
    start_joined[["edge_id", "node_id"]], left_on="edge_id", right_on="edge_id"
)
edges.rename({"node_id": "u"}, inplace=True, axis=1)

edges = edges.merge(
    end_joined[["edge_id", "node_id"]], left_on="edge_id", right_on="edge_id"
)
edges.rename({"node_id": "v"}, inplace=True, axis=1)

# find edges with same start and end node (but could still be on different roads!)
edges["key"] = 0

edges = graphedit.find_parallel_edges(edges)

child_node_ids = nodes.loc[nodes.ismain == 0]["node_id"].to_list()

# Identify parallel edges on same roads that should be excluded from e.g. length computation
# Based on parent-child node classification
parallel_edges = []
grouped_edges = edges.groupby(["u", "v"])
assert len(grouped_edges) == len(edges.loc[edges.key == 0])

for nodes_ids, group in grouped_edges:
    if (
        nodes_ids[0] in child_node_ids
        and nodes_ids[1] in child_node_ids
        and len(group) > 1
    ):
        parallel_edges.append(group["length"].idxmin())

edges["parallel"] = 0
edges.loc[parallel_edges, "parallel"] = 1

assert len(edges.loc[edges.parallel == 1]) == len(parallel_edges)

# Export
edges.to_file(output_file)

# Remove temporary layers from project if they exist already
remove_existing_layers(["input edges", "input nodes", "parallel edges"])

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
        marker_size=4,
    )

    zoom_to_layer("input data")

if display_output:
    key_edges = QgsVectorLayer(
        output_file, "parallel edges (start and end nodes)", "ogr"
    )
    QgsProject.instance().addMapLayer(key_edges)

    draw_categorical_layer(
        "parallel edges (start and end nodes)", "key", alpha=180, line_style="dash"
    )

    parallel_edges = QgsVectorLayer(output_file, "parallel edges (same road)", "ogr")
    QgsProject.instance().addMapLayer(parallel_edges)

    draw_categorical_layer(
        "parallel edges (same road)", "parallel", alpha=180, line_style="solid"
    )

if display_input and display_output:
    group_layers(
        "Find parallel edges",
        [
            "input edges",
            "input nodes",
            "parallel edges (start and end nodes)",
            "parallel edges (same road)",
        ],
        remove_group_if_exists=True,
    )

if display_input == False and display_output == True:
    group_layers(
        "Find parallel edges",
        [
            "parallel edges (start and end nodes)",
            "parallel edges (same road)",
        ],
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
