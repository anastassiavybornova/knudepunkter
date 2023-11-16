# TODO: insert script description

##### NO CHANGES BELOW THIS LINE
print("00_make_polygon script started")

# define study area to be used
# (will later be user-provided polygon; here random choice
# of 1 of 3 study areas)

# import libraries
import os
import geopandas as gpd
import pandas as pd
import random
import yaml
import sys

random.seed(22)

# define homepath variable (where is the qgis project saved?)
homepath = QgsProject.instance().homePath()

# define homepath variable (where is the qgis project saved?)
homepath = QgsProject.instance().homePath()

# add project path to PATH
sys.path.append(homepath)

# load configs
configfile = os.path.join(homepath, "config.yml")  # filepath of config file
configs = yaml.load(open(configfile), Loader=yaml.FullLoader)
proj_crs = configs["proj_crs"]

# read in latest folkersma data set
gdf = gpd.read_file(
    homepath
    + "/data/raw/folkersma_digital/2023-08-01 Cycling network Denmark shapefiles/stretch.shp"
)

# convert to projected crs
gdf = gdf.to_crs(proj_crs)

# buffer and merge
polys = gdf.buffer(500).unary_union

# convex hull polygons for each region
polys = [p.convex_hull for p in polys.geoms]

# randomly select one (determined by random.seed)
my_poly = random.choice(polys)

# make sure there's the user_input folder
os.makedirs(homepath + "/data/raw/user_input/", exist_ok=True)

# save as gpkg (to be used by 01_define_area)
gpd.GeoDataFrame(geometry=[my_poly], crs=gdf.crs).to_file(
    homepath + "/data/raw/user_input/study_area.gpkg", index=False
)

print("Study area polygon saved")
print("00_make_polygon script ended successfully")