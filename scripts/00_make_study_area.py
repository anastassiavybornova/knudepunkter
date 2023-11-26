
##### CUSTOM SETTINGS
display_studyarea = True # display the study area polygon? 

##### NO CHANGES BELOW THIS LINE
print("SCRIPT NAME started with user settings:")
print(f"\t * Display user-defined study area: {display_studyarea}")

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

# load configs
configfile = os.path.join(homepath, "config.yml")  # filepath of config file
configs = yaml.load(open(configfile), Loader=yaml.FullLoader)
proj_crs = configs["proj_crs"]  # projected CRS

# define location of municipality boundaries file
filepath_municipalities = homepath + "/data/raw/municipalities/muni_boundary.gpkg"
# define location of study area polygon (union of user-provided municipality polygons)
filepath_study = homepath + "/data/raw/user_input/study_area.gpkg"

### READ IN DATA
muni = gpd.read_file(filepath_municipalities)

# check list of municipalities for errors
for m in configs["municipalities"]:
    assert m in list(muni["kommunekode"]), f"\n Could not find the municipality code {m}. \n Please correct the municipality code in the config.yml file and run this script again!"

# if all kommunekode are correct, filter data set and save a copy
muni = muni[muni.kommunekode.isin(configs["municipalities"])].copy()
muni.to_file(filepath_study, index = False)
print(f"Study area layer saved to: {filepath_study}")

# set to projected CRS
QgsProject.instance().setCrs(QgsCoordinateReferenceSystem(proj_crs))


if display_studyarea == True:
    
    # import qgis-based plotting functions
    exec(open(homepath + "/src/plot_func.py").read())

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
    
print("SCRIPTNAME script ended succcessfully \n")