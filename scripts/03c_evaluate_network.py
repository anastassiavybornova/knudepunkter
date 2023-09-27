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


# TODO: test for diff plotting options

#### **** EVALUATE POLYGON LAYERS **** ####


## HELPER FUNCTIONS ##


# TODO: take into account parallel
def evaluate_export_plot_poly(
    input_fp,
    output_fp,
    network_edges,
    dist,
    name,
    type_col,
    fill_color_rgb,
    outline_color_rgb,
    line_color_rgb,
    line_width=1,
    line_style="solid",
    plot_categorical=False,
    fill_alpha="100",
    outline_alpha="200",
    display_output=True,
    display_input=True,
):
    # TODO: add docstring
    # import layer
    input_poly = gpd.read_file(input_fp)

    # evaluate
    evaluate_network = eval_func.evaluate_polygon_layer(input_poly, network_edges, dist)

    print(f"{name} areas evaluated")
    print(
        f"{evaluate_network.unary_union.length / 1000:.2f} out of {network_edges.unary_union.length / 1000:.2f} km of the network go through {name.lower()} areas."
    )

    # export
    evaluate_network.to_file(output_fp)

    input_layer_name = None
    output_layer_name = None

    # plot
    if display_input:
        input_layer_name = f"{name} areas"

        vlayer_in = QgsVectorLayer(input_fp, input_layer_name, "ogr")

        QgsProject.instance().addMapLayer(vlayer_in)
        draw_simple_polygon_layer(
            input_layer_name,
            color=fill_color_rgb + "," + fill_alpha,
            outline_color=outline_color_rgb + "," + outline_alpha,
            outline_width=0.5,
        )

    if display_output:
        output_layer_name = f"Network in {name.lower()} areas"

        vlayer_out = QgsVectorLayer(output_fp, output_layer_name, "ogr")
        QgsProject.instance().addMapLayer(vlayer_out)

        if plot_categorical:
            draw_categorical_layer(output_layer_name, type_col)

        else:
            draw_simple_line_layer(
                output_layer_name,
                line_color_rgb,
                line_width=line_width,
                line_style=line_style,
            )

    return input_layer_name, output_layer_name


#### AGRICULTURE ####

if os.path.exists(eval_path + "agriculture.gpkg"):
    agri_input_name, agri_output_name = evaluate_export_plot_poly(
        input_fp=eval_path + "agriculture.gpkg",
        output_fp=results_path + f"agricultural_network_{dist_agri}.gpkg",
        network_edges=edges,
        dist=dist_agri,
        name="Agricultural",
        type_col="types",
        fill_color_rgb="245,245,220",
        outline_color_rgb="245,245,220",
        line_color_rgb="245,245,220",
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


def evaluate_export_plot_point(
    input_fp,
    within_reach_output_fp,
    outside_reach_output_fp,
    network_edges,
    dist,
    name,
    type_col,
    input_size=2,
    output_size=5,
    input_alpha="100",
    output_alpha="200",
    display_output=True,
    display_input=True,
):
    # TODO: add docstring
    # import layer
    input_points = gpd.read_file(input_fp)

    # evaluate
    evaluated_points = eval_func.evaluate_point_layer(input_points, network_edges, dist)
    print(f"{name} layer evaluated")

    points_withinreach = evaluated_points.loc[evaluated_points.withinreach == 1]
    print(
        f"Out of {len(input_points)} {name.lower()} points, {len(points_withinreach)} {name.lower()} are within reach"
    )

    # export
    points_withinreach.to_file(within_reach_output_fp)

    evaluated_points.loc[evaluated_points.withinreach == 0].to_file(
        outside_reach_output_fp
    )

    input_layer_name = None
    output_layer_name = None

    # plot
    if display_input:
        input_layer_name = f"{name} not within reach"

        vlayer_outside = QgsVectorLayer(
            outside_reach_output_fp, input_layer_name, "ogr"
        )

        QgsProject.instance().addMapLayer(vlayer_outside)
        draw_categorical_layer(
            input_layer_name,
            type_col,
            alpha=input_alpha,
            marker_size=input_size,
        )

    if display_output:
        output_layer_name = f"{name} within reach"
        vlayer_within = QgsVectorLayer(within_reach_output_fp, output_layer_name, "ogr")

        QgsProject.instance().addMapLayer(vlayer_within)
        draw_categorical_layer(
            output_layer_name,
            type_col,
            alpha=output_alpha,
            marker_size=output_size,
        )

    return input_layer_name, output_layer_name


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

# # import layer
# facilities = gpd.read_file(eval_path + "facilities.gpkg")

# # evaluate layer
# facilities_eval = eval_func.evaluate_point_layer(facilities, edges, dist_faci)
# print("facilities layer evaluated")

# facilities_withinreach = facilities_eval.loc[facilities_eval.withinreach == 1]
# print(f"{len(facilities_withinreach)} facilities are within reach")

# # export
# facilities_output = results_path + f"facilities_within_reach_{dist_faci}.gpkg"
# facilities_withinreach.to_file(facilities_output)

# facilities_outside_output = results_path + f"facilities_outside_reach_{dist_faci}.gpkg"
# facilities_eval.loc[facilities_eval.withinreach == 0].to_file(facilities_outside_output)

# # plot
# if display_output:
#     vlayer_faci = QgsVectorLayer(facilities_output, "Facilities within reach", "ogr")
#     vlayer_faci_all = QgsVectorLayer(
#         facilities_outside_output, "Facilities not within reach", "ogr"
#     )

#     QgsProject.instance().addMapLayer(vlayer_faci)
#     draw_categorical_layer("Facilities within reach", "type", marker_size=3)

#     QgsProject.instance().addMapLayer(vlayer_faci_all)
#     draw_simple_point_layer(
#         "Facilities not within reach", marker_size=2, color="red", outline_width=0.0
#     )


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

# TODO:
### MISSING: QUANTITATIVE SUMMARY OF RESULTS
# absolute + percentage length in each layer (for polygon layers)
# absolute + perentage number of points in each layer (for point layers)
# (refine once we have taken care of parallel edges)

# TODO: group output based on input type?

# TODO: sort alphabetically

all_layers = input_layers + output_layers

if display_input == False and display_output == True:
    group_layers(
        "Evaluate network",
        output_layers,
        remove_group_if_exists=True,
    )

if display_input == True and display_output == False:
    group_layers(
        "Evaluate network",
        input_layers,
        remove_group_if_exists=True,
    )


if display_input == True and display_output == True:
    group_layers(
        "Evaluate network",
        all_layers,
        remove_group_if_exists=True,
    )

# types = [
#     "Culture",
#     "Nature",
#     "Agricultural",
#     "Undesirable",
#     "POIS",
#     "Service",
#     "Facilities",
#     "Summer",
# ]

# types = ["Culture"]

# for t in types:
#     if display_input == False and display_output == True:
#         group_cols = [o for o in output_layers if t in o or t.lower() in o]
#         print(group_cols)
#     #     group_layers(
#     #     "Evaluate network",
#     #     output_layers,
#     #     remove_group_if_exists=True,
#     # )

#     if display_input == True and display_output == False:
#         group_cols = [o for o in output_layers if t in o or t.lower() in o]
#         print(group_cols)
#         # group_layers(
#         #     "Evaluate network",
#         #     input_layers,
#         #     remove_group_if_exists=True,
#         # )

#     if display_input == True and display_output == True:
#         group_cols = [o for o in all_layers if t in o or t.lower() in o]
#         print(group_cols)
#         group_layers(
#             t,
#             group_cols,
#             remove_group_if_exists=True,
#         )
