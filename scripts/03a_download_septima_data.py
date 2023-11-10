### IMPORT all WFS layers

## PLEASE NOTE: This script will take a while to run (5+ minutes)

### CUSTOM SETTINGS
show_layers = False

##### NO CHANGES BELOW THIS LINE
print("03a_download_septima_data script started with user settings:")
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
wfs_list = configs["wfs_list"]  # defining layers to import

# make vector layer of study area
study_area_vlayer = QgsVectorLayer(study_area_path, "Study area", "ogr")

if show_layers == True:
    QgsProject.instance().addMapLayer(study_area_vlayer)
    draw_simple_polygon_layer(
        "Study area",
        color="250,181,127,128",
        outline_color="black",
        outline_width=0.5,
    )
    zoom_to_layer("Study area")

# WFS settings
wfs_version = "1.1.0"

# get bounds for study area
study_area_gdf = gpd.read_file(study_area_path)
bounds = wfs_func.get_bounds(study_area_gdf)


for wfs_name in wfs_list:
    # define WFS URL
    wfs_core = f"https://rida-services.test.septima.dk/ows?map={wfs_name}&service=WFS"
    try:
        wfs_func.get_wfs_layers(
            study_area_vlayer,
            bounds,
            wfs_core,
            wfs_name,
            wfs_version,
            homepath,
            proj_crs,
        )

        # add layers to QGIS project
        if show_layers == True:
            wfs_folder = homepath + f"/data/raw/wfs/{wfs_name}/"

            files = os.listdir(wfs_folder)

            layernames = [f.strip(".gpkg") for f in files]

            for f, l in zip(files, layernames):
                new_layer = QgsVectorLayer(wfs_folder + f, l, "ogr")
                QgsProject.instance().addMapLayer(new_layer)
                print(f"Added layer {l}")
    except:
        print(f"Error when fetching {wfs_name}")

print("Layers fetched and saved.")
# for some reason, there are two wfs layers from land_landskabnatur that don't get downloaded:
# værdifulde landskaber and fredninger

print("03a_download_septima_data script ended successfully")
