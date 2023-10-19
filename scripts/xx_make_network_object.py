##### TO DO: UPDATE - SHOULD USE COMMUNICATION LAYER AS INPUT!

# IS already almost a network object - use start and end nodes in edge geodataframe

### Script for converting preprocessed beta data to network/graph format

### *********
### CUSTOM SETTINGS
### *********

display_intermediate_data = True
display_network_layer = True

### NO CHANGES BELOW THIS LINE

### *********
### Functions
### *********

# define homepath variable (where is the qgis project saved?)
homepath = QgsProject.instance().homePath()
exec(open(homepath + "/src/plot_func.py").read())

# ### *********
# ### Step 2: data>network with python tools
# ### *********

# import packages
import src.graphedit as graphedit
import geopandas as gpd
import osmnx as ox
import networkx as nx
import pandas as pd
import os
import yaml

from qgis.core import *

# load configs
configfile = os.path.join(homepath, "config.yml")  # filepath of config file
configs = yaml.load(open(configfile), Loader=yaml.FullLoader)
proj_crs = configs["proj_crs"]


# INPUT/OUTPUT FILE PATHS
input_file = homepath + "/data/processed/workflow_steps/qgis_output_beta.gpkg"
output_file = homepath + "/data/processed/workflow_steps/G_beta.json"
edgefile = homepath + "/data/processed/workflow_steps/edges_beta.gpkg"
nodefile = homepath + "/data/processed/workflow_steps/nodes_beta.gpkg"

# Remove temporary layers from project if they exist already
remove_existing_layers(["network input data", "Edges", "Nodes"])

# input data
input_layer = QgsVectorLayer(input_file, "network input data", "ogr")

if display_intermediate_data:
    QgsProject.instance().addMapLayer(input_layer)
    draw_recent_simple_line_layer(color="purple", width=0.5)
    zoom_to_layer("network input data")

# import cleaned data
gdf = gpd.read_file(input_file)
if gdf.crs != proj_crs:
    gdf = gdf.to_crs(proj_crs)

# Convert to network structure

# OBS: If problems arise here, look into edges of length 0 or edge linestring geometries

# Create data with LineStrings only defined by end and start coordinate
gdf["osmid"] = gdf.index
gdf = graphedit.unzip_linestrings(gdf, "osmid")
gdf = gdf[gdf.geometry.length != 0.0]

gdf["osmid"] = gdf.index
G = graphedit.create_osmnx_graph(gdf)
G_simp = ox.simplify_graph(G)
G_final = ox.get_undirected(G_simp)
nodes, edges = ox.graph_to_gdfs(G_final)


# Check number of components and degree
print(f"The graph has {len([c for c in nx.connected_components(G_final)])} components")

print("Degrees:", nx.degree_histogram(G_final))

# Save component number to edges
comps = [c for c in nx.connected_components(G_final)]

edges["component"] = None

for i, comp in enumerate(comps):
    index_list = list(G_final.edges(comp))

    for index in index_list:
        try:
            edges.loc[index, "component"] = i + 1  # start counting at 1
        except KeyError:
            edges.loc[(index[1], index[0]), "component"] = i + 1  # start counting at 1

# rename component nr 1 (the biggest one) into "LCC"
edges.loc[edges["component"] == 1, "component"] = "LCC"

assert len(edges.component.unique()) == len(comps)
assert len(edges.loc[edges.component.isna()]) == 0

# Save degrees to nodes
pd_degrees = pd.DataFrame.from_dict(
    dict(G_final.degree), orient="index", columns=["degree"]
)
nodes = nodes.merge(pd_degrees, left_index=True, right_index=True)

# Export
ox.save_graphml(G_final, output_file)
edges[["geometry", "component"]].to_file(edgefile)
nodes[["x", "y", "degree", "geometry"]].to_file(nodefile)


# display in QGIS
if display_network_layer:
    vlayer_edges = QgsVectorLayer(edgefile, "Edges (beta)", "ogr")
    if not vlayer_edges.isValid():
        print("Layer failed to load!")
    else:
        QgsProject.instance().addMapLayer(vlayer_edges)

    vlayer_nodes = QgsVectorLayer(nodefile, "Nodes (beta)", "ogr")
    if not vlayer_nodes.isValid():
        print("Layer failed to load!")
    else:
        QgsProject.instance().addMapLayer(vlayer_nodes)
        draw_simple_point_layer("Nodes (beta)", marker_size=2)

    draw_categorical_layer("Edges (beta)", "component", line_width=1)
    draw_categorical_layer("Nodes (beta)", "degree", marker_size=3)


if display_intermediate_data == False and display_network_layer == True:
    group_layers(
        "Make Beta Network",
        ["Edges (beta)", "Nodes (beta)"],
        remove_group_if_exists=True,
    )

if display_preprocessed_layer == True and display_network_layer == False:
    group_layers(
        "Make Beta Network",
        ["network input data"],
        remove_group_if_exists=True,
    )

if display_intermediate_data == True and display_network_layer == True:
    group_layers(
        "Make Beta Network",
        ["network input data", "Edges (beta)", "Nodes (beta)"],
        remove_group_if_exists=True,
    )
