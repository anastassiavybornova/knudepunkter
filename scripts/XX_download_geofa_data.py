### IMPORT GEOFA DATA

### CUSTOM SETTINGS
show_layers = True

##### NO CHANGES BELOW THIS LINE
print("XX_download_geofa_data script started with user settings:")
print(f"Show layers: {show_layers}")

# define homepath variable (where is the qgis project saved?)
homepath = QgsProject.instance().homePath()

# add project path to PATH
import sys
if homepath not in sys.path:
    sys.path.append(homepath)

# import libraries
import os
import yaml
import geopandas as gpd
from owslib.wfs import WebFeatureService
from src import wfs_func

# define paths
configfile = os.path.join(homepath, "config.yml")  # filepath of config file
output_path = os.path.join(homepath, "output_overlay.gpkg")  # filepath of config file
study_area_path = os.path.join(homepath, "data/raw/user_input/study_area.gpkg")

# import functions
exec(open(homepath + "/src/plot_func.py").read())

# load configs
configs = yaml.load(open(configfile), Loader=yaml.FullLoader)
proj_crs = configs["proj_crs"]
wfs_list = configs["wfs_list"]

# Remove layers from project if they exist already
remove_existing_layers(["Study area", "geofa_test"])  # TODO: ADD NAME OF WFS LAYER HERE

# make vector layer of study area
study_area_vlayer = QgsVectorLayer(study_area_path, "Study area", "ogr")

if show_layers == True:
    QgsProject.instance().addMapLayer(study_area_vlayer)
    draw_simple_polygon_layer(
        "Study area", color="250,181,127,128", outline_color="black", outline_width=0.5
    )
    zoom_to_layer("Study area")

# define configurations for WFS connection
wfs_version = "2.0.0"
wfs_url = "https://geofa.geodanmark.dk/ows/fkg/fkg"
layer = "fkg:fkg.t_5802_fac_li"  # "fkg:fkg.linjer"
layer_name = "geofa_test"

source = f"pagingEnabled='true' preferCoordinatesForWfsT11='false' restrictToRequestBBOX='1' srsname={proj_crs} typename={layer} url={wfs_url} version='auto'"

# get WFS layer
temp_layer = QgsVectorLayer(source, layer_name, "WFS")

# fix geometries
fixed_layer = wfs_func.fix_geometries(temp_layer)

# settings for where to save data (make new folder)
wfs_dir = homepath + f"/data/raw/wfs/"

if not os.path.isdir(wfs_dir):
    os.mkdir(wfs_dir)

wfs_layer_dir = homepath + f"/data/raw/wfs/geofa/"

if not os.path.isdir(wfs_layer_dir):
    os.mkdir(wfs_layer_dir)

filepath = wfs_layer_dir + layer_name + ".gpkg"

# clip layer to study area extent
wfs_func.clip_save_layer(
    input_layer=fixed_layer,
    study_area_vlayer=study_area_vlayer,
    filepath=filepath,
    layer_name=layer_name,
)

# add layers to QGIS project
if show_layers == True:
    new_layer = QgsVectorLayer(filepath, layer_name, "ogr")
    QgsProject.instance().addMapLayer(new_layer)
    draw_recent_simple_line_layer(color="purple", width=0.7, line_style="dash")
    print(f"Added layer {layer_name}")

    group_layers("Get GeoFa Data", [layer_name], remove_group_if_exists=True)

print("XX_download_geofa_data script ended successfully")