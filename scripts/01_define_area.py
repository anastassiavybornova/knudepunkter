### CUSTOM SETTINGS
display_layer = True
### NO CHANGES BELOW THIS LINE

import os
import geopandas as gpd

# define homepath variable (where is the qgis project saved?)
homepath = QgsProject.instance().homePath()

# read in edges of Faxe concept network
edges = gpd.read_file(homepath + "/data/raw/faxe_concept/stretch.shp")

# define a buffered area around those edges as the study area
study_area_polygon = edges.unary_union.convex_hull.buffer(500)
study_area_gdf = gpd.GeoDataFrame({"geometry":[study_area_polygon]},crs=edges.crs)

# save to file
os.makedirs(homepath + "/data/raw/user_input", exist_ok=True)
filepath_to = homepath + "/data/raw/user_input/study_area.gpkg"
study_area_gdf.to_file(filepath_to, index = False)
print(f"Study area polygon saved to {filepath_to}")

if display_layer == True:
    vlayer = QgsVectorLayer(filepath_to, "Study area", "ogr")
    if not vlayer.isValid():
        print("Study area layer failed to load!")
    else:
        QgsProject.instance().addMapLayer(vlayer)