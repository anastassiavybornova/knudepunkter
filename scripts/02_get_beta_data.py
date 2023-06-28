### CUSTOM SETTINGS
display_layer = True
### NO CHANGES BELOW THIS LINE

import os
os.environ['USE_PYGEOS'] = '0' # pygeos/shapely2.0/osmnx conflict solving
import geopandas as gpd

# define homepath variable (where is the qgis project saved?)
homepath = QgsProject.instance().homePath()

# read in file
edges = gpd.read_file(homepath + "/data/raw/folkersma_beta/stretch.shp")

# remove empty geometries
edges = edges[~edges.geometry.isna()].reset_index(drop=True)

# assert there is one (and only one) LineString per geometry row
edges = edges.explode(index_parts=False).reset_index(drop=True)
assert all(edges.geometry.type=="LineString")
assert all(edges.geometry.is_valid)

# rectify attributes (ratings)
edges["myattribute"]= edges["rating"].fillna(0)
edges["myattribute"] = edges.apply(lambda x: int(x.myattribute), axis = 1)

# classify manually
edges.loc[edges["myattribute"]==0, "myattribute"] = 1

# add crs to edges
edges.crs = "EPSG:4326"

# convert to projected crs
edges = edges.to_crs("EPSG:25832")

# Read in study area
study_area = gpd.read_file(homepath + "/data/raw/user_input/study_area.gpkg")
study_area_polygon = study_area.loc[0,"geometry"]

# Find all edges that intersect the study area polygon
edges_in_study_area = edges[
    edges.intersects(study_area_polygon)].copy().reset_index(drop=True)

os.makedirs(homepath + "/data/processed/workflow_steps", exist_ok=True)
filepath_to = homepath + "/data/processed/workflow_steps/qgis_input_beta.gpkg"
edges_in_study_area.to_file(filepath_to, index=False)

print("preprocessed beta network data for study area saved to:", filepath_to)

if display_layer == True:
    vlayer = QgsVectorLayer(filepath_to, "beta data (pre-network)", "ogr")
    if not vlayer.isValid():
        print("Layer failed to load!")
    else:
        QgsProject.instance().addMapLayer(vlayer)