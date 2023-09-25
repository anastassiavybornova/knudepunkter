### indicate which layers to display

# polygon layers:
display_agri = True
display_bad = True
display_cult = True
display_natu = True
display_somm = True

# point layers:
display_faci = True
display_serv = True
display_pois = True

### define distance thresholds for point layers
# (move this to config file later)
dist_faci = 100
dist_serv = 500
dist_pois = 1000

### No changes below this line

# import libraries
import os

os.environ["USE_PYGEOS"] = "0"  # pygeos/shapely2.0/osmnx conflict solving
import geopandas as gpd
import pandas as pd
from shapely import strtree
from src import eval_func

# define paths
homepath = QgsProject.instance().homePath()  # where is QGIS project
study_path = (
    homepath + "/data/processed/workflow_steps/qgis_output_beta.gpkg"
)  # where is study area network
eval_path = homepath + "/data/processed/eval/"  # where is evaluation data

# import functions
exec(open(homepath + "/src/plot_func.py").read())

# import study area edges
edges = gpd.read_file(study_path)

### EVALUATE POLYGON LAYERS
# (agriculture, bad, culture, nature, sommerhus)
# evaluate & display the length % of intersection
# (import; buffer with 100m)

### AGRICULTURE

### BAD

# import "bad" layer
bad = gpd.read_file(eval_path + "bad.gpkg")

# evaluate
gdf_eval = eval_func.evaluate_polygon_layer(bad, edges, 100)

# TODO: save to file - read into Qgs Vector layer - plot
# MISSING: VISUALIZE evaluation as layer in qgis projet


### CULTURE

### NATURE

### SOMMERHUS

### EVALUATE POINT LAYERS
# for point layers, whether they are within given distance
# (facilities (in 100m), service (500m), pois (1000m))

### FACILITIES

# import layer
facilities = gpd.read_file(eval_path + "facilities.gpkg")

# evaluate layer
facilities_eval = eval_func.evaluate_point_layer(facilities, edges, dist_faci)
print("facilities layer evaluated")

# MISSING: VISUALIZE LAYER


### SERVICE

### POIS


### MISSING: QUANTITATIVE SUMMARY OF RESULTS
# absolute + percentage length in each layer (for polygon layers)
# absolute + perentage number of points in each layer (for point layers)
# (refine once we have taken care of parallel edges)
