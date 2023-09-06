### Script that converts beta DATA into a beta NETWORK - to be updated!
### currently has 2 steps: 1. preprocess (snap etc.) and 2. convert to network (using nx tools)

# TODO

### *********
### CUSTOM SETTINGS
display_intermediate_data = True  # TODO
display_preprocessed_layer = True
display_network_layer = True
mytolerance = 5  # distance threshold for when to snap objects (in meters)
mybehaviour = 6  # end point to end point
mybehaviour_verbose = "end point to end point"

### NO CHANGES BELOW THIS LINE

# import packages
import os

os.environ["USE_PYGEOS"] = "0"
import geopandas as gpd
from src import plot_func

# import src.graphedit as graphedit
from PyQt5.QtCore import QVariant

# define homepath variable (where is the qgis project saved?)
homepath = QgsProject.instance().homePath()

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


### *********
### Step 1: preprocess data with qgis methods
### *********

# INPUT/OUTPUT FILE PATHS
myinputfile = homepath + "/data/processed/workflow_steps/qgis_input_beta.gpkg"
myoutputfile = homepath + "/data/processed/workflow_steps/qgis_output_beta.gpkg"

# Remove temporary layers from project if they exist already
existing_layers_ids = [
    layer.id() for layer in QgsProject.instance().mapLayers().values()
]

remove_layers = [
    e
    for e in existing_layers_ids
    if e.startswith(("Valid", "Split", "Snapped", "input_"))
]

for r in remove_layers:
    QgsProject.instance().removeMapLayer(r)

# TEMP - load input data
org_input = QgsVectorLayer(myinputfile, "input_data", "ogr")

if display_intermediate_data:
    QgsProject.instance().addMapLayer(org_input)

    draw_recent_simple_line_layer(color="blue", width=0.5)


# Run processing algorithm "split with lines"
temp_out_split = processing.run(
    "native:splitwithlines",
    {"INPUT": myinputfile, "LINES": myinputfile, "OUTPUT": "TEMPORARY_OUTPUT"},
)
print("done: split with lines")

if display_intermediate_data:
    QgsProject.instance().addMapLayer(temp_out_split["OUTPUT"])
    draw_recent_simple_line_layer(color="red", width=0.7)

# snap
temp_out_snap = processing.run(
    "native:snapgeometries",
    {
        "INPUT": temp_out_split["OUTPUT"],
        "REFERENCE_LAYER": temp_out_split["OUTPUT"],
        "TOLERANCE": mytolerance,
        "BEHAVIOR": mybehaviour,
        "OUTPUT": "TEMPORARY_OUTPUT",
    },
)
print(f"done: snapped with tolerance {mytolerance}, behaviour: '{mybehaviour_verbose}'")

if display_intermediate_data:
    QgsProject.instance().addMapLayer(temp_out_snap["OUTPUT"])
    draw_recent_simple_line_layer(color="orange", width=0.7)

# Check validity
temp_out_validity = processing.run(
    "qgis:checkvalidity",
    {
        "INPUT_LAYER": temp_out_snap["OUTPUT"],
        "METHOD": 2,
        "IGNORE_RING_SELF_INTERSECTION": False,
        "VALID_OUTPUT": "TEMPORARY_OUTPUT",
        "INVALID_OUTPUT": homepath + "/data/invalid.gpkg",  # None,
        "ERROR_OUTPUT": None,
    },
)
print("done: validity check")


if display_intermediate_data:
    QgsProject.instance().addMapLayer(temp_out_validity["VALID_OUTPUT"])
    draw_recent_simple_line_layer(color="blue", width=0.7)


# Delete linestrings of just 1 point
vlayer = temp_out_validity["VALID_OUTPUT"]
layer_provider = vlayer.dataProvider()

# add a "mylength" colum to the attribute table
layer_provider.addAttributes([QgsField("new_length", QVariant.Double)])
field_idx = vlayer.fields().indexOf("new_length")

if field_idx == -1:
    field_idx = len(vlayer.fields())
vlayer.updateFields()

# fill "length" column with length values
vlayer.startEditing()
for f in vlayer.getFeatures():
    id = f.id()
    length = f.geometry().length()
    attr_value = {field_idx: length}
    layer_provider.changeAttributeValues({id: attr_value})
vlayer.commitChanges()

# # find strings with length 0
# expression = "mylength = 0"
# request = QgsFeatureRequest().setFilterExpression(expression)
# matches = []
# for f in vlayer.getFeatures(request):
#     matches.append(f["fid"])

# # erase length 0 strings
# if vlayer.dataProvider().capabilities() & QgsVectorDataProvider.DeleteFeatures:
#     print("layer supports deletion")
#     res = vlayer.dataProvider().deleteFeatures(matches)

# # delete "mylength" field
# vlayer.dataProvider().deleteAttributes([0, 2])

# print("done: delete linestrings with length 0")

# # export
# _ = processing.run(
#     "native:package",
#     {
#         "LAYERS": vlayer,
#         "OUTPUT": myoutputfile,
#         "OVERWRITE": True,
#         "SAVE_STYLES": False,
#         "SAVE_METADATA": True,
#         "SELECTED_FEATURES_ONLY": False,
#         "EXPORT_RELATED_LAYERS": False,
#     },
# )

# print(f"done: save to {myoutputfile}")

# if display_preprocessed_layer == True:
#     vlayer = QgsVectorLayer(myoutputfile, "Beta data (post-network)", "ogr")
#     if not vlayer.isValid():
#         print("Layer failed to load!")
#     else:
#         QgsProject.instance().addMapLayer(vlayer)

# ### *********
# ### Step 2: data>network with python tools
# ### *********

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
