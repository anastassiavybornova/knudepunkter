### Script for converting preprocessed beta data to network/graph format

### *********
### CUSTOM SETTINGS
### *********


### NO CHANGES BELOW THIS LINE

### *********
### Functions
### *********


def draw_recent_simple_line_layer(color="purple", width=0.7, line_style="solid"):
    symbol = QgsLineSymbol.createSimple(
        {"color": color, "width": width, "line_style": line_style}
    )
    renderer = QgsSingleSymbolRenderer(symbol)
    iface.activeLayer().setRenderer(renderer)
    iface.activeLayer().triggerRepaint()
    iface.layerTreeView().refreshLayerSymbology(iface.activeLayer().id())


# ### *********
# ### Step 2: data>network with python tools
# ### *********

# import packages
from qgis.analysis import *

# define homepath variable (where is the qgis project saved?)
homepath = QgsProject.instance().homePath()

director = QgsVectorLayerDirector(
    vectorLayer,
    directionFieldId,
    directDirectionValue,
    reverseDirectionValue,
    bothDirectionValue,
    defaultDirection,
)

# import src.graphedit as graphedit
# from PyQt5.QtCore import QVariant

# # import cleaned data
# gdf = gpd.read_file(homepath + "/data/processed/workflow_steps/qgis_output_beta.gpkg")
# proj_crs = gdf.crs
# print("proj_crs: ", proj_crs)

# # make graph from data
# G = graphedit.get_graph_from_gdf(gdf)

# # where to save
# filepath_to = homepath + "/data/processed/workflow_steps/G_beta.json"

# # save to json
# graphedit.spatialgraph_tojson(G, proj_crs, filepath_to)

# del G

# # import back (to check if it worked)
# G = graphedit.spatialgraph_fromjson(filepath_to)

# # for plotting, save nodes and edges with component / degree information
# nodes = graphedit.get_node_gdf(G, return_degrees=True)
# mynodefile = homepath + "/data/processed/workflow_steps/nodes_beta.gpkg"
# nodes[["geometry", "degree"]].to_file(mynodefile, index=False)

# edges = graphedit.get_edge_gdf(G, return_components=True)
# myedgefile = homepath + "/data/processed/workflow_steps/edges_beta.gpkg"
# edges[["geometry", "component_nr"]].to_file(myedgefile, index=False)

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
