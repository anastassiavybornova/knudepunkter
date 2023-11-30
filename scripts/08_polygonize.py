# DESCRIBE SCRIPT

##### CUSTOM SETTINGS
display_polygons = True

##### NO CHANGES BELOW THIS LINE
print("07_polygonize script started with user settings:")
print(f"Display polygons: {display_polygons}")

### SETUP

# define homepath variable (where is the qgis project saved?)
homepath = QgsProject.instance().homePath()

# add project path to PATH
import sys

if homepath not in sys.path:
    sys.path.append(homepath)

# import python packages
import os

os.environ["USE_PYGEOS"] = "0"
import geopandas as gpd
import shapely
import geopandas as gpd
from qgis.core import *
import json

# load configs
configfile = os.path.join(homepath, "config.yml")  # filepath of config file
configs = yaml.load(open(configfile), Loader=yaml.FullLoader)
proj_crs = configs["proj_crs"]  # projected CRS

### PATHS

# input filepath
input_file = homepath + "/data/processed/workflow_steps/network_edges_no_parallel.gpkg"
output_file = homepath + "/data/processed/workflow_steps/loop_polygons.gpkg"
results_path = homepath + "/results/data/"  # store output geopackages here
stats_path = homepath + "/results/stats/" # store output json here

### LOAD INPUT DATA AND PROJECT
gdf = gpd.read_file(input_file)
gdf = gdf.to_crs(proj_crs)

### POLYGONIZE LINESTRINGS

polygons = gpd.GeoSeries(
    shapely.polygonize(  # polygonize
        shapely.node(  # ensure properly nodded non-planar interesections
            shapely.GeometryCollection(  # need a single geometry for nodding
                gdf.geometry.array
            )
        ).geoms  # get parts of the collection from nodding
    ).geoms,  # get parts of the collection from polygonize
    crs=gdf.crs,
).explode(
    ignore_index=True
)  # shoudln't be needed but doesn't hurt to ensure

# Store geometries as a GeoDataFrame
polygons = gpd.GeoDataFrame(geometry=polygons)

# Ensure all polygons are valid. Should not be necessary.
if not polygons.is_valid.all():
    polygons = gpd.GeoDataFrame(
        geometry=gpd.GeoSeries(
            shapely.make_valid(polygons.geometry.array), crs=gdf.crs
        ).explode(ignore_index=True)
    )

# Ensure that all geometries are polygons
if not (polygons.geom_type == "Polygon").all():
    polygons = polygons[polygons.geom_type == "Polygon"].reset_index(drop=True)

# add a column with the area
polygons["polygon_area"] = polygons.area

### EXPORT RESULTS TO GPKG

polygons.to_file(output_file, index=False)

print(f"Polygons exported to {output_file}!")

### Summary statistics of polygonization
res = {} # initialize stats results dictionary
res["polygon_areas"] = list(polygons["polygon_area"])
with open(f"{stats_path}stats_polygons.json", "w") as opened_file: 
    json.dump(res, opened_file, indent = 6)

### IF REQUESTED BY USER, DISPLAY LAYER

remove_existing_layers(["Loop polygons"])

if display_polygons:
    vlayer_polygons = QgsVectorLayer(output_file, "Loop polygons", "ogr")
    QgsProject.instance().addMapLayer(vlayer_polygons)

    group_layers(
        "Polygonize network",
        [
            "Loop polygons",
        ],
        remove_group_if_exists=True,
    )

    zoom_to_layer("Loop polygons")


layer_names = [layer.name() for layer in QgsProject.instance().mapLayers().values()]
if "Basemap" in layer_names:
    move_basemap_back(basemap_name="Basemap")

print("07_polygonize script ended successfully \n")