### IMPORT all WFS layers

### CUSTOM SETTINGS
show_layers = True


# import libraries
import os
import yaml
import geopandas as gpd
from owslib.wfs import WebFeatureService
from src import wfs_func


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
wfs_list = configs["wfs_list"]

# make vector layer of study area
study_area_vlayer = QgsVectorLayer(study_area_path, "Study area", "ogr")

if show_layers == True:
    QgsProject.instance().addMapLayer(study_area_vlayer)

wfs_version = "1.1.0"

study_area_gdf = gpd.read_file(study_area_path)

bounds = wfs_func.get_bounds(study_area_gdf)

# wfs_list = ["land_landskabnatur", "vej_type"]
# wfs_list = ["land_landskabnatur"]
# wfs_list = ["vej_type"]


for wfs_name in wfs_list:
    # define WFS URL
    wfs_core = f"https://rida-services.test.septima.dk/ows?MAP={wfs_name}&service=WFS"

    wfs_func.get_wfs_layers(
        study_area_vlayer,
        bounds,
        wfs_core,
        wfs_name,
        wfs_version,
        homepath,
        proj_crs,
    )

    wfs_folder = homepath + f"/data/raw/wfs/{wfs_name}/"

    files = os.listdir(wfs_folder)

    layernames = [f.strip(".gpkg") for f in files]

    for f, l in zip(files, layernames):
        new_layer = QgsVectorLayer(wfs_folder + f, l, "ogr")
        QgsProject.instance().addMapLayer(new_layer)
        print(f"Added layer {l}")
