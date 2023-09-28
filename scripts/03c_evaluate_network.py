# TODO: Write docstrings + documentation, move funcs to separate script, test w. different plotting input, summarize results

# TODO:
### MISSING: QUANTITATIVE SUMMARY OF RESULTS
# absolute + percentage length in each layer (for polygon layers)
# absolute + perentage number of points in each layer (for point layers)
# (refine once we have taken care of parallel edges)

### indicate which layers to display

display_input = True
display_output = True

### define distance thresholds for point layers
# (move this to config file later)
dist_faci = 100
dist_serv = 500
dist_pois = 1000

dist_bad = 100
dist_agri = 100
dist_culture = 100
dist_nature = 100
dist_summer = 100

### No changes below this line

# import libraries
import os
import os.path

os.environ["USE_PYGEOS"] = "0"  # pygeos/shapely2.0/osmnx conflict solving
import geopandas as gpd
import pandas as pd
from shapely import strtree

# from src import eval_func

# define paths
homepath = QgsProject.instance().homePath()  # where is QGIS project
study_path = (
    homepath + "/data/processed/workflow_steps/qgis_output_beta.gpkg"
)  # where is study area network
eval_path = homepath + "/data/processed/eval/"  # where is evaluation data
results_path = homepath + "/results/data/"  # store output geopackages here

# import functions
exec(open(homepath + "/src/plot_func.py").read())
exec(open(homepath + "/src/eval_func.py").read())

# Remove layers from project if they exist already

remove_existing_layers(
    [
        "Network",
        "Network in undesirable areas",
        "Undesirable areas",
        "Network in agricultural areas",
        "Agricultural areas",
        "Network in nature areas",
        "Nature areas",
        "Network in culture areas",
        "Culture areas",
        "Network in summer house areas",
        "Summer house areas",
        "Facilities within reach",
        "Facilities not within reach",
        "Services within reach",
        "Services not within reach",
        "POIS within reach",
        "POIS not within reach",
    ]
)

# define root
root = QgsProject.instance().layerTreeRoot()

# make main group for layers
main_group_name = "Evaluate network"

# Check if group already exists
for group in [child for child in root.children() if child.nodeType() == 0]:
    if group.name() == main_group_name:
        root.removeChildNode(group)

# Initialize list of layers for layer grouping
input_layers = []
output_layers = []

# import study area edges
edges = gpd.read_file(study_path)

if display_input:
    vlayer_network = QgsVectorLayer(study_path, "Network", "ogr")

    QgsProject.instance().addMapLayer(vlayer_network)
    draw_simple_line_layer("Network", color="black", line_width=0.5, line_style="dash")

    zoom_to_layer("Network")

    input_layers.append("Network")


#### **** EVALUATE POLYGON LAYERS **** ####

#### AGRICULTURE ####

if os.path.exists(eval_path + "agriculture.gpkg"):
    agri_input_name, agri_output_name = evaluate_export_plot_poly(
        input_fp=eval_path + "agriculture.gpkg",
        output_fp=results_path + f"agricultural_network_{dist_agri}.gpkg",
        network_edges=edges,
        dist=dist_agri,
        name="Agricultural",
        type_col="types",
        fill_color_rgb="205,186,136",
        outline_color_rgb="205,186,136",
        line_color_rgb="205,186,136",
        line_width=1,
        line_style="solid",
        plot_categorical=False,
        fill_alpha="100",
        outline_alpha="200",
        display_output=True,
        display_input=True,
    )

    input_layers.append(agri_input_name)
    output_layers.append(agri_output_name)

#### BAD #####

if os.path.exists(eval_path + "bad.gpkg"):
    bad_input_name, bad_output_name = evaluate_export_plot_poly(
        input_fp=eval_path + "bad.gpkg",
        output_fp=results_path + f"bad_network_{dist_bad}.gpkg",
        network_edges=edges,
        dist=dist_bad,
        name="Undesirable",
        type_col="types",
        fill_color_rgb="170,1,20",
        outline_color_rgb="170,1,20",
        line_color_rgb="170,1,20",
        line_width=1,
        line_style="solid",
        plot_categorical=False,
        fill_alpha="100",
        outline_alpha="200",
        display_output=True,
        display_input=True,
    )

    input_layers.append(bad_input_name)
    output_layers.append(bad_output_name)

#### CULTURE ####

if os.path.exists(eval_path + "culture.gpkg"):
    culture_input_name, culture_output_name = evaluate_export_plot_poly(
        input_fp=eval_path + "culture.gpkg",
        output_fp=results_path + f"culture_network_{dist_culture}.gpkg",
        network_edges=edges,
        dist=dist_culture,
        name="Culture",
        type_col="types",
        fill_color_rgb="86,85,211",
        outline_color_rgb="86,85,211",
        line_color_rgb="86,85,211",
        line_width=1,
        line_style="solid",
        plot_categorical=False,
        fill_alpha="100",
        outline_alpha="200",
        display_output=True,
        display_input=True,
    )

    input_layers.append(culture_input_name)
    output_layers.append(culture_output_name)

#### NATURE ####

if os.path.exists(eval_path + "nature.gpkg"):
    nature_input_name, nature_output_name = evaluate_export_plot_poly(
        input_fp=eval_path + "nature.gpkg",
        output_fp=results_path + f"nature_network_{dist_nature}.gpkg",
        network_edges=edges,
        dist=dist_nature,
        name="Nature",
        type_col="types",
        fill_color_rgb="0,128,0",
        outline_color_rgb="0,128,0",
        line_color_rgb="0,128,0",
        line_width=1,
        line_style="solid",
        plot_categorical=False,
        fill_alpha="100",
        outline_alpha="200",
        display_output=True,
        display_input=True,
    )

    input_layers.append(nature_input_name)
    output_layers.append(nature_output_name)

#### SOMMERHUS ####

if os.path.exists(eval_path + "sommerhus.gpkg"):
    summer_input_name, summer_output_name = evaluate_export_plot_poly(
        input_fp=eval_path + "sommerhus.gpkg",
        output_fp=results_path + f"summer_network_{dist_summer}.gpkg",
        network_edges=edges,
        dist=dist_summer,
        name="Summer house",
        type_col="types",
        fill_color_rgb="255,165,0",
        outline_color_rgb="255,165,0",
        line_color_rgb="255,165,0",
        line_width=1,
        line_style="solid",
        plot_categorical=False,
        fill_alpha="100",
        outline_alpha="200",
        display_output=True,
        display_input=True,
    )

    input_layers.append(summer_input_name)
    output_layers.append(summer_output_name)

#### **** EVALUATE POINT LAYERS **** ####
# for point layers, whether they are within given distance
# (facilities (in 100m), service (500m), pois (1000m))


#### FACILITIES ####

if os.path.exists(eval_path + "facilities.gpkg"):
    faci_input_name, faci_output_name = evaluate_export_plot_point(
        input_fp=eval_path + "facilities.gpkg",
        within_reach_output_fp=results_path
        + f"facilities_within_reach_{dist_faci}.gpkg",
        outside_reach_output_fp=results_path
        + f"facilities_outside_reach_{dist_faci}.gpkg",
        network_edges=edges,
        dist=dist_faci,
        name="Facilities",
        type_col="type",
    )

    input_layers.append(faci_input_name)
    output_layers.append(faci_output_name)


#### SERVICE ####

if os.path.exists(eval_path + "facilities.gpkg"):
    service_input_name, service_output_name = evaluate_export_plot_point(
        input_fp=eval_path + "service.gpkg",
        within_reach_output_fp=results_path + f"service_within_reach_{dist_faci}.gpkg",
        outside_reach_output_fp=results_path
        + f"service_outside_reach_{dist_faci}.gpkg",
        network_edges=edges,
        dist=dist_faci,
        name="Services",
        type_col="type",
    )

    input_layers.append(service_input_name)
    output_layers.append(service_output_name)

#### POIS ####

if os.path.exists(eval_path + "pois.gpkg"):
    pois_input_name, pois_output_name = evaluate_export_plot_point(
        input_fp=eval_path + "pois.gpkg",
        within_reach_output_fp=results_path + f"pois_within_reach_{dist_faci}.gpkg",
        outside_reach_output_fp=results_path + f"pois_outside_reach_{dist_faci}.gpkg",
        network_edges=edges,
        dist=dist_pois,
        name="POIS",
        type_col="type",
    )

    input_layers.append(pois_input_name)
    output_layers.append(pois_output_name)


all_layers = input_layers + output_layers


types = [
    "Culture",
    "Nature",
    "Agricultural",
    "Undesirable",
    "POIS",
    "Service",
    "Facilities",
    "Summer",
]


# make main group
main_group = root.insertGroup(0, main_group_name)

for t in types:
    if display_input == False and display_output == True:
        layer_names = [o for o in input_layers if t in o or t.lower() in o]

        sub_group = main_group.addGroup(t)

        for layer_name in layer_names:
            add_layer_to_group(layer_name, sub_group)

    if display_input == True and display_output == False:
        layer_names = [o for o in output_layers if t in o or t.lower() in o]

        sub_group = main_group.addGroup(t)

        add_layer_to_group("Network", main_group)

        for layer_name in layer_names:
            add_layer_to_group(layer_name, sub_group)

    if display_input == True and display_output == True:
        layer_names = [o for o in all_layers if t in o or t.lower() in o]

        sub_group = main_group.addGroup(t)

        add_layer_to_group("Network", main_group)

        for layer_name in layer_names:
            add_layer_to_group(layer_name, sub_group)
