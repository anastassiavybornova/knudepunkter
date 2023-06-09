### CUSTOM SETTINGS
display_layer = True
### NO CHANGES BELOW THIS LINE

# import python libraries
import src.graphedit
import os
os.environ['USE_PYGEOS'] = '0'
import geopandas as gpd
import shapely
from shapely.geometry import Point
from shapely.wkt import loads, dumps
import momepy
import networkx as nx
from collections import Counter

# define homepath variable (where is the qgis project saved?)
homepath = QgsProject.instance().homePath()

# import cleaned data
gdf = gpd.read_file(homepath + "/data/processed/workflow_steps/qgis_output_concept.gpkg")
proj_crs = gdf.crs
print("proj_crs: ", proj_crs)

# make graph from data
G = src.graphedit.get_graph_from_gdf(gdf)

# where to save
filepath_to = homepath + "/data/processed/workflow_steps/G_concept.json"

# save to json
src.graphedit.spatialgraph_tojson(G, proj_crs, filepath_to)

del(G)

# import back (to check if it worked)
G = src.graphedit.spatialgraph_fromjson(filepath_to)

# for plotting, save nodes and edges with component / degree information
nodes = src.graphedit.get_node_gdf(G, return_degrees = True)
mynodefile = homepath + "/data/processed/workflow_steps/nodes_concept.gpkg"
nodes[["geometry", "degree"]].to_file(mynodefile, index = False)

edges = src.graphedit.get_edge_gdf(G, return_components = True)
myedgefile = homepath + "/data/processed/workflow_steps/edges_concept.gpkg"
edges[["geometry", "component_nr"]].to_file(myedgefile, index = False)

# display in QGIS
if display_layer == True:

    vlayer_edges = QgsVectorLayer(myedgefile, "Edges (concept)", "ogr")
    if not vlayer_edges.isValid():
        print("Layer failed to load!")
    else:
        QgsProject.instance().addMapLayer(vlayer_edges)

    vlayer_nodes = QgsVectorLayer(mynodefile, "Nodes (concept)", "ogr")
    if not vlayer_nodes.isValid():
        print("Layer failed to load!")
    else:
        QgsProject.instance().addMapLayer(vlayer_nodes)

# TO DO: automatically categorize : cf. https://docs.qgis.org/3.28/en/docs/pyqgis_developer_cookbook/vector.html#categorized-symbol-renderer
# e.g. in here: https://gist.github.com/sylsta/0c182ec53b590b6c6e5e272db9674936 