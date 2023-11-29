# In this script, we:
# - get the user-defined study area polygon
# - get the input data and cut it to the study area
# - preprocess the input data to create the technical layer
# - save the technical layer to a subfolder
# - optional (if requested by user):
#   display study area; input data; and technical layer
# the technical layer will be used ONLY FOR PLOTTING by future scripts

##### CUSTOM SETTINGS
display_inputdata = (
    True  # display the study area polygon and the entire Folkersma data set?
)
display_technicallayer = True  # display the technical layer of edges?

##### NO CHANGES BELOW THIS LINE
print("01a_make_technical_layer script started with user settings:")
print(f"\t * Display input data: {display_inputdata}")
print(f"\t * Display technical layer: {display_technicallayer}")

### SETUP

# define homepath variable (where is the qgis project saved?)
homepath = QgsProject.instance().homePath()

# add project path to PATH
import sys

if homepath not in sys.path:
    sys.path.append(homepath)

# import python packages
import os

os.environ["USE_PYGEOS"] = "0"  # pygeos/shapely2.0/osmnx conflict solving
import geopandas as gpd
import yaml
from qgis.core import *

# import qgis-based plotting functions
exec(open(homepath + "/src/plot_func.py").read())

# load configs
configfile = os.path.join(homepath, "config.yml")  # filepath of config file
configs = yaml.load(open(configfile), Loader=yaml.FullLoader)
proj_crs = configs["proj_crs"]  # projected CRS
dataforsyning_token = configs["dataforsyning_token"]

print("done: setup")

### PATHS

# make folders for results (if they don't exist yet)
os.makedirs(homepath + "/data/processed/workflow_steps", exist_ok=True)

# define paths to input files
node_inpath = (homepath + "/data/raw/network/nodes.gpkg")
edge_inpath = (homepath + "/data/raw/network/edges.gpkg")

# define paths to output files
nodetech_outpath = homepath + "/data/processed/workflow_steps/nodes_technical.gpkg"
edgetech_outpath = homepath + "/data/processed/workflow_steps/edges_technical.gpkg"

# define location of study area polygon (user-provided)
filepath_study = homepath + "/data/user_input/study_area.gpkg"

print("done: paths")

### STUDY AREA

# read in study area polygon provided by the user
study_area = gpd.read_file(filepath_study)
study_area = study_area.to_crs(proj_crs)

# Remove layers from project if they exist already
remove_existing_layers(["Study area", "beta data (pre-network)"])

print("done: study area")

### READ IN INPUT DATA (BETA NETWORK FROM FOLKERSMA)

nodes = gpd.read_file(node_inpath)
nodes = nodes.to_crs(proj_crs)

edges = gpd.read_file(edge_inpath)
edges = edges.to_crs(proj_crs)

print("done: input data")

### LIMIT INPUT DATA TO STUDY AREA EXTENT

assert nodes.crs == study_area.crs
assert edges.crs == study_area.crs

# only keep those nodes and edges that are within the study area
nodes = nodes[nodes.intersects(study_area.loc[0, "geometry"])].copy()
nodes.reset_index(drop=True, inplace=True)

edges = edges[edges.intersects(study_area.loc[0, "geometry"])].copy()
edges.reset_index(drop=True, inplace=True)

print("done: limit to study area")

### PROCESS NODE & EDGE DATA

# remove empty geometries
edges = edges[edges.geometry.notna()].reset_index(drop=True)
nodes = nodes[nodes.geometry.notna()].reset_index(drop=True)

# assert there is one (and only one) LineString per edge geometry row
nodes = nodes.explode(index_parts=False).reset_index(drop=True)
assert all(nodes.geometry.type == "Point")
assert all(nodes.geometry.is_valid)

# assert there is one (and only one) Point per node geometry row
edges = edges.explode(index_parts=False).reset_index(drop=True)
assert all(edges.geometry.type == "LineString")
assert all(edges.geometry.is_valid)

# project to projected crs
nodes.to_crs(proj_crs, inplace=True)
edges.to_crs(proj_crs, inplace=True)

print("done: process data")

### SAVE TECHNICAL NODE AND EDGE DATA TO FILE
# these are the "technical data" layers that will be used by all consecutive scripts FOR PLOTTING
nodes.to_file(nodetech_outpath)
edges.to_file(edgetech_outpath)
print(f"Technical data layer for nodes in study area saved to: {nodetech_outpath}")
print(f"Technical data layer for edges in study area saved to: {edgetech_outpath}")


### IF REQUESTED BY USER, DISPLAY LAYERS

remove_existing_layers(["Study area", "Input data", "Technical network", "Basemap"])

QgsProject.instance().setCrs(QgsCoordinateReferenceSystem(proj_crs))

# input data (entire raw data set from folkersma and study area)
if display_inputdata == True:
    sa_layer = QgsVectorLayer(filepath_study, "Study area", "ogr")
    if not sa_layer.isValid():
        print("Study area layer failed to load!")
    else:
        QgsProject.instance().addMapLayer(sa_layer)
        draw_simple_polygon_layer(
            "Study area",
            color="250,181,127,128",
            outline_color="black",
            outline_width=0.5,
        )

    input_layer = QgsVectorLayer(edge_inpath, "Input data", "ogr")
    if not input_layer.isValid():
        print("Layer failed to load!")
    else:
        QgsProject.instance().addMapLayer(input_layer)
        draw_recent_simple_line_layer(color="green", width=0.7, line_style="dash")


# output data (folkersma data cut to study area and cleaned)
if display_technicallayer == True:
    tech_layer = QgsVectorLayer(edgetech_outpath, "Technical network", "ogr")
    if not tech_layer.isValid():
        print("Layer failed to load!")
    else:
        QgsProject.instance().addMapLayer(tech_layer)
        draw_recent_simple_line_layer(color="blue", width=0.7, line_style="solid")


if display_inputdata and display_technicallayer:
    group_layers(
        group_name="Make technical network layer",
        layer_names=["Study area", "Input data", "Technical network"],
    )

    zoom_to_layer("Study area")

if display_inputdata == True and display_technicallayer == False:
    group_layers(
        group_name="Make technical network layer",
        layer_names=["Study area", "Input data"],
    )

    zoom_to_layer("Study area")

if display_inputdata == False and display_technicallayer == True:
    group_layers(
        group_name="Make technical network layer", layer_names=["Technical network"]
    )

    zoom_to_layer("Technical network")


if dataforsyning_token and (display_inputdata or display_technicallayer):
    basemap_name = "topo_skaermkort_daempet"
    url = f"https://api.dataforsyningen.dk/{basemap_name}_DAF?service%3DWMTS%26request%3DGetCapabilities%26token%3D{dataforsyning_token}"
    source = f"crs={proj_crs}&dpiMode=7&format=image/jpeg&layers={basemap_name}&styles=default&tileMatrixSet=View1&tilePixelRatio=0&url={url}"
    basemap = QgsRasterLayer(source, "Basemap", "wms")

    QgsProject.instance().addMapLayer(basemap, False)

    root = QgsProject.instance().layerTreeRoot()

    root.insertLayer(-1, basemap)

print("01a_make_technical_layer script ended successfully \n")