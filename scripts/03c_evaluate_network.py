### indicate which layers to display

display_input = True
display_output = True

### define distance thresholds for point layers
# (move this to config file later)
dist_faci = 100
dist_serv = 500
dist_pois = 1000

dist_bad = 100

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
results_path = homepath + "/results/data/"  # store output geopackages here

# import functions
exec(open(homepath + "/src/plot_func.py").read())

# Remove layers from project if they exist already
remove_existing_layers(
    [
        "Network",
        "Network in undesirable areas",
        "Undesirable areas",
        "Facilities within reach",
        "Facilities not within reach",
    ]
)


# import study area edges
edges = gpd.read_file(study_path)

if display_input:
    vlayer_network = QgsVectorLayer(study_path, "Network", "ogr")

    QgsProject.instance().addMapLayer(vlayer_network)
    draw_simple_line_layer("Network", color="black", linewidth=0.5, line_style="dash")

    zoom_to_layer("Network")


### EVALUATE POLYGON LAYERS
# (agriculture, bad, culture, nature, sommerhus)
# evaluate & display the length % of intersection
# (import; buffer with 100m)

### AGRICULTURE

### BAD

# import "bad" layer
bad = gpd.read_file(eval_path + "bad.gpkg")

# evaluate
bad_eval = eval_func.evaluate_polygon_layer(bad, edges, dist_bad)

print("undesirable areas evaluated")
print(
    f"{bad_eval.unary_union.length / 1000:.2f} out of {edges.unary_union.length / 1000:.2f} km of the network go through undesirable areas."
)

bad_output = results_path + f"bad_network_{dist_bad}.gpkg"
bad_eval.to_file(bad_output)

if display_input:
    vlayer_bad = QgsVectorLayer(eval_path + "bad.gpkg", "Undesirable areas", "ogr")

    QgsProject.instance().addMapLayer(vlayer_bad)
    draw_simple_polygon_layer(
        "Undesirable areas",
        color="170,1,20,100",
        outline_color="170,1,20,200",
        outline_width=0.5,
    )


if display_output:
    vlayer_bad = QgsVectorLayer(bad_output, "Network in undesirable areas", "ogr")
    QgsProject.instance().addMapLayer(vlayer_bad)
    draw_categorical_layer("Network in undesirable areas", "types")


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

facilities_withinreach = facilities_eval.loc[facilities_eval.withinreach == 1]
print(f"{len(facilities_withinreach)} facilities are within reach")

facilities_output = results_path + f"facilities_within_reach_{dist_faci}.gpkg"
facilities_withinreach.to_file(facilities_output)

facilities_outside_output = results_path + f"facilities_outside_reach_{dist_faci}.gpkg"
facilities_eval.loc[facilities_eval.withinreach == 0].to_file(facilities_outside_output)

if display_output:
    vlayer_faci = QgsVectorLayer(facilities_output, "Facilities within reach", "ogr")
    vlayer_faci_all = QgsVectorLayer(
        facilities_outside_output, "Facilities not within reach", "ogr"
    )

    QgsProject.instance().addMapLayer(vlayer_faci)
    draw_categorical_layer("Facilities within reach", "type", marker_size=3)

    QgsProject.instance().addMapLayer(vlayer_faci_all)
    draw_simple_point_layer(
        "Facilities not within reach", marker_size=2, color="red", outline_width=0.0
    )


### SERVICE


### POIS


### MISSING: QUANTITATIVE SUMMARY OF RESULTS
# absolute + percentage length in each layer (for polygon layers)
# absolute + perentage number of points in each layer (for point layers)
# (refine once we have taken care of parallel edges)

if display_input == False and display_output == True:
    group_layers(
        "Evaluate network",
        [
            "Network in undesirable areas",
            "Facilities not within reach",
            "Facilities within reach",
        ],
        remove_group_if_exists=True,
    )

if display_input == True and display_output == False:
    group_layers(
        "Evaluate network",
        ["Network", "Undesirable areas"],
        remove_group_if_exists=True,
    )


if display_input == True and display_output == True:
    group_layers(
        "Evaluate network",
        [
            "Network",
            "Undesirable areas",
            "Network in undesirable areas",
            "Facilities not within reach",
            "Facilities within reach",
        ],
        remove_group_if_exists=True,
    )
