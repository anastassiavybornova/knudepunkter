### ***************
### for a polygon defined by the user,
### fetch and preprocess beta network data.
### ***************
### CUSTOM SETTINGS
display_studyarea_layer = True
display_beta_layer = True
### NO CHANGES BELOW THIS LINE

# import python packages
import os

os.environ["USE_PYGEOS"] = "0"  # pygeos/shapely2.0/osmnx conflict solving
import geopandas as gpd

# define projected crs
proj_crs = "EPSG:25832"

# define homepath variable (where is the qgis project saved?)
homepath = QgsProject.instance().homePath()

# import functions
exec(open(homepath + "/src/plot_func.py").read())


# define location of study area polygon (user-provided)
filepath_study = homepath + "/data/raw/user_input/study_area.gpkg"

# read in study area polygon provided by the user
study_area = gpd.read_file(filepath_study)
study_area = study_area.to_crs(proj_crs)

# Remove layers from project if they exist already
remove_existing_layers(["Study area", "beta data (pre-network)"])

# if requested by user, display study area polygon
if display_studyarea_layer == True:
    vlayer = QgsVectorLayer(filepath_study, "Study area", "ogr")
    if not vlayer.isValid():
        print("Study area layer failed to load!")
    else:
        QgsProject.instance().addMapLayer(vlayer)
        draw_simple_polygon_layer(
            "Study area",
            color="250,181,127,128",
            outline_color="black",
            outline_width=0.5,
        )
        zoom_to_layer("Study area")


# ******* Code below used to import beta data.
# ******* This will be replaced by
# ******* a request to GeoDK for the data (?)

# read in edges of entire beta network
# WILL BE REPLACED BY GEOFA REQUEST
edges = gpd.read_file(
    homepath
    + "/data/raw/folkersma_digital/2023-08-01 Cycling network Denmark shapefiles/stretch.shp"
)

# remove empty geometries
edges = edges[~edges.geometry.isna()].reset_index(drop=True)

# project
edges = edges.to_crs(proj_crs)

# only keep those edges that are within the study area
edges_study = edges[edges.intersects(study_area.loc[0, "geometry"])].copy()
edges_study.reset_index(drop=True, inplace=True)

del edges

# assert there is one (and only one) LineString per geometry row
edges_study = edges_study.explode(index_parts=False).reset_index(drop=True)
assert all(edges_study.geometry.type == "LineString")
assert all(edges_study.geometry.is_valid)

# rectify attributes (ratings)
edges_study["myattribute"] = edges_study["rating"].fillna(0)
edges_study["myattribute"] = edges_study.apply(lambda x: int(x.myattribute), axis=1)
# do we need this?
edges_study.loc[edges_study["myattribute"] == 0, "myattribute"] = 1

os.makedirs(homepath + "/data/processed/workflow_steps", exist_ok=True)
filepath_to = homepath + "/data/processed/workflow_steps/qgis_input_beta.gpkg"
edges_study.to_file(filepath_to, index=False)

print("Beta data for study area saved to:", filepath_to)

if display_beta_layer == True:
    vlayer = QgsVectorLayer(filepath_to, "beta data (pre-network)", "ogr")
    if not vlayer.isValid():
        print("Layer failed to load!")
    else:
        QgsProject.instance().addMapLayer(vlayer)
        draw_recent_simple_line_layer(color="green", width=0.7, line_style="dash")
