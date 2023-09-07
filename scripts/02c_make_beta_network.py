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


# INPUT/OUTPUT FILE PATHS
input_file = homepath + "/data/processed/workflow_steps/qgis_output_beta.gpkg"
output_file = homepath + "/data/processed/workflow_steps/G_beta.json"
edgefile = homepath + "/data/processed/workflow_steps/edges_beta.gpkg"
nodefile = homepath + "/data/processed/workflow_steps/nodes_beta.gpkg"

# Remove temporary layers from project if they exist already
remove_existing_layers(("input"))

# input data
input_layer = QgsVectorLayer(input_file, "input data", "ogr")

if display_intermediate_data:
    QgsProject.instance().addMapLayer(input_layer)
    draw_recent_simple_line_layer(color="purple", width=0.5)


# input_file = "../data/processed/workflow_steps/qgis_output_beta.gpkg"
# output_file = "../data/processed/workflow_steps/G_beta.json"
# nodefile = "../data/processed/workflow_steps/nodes_beta.gpkg"
# edgefile = "../data/processed/workflow_steps/edges_beta.gpkg"

# import cleaned data
gdf = gpd.read_file(input_file)
proj_crs = gdf.crs
print("proj_crs: ", proj_crs)

# Convert to network structure

# OBS: If problems arise here, look into edges of length 0 or edge linestring geometries

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
            edges.loc[index, "component"] = i
        except KeyError:
            edges.loc[(index[1], index[0]), "component"] = i

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

# Plot
if display_network_layer:
    pass

# # make graph from data
# G = graphedit.get_graph_from_gdf(gdf)


# # save to json
# graphedit.spatialgraph_tojson(G, proj_crs, output_file)

# del G

# # import back (to check if it worked)
# G = graphedit.spatialgraph_fromjson(output_file)
#

# # for plotting, save nodes and edges with component / degree information
# nodes = graphedit.get_node_gdf(G, return_degrees=True)
# # mynodefile = "../data/processed/workflow_steps/nodes_beta.gpkg"
# mynodefile = homepath + "/data/processed/workflow_steps/nodes_beta.gpkg"
# nodes[["geometry", "degree"]].to_file(mynodefile, index=False)

# edges = graphedit.get_edge_gdf(G, return_components=True)
# # myedgefile = "../data/processed/workflow_steps/edges_beta.gpkg"
# myedgefile = homepath + "/data/processed/workflow_steps/edges_beta.gpkg"
# edges[["geometry", "component_nr"]].to_file(myedgefile, index=False)

#
# # display in QGIS
# if display_network_layer == True:
#     vlayer_edges = QgsVectorLayer(myedgefile, "Edges (beta)", "ogr")
#     if not vlayer_edges.isValid():
#         print("Layer failed to load!")
#     else:
#         QgsProject.instance().addMapLayer(vlayer_edges)

#     vlayer_nodes = QgsVectorLayer(mynodefile, "Nodes (beta)", "ogr")
#     if not vlayer_nodes.isValid():
#         print("Layer failed to load!")
#     else:
#         QgsProject.instance().addMapLayer(vlayer_nodes)

# # TO DO: automatically categorize : cf. https://docs.qgis.org/3.28/en/docs/pyqgis_developer_cookbook/vector.html#categorized-symbol-renderer
# # e.g. in here: https://gist.github.com/sylsta/0c182ec53b590b6c6e5e272db9674936
