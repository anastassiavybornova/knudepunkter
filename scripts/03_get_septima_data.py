### IMPORT all layers from "FACILITETER" WFS; keep info on *what* kind of facility it is

### CUSTOM SETTINGS
show_study_area = True


# import libraries
import os
import yaml
import geopandas as gpd
from random import randrange
from owslib.wfs import WebFeatureService
from src import plot_data
from processing.tools import dataobjects
from qgis.core import QgsFeatureRequest

# define paths
homepath = (
    QgsProject.instance().homePath()
)  # homepath variable (where is the qgis project saved?)
configfile = os.path.join(homepath, "config.yml")  # filepath of config file
output_path = os.path.join(homepath, "output_overlay.gpkg")  # filepath of config file
study_area_path = os.path.join(homepath, "data/raw/user_input/study_area.gpkg")

# load configs
configs = yaml.load(open(configfile), Loader=yaml.FullLoader)
proj_crs = configs["proj_crs"]

if show_study_area == True:
    # make vector layer of study area
    study_area_vlayer = QgsVectorLayer(study_area_path, "Study area", "ogr")
    QgsProject.instance().addMapLayer(study_area_vlayer)

study_area_path,
wfs_version = "1.1.0"
wfs_name = "wfs_data"
proj_crs = "EPSG:25832"
# geom_type = "Polygon"

study_area_gdf = gpd.read_file(study_area_path)

bounds = study_area_gdf.bounds
minx = bounds.minx[0]
miny = bounds.miny[0]
maxx = bounds.maxx[0]
maxy = bounds.maxy[0]

# TODO
wfs_layers = ["land_landskabnatur"]
wfs_layer = "land_landskabnatur"

# define WFS URL
wfs_core = f"https://rida-services.test.septima.dk/ows?MAP={wfs_layer}&service=WFS"

wfs_url_get = wfs_core + "&request=GetCapabilities"
wfs_get = WebFeatureService(url=wfs_url_get, version=wfs_version)
layers_to_import = list(wfs_get.contents)

print("Importing layers:", layers_to_import, "from WFS: ", wfs_layer)

wfs_dir = homepath + f"/data/raw/wfs/"

if not os.path.isdir(wfs_dir):
    os.mkdir(wfs_dir)

wfs_layer_dir = homepath + f"/data/raw/wfs/{wfs_layer}/"

if not os.path.isdir(wfs_layer_dir):
    os.mkdir(wfs_layer_dir)

for mylayer in layers_to_import:
    fp = wfs_layer_dir + mylayer + ".gpkg"

    print("Getting data for layer:", mylayer)

    wfs_url = (
        wfs_core
        + f"&request=GetFeature&typeName={mylayer}&SRSName=EPSG:25832&BBOX={minx},{miny},{maxx},{maxy}"
    )

    Source = f"pagingEnabled='true' preferCoordinatesForWfsT11='false' restrictToRequestBBOX='1' srsname={proj_crs} typename={mylayer} url={wfs_url} version='auto'"

    # initialize vector layer of WFS features
    temp_layer = QgsVectorLayer(Source, wfs_name, "WFS")

    fix_layer = processing.run(
        "native:fixgeometries", {"INPUT": temp_layer, "OUTPUT": "memory:"}
    )["OUTPUT"]

    clip_params = {
        "INPUT": fix_layer,
        "OVERLAY": study_area_vlayer,
        "OUTPUT": fp,  # "TEMPORARY_OUTPUT"
    }
    context = dataobjects.createContext()
    context.setInvalidGeometryCheck(QgsFeatureRequest.GeometryNoCheck)

    # clip to study area polygon
    clip_out = processing.run("native:clip", clip_params)
    # clip_out = processing.run("native:clip", clip_params, context=context)

    # current_layer = temp_clip_out["OUTPUT"]
    layer = QgsVectorLayer(fp, mylayer, "ogr")

    QgsProject.instance().addMapLayer(layer)
    print(f"Added {mylayer} layer")


# plot_data.visualize_categorical("wfs_data_MERGED", "Category")


# def add_wfs_layers(
#     wfs_core,
#     study_area_path,
#     wfs_version="1.1.0",
#     wfs_name="wfs_data",
#     proj_crs="EPSG:25832",
#     geom_type="Point",
# ):
#     study_area_gdf = gpd.read_file(study_area_path)

#     bounds = study_area_gdf.bounds
#     minx = bounds.minx[0]
#     miny = bounds.miny[0]
#     maxx = bounds.maxx[0]
#     maxy = bounds.maxy[0]

#     # define WFS URL
#     wfs_url_get = wfs_core + "&request=GetCapabilities"
#     wfs_get = WebFeatureService(url=wfs_url_get, version=wfs_version)
#     layers_to_import = list(wfs_get.contents)

#     print("Importing layers:", layers_to_import)

#     # create an empty QgsVectorLayer (for all wfs layers)
#     merged_wfs_name = wfs_name + "_MERGED"
#     new_layer = QgsVectorLayer(
#         f"{geom_type}?crs={proj_crs}&field=category:string", merged_wfs_name, "memory"
#     )

#     for mylayer in layers_to_import:
#         print("Getting data for layer:", mylayer)

#         wfs_url = (
#             wfs_core
#             + f"&request=GetFeature&typeName={mylayer}&SRSName=EPSG:25832&BBOX={minx},{miny},{maxx},{maxy}"
#         )

#         Source = f"pagingEnabled='true' preferCoordinatesForWfsT11='false' restrictToRequestBBOX='1' srsname={proj_crs} typename={mylayer} url={wfs_url} version='auto'"

#         # initialize vector layer of WFS features
#         temp_layer = QgsVectorLayer(Source, wfs_name, "WFS")

#         # clip to study area polygon
#         temp_clip_out = processing.run(
#             "native:clip",
#             {
#                 "INPUT": temp_layer,
#                 "OVERLAY": study_area_vlayer,
#                 "OUTPUT": "TEMPORARY_OUTPUT",
#             },
#         )

#         current_layer = temp_clip_out["OUTPUT"]

#         ### TO DO 1: MAKE THE ADDING OF FEATUES (BELOW) MORE EFFICIENT INSTEAD OF LOOPING THROUGH ALL FEATURES... if possible?
#         # make a list of all features of current layer, with mylayer (layer name) as attribute
#         ### TO DO 2: HOW CAN WE KEEP ALL ATTRIBUTES (there are different numbers of attributes for different layers)
#         ### and just *add* an attribute called "facility_type" where we keep the information on which WFS layer each feature comes from
#         ### (in the current version of the code, we don't keep any attributes, and create a separate attribute where we insert the layer name)

#         features_list = []
#         for feat in current_layer.getFeatures():
#             feature = QgsFeature()  # initialize feature
#             feature.setGeometry(feat.geometry())  # add geometries
#             feature.setAttributes([mylayer])  # add type name attribute
#             features_list.append(feature)
#         ## to add features, access data provider behind the layer with method addfeatures
#         new_layer.dataProvider().addFeatures(features_list)

#     return new_layer


# wfs_core = (
#     "https://rida-services.test.septima.dk/ows?map=facilit_faciliteter&service=WFS"
# )
# new_facilities_layer = add_wfs_layers(wfs_core, study_area_path)


# # add merged layer to map
# QgsProject.instance().addMapLayer(new_facilities_layer)
# print("Added merged facilities layer")


# unique_values = [
#     "rasteplads_suppl",
#     "infoservice_suppl",
#     "indkoeb",
#     "overnatning",
#     "rasteplads",
#     "infoservice",
# ]

# #plot_data.visualize_categorical("wfs_data_MERGED", "Category")
