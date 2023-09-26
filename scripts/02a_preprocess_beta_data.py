### Script for preprocessing beta data to prepare for network creation

### *********
### CUSTOM SETTINGS
### *********
display_intermediate_data = True
display_preprocessed_layer = True
snap_tolerance = 5  # distance threshold for when to snap objects (in meters)
snap_behaviour = 6  # end point to end point
snap_behaviour_verbose = "end point to end point"

### NO CHANGES BELOW THIS LINE

# import packages
import os

os.environ["USE_PYGEOS"] = "0"
import geopandas as gpd
from src import plot_func

# define homepath variable (where is the qgis project saved?)
homepath = QgsProject.instance().homePath()

### *********
### Functions
### *********

exec(open(homepath + "/src/plot_func.py").read())

### *********
### Step 1: preprocess data with qgis methods
### *********

# INPUT/OUTPUT FILE PATHS
inputfile = homepath + "/data/processed/workflow_steps/qgis_input_beta.gpkg"
outputfile = homepath + "/data/processed/workflow_steps/qgis_output_beta.gpkg"

# Remove temporary layers from project if they exist already
remove_existing_layers(["Valid", "Split", "Snapped", "input", "Beta"])

# TEMP - load input data
org_input = QgsVectorLayer(inputfile, "input data", "ogr")

if display_intermediate_data:
    QgsProject.instance().addMapLayer(org_input)

    draw_recent_simple_line_layer(color="blue", width=0.5)
    zoom_to_layer("input data")


# Run processing algorithm "split with lines"
temp_out_split = processing.run(
    "native:splitwithlines",
    {"INPUT": inputfile, "LINES": inputfile, "OUTPUT": "TEMPORARY_OUTPUT"},
)
print("done: split with lines")

if display_intermediate_data:
    QgsProject.instance().addMapLayer(temp_out_split["OUTPUT"])
    draw_recent_simple_line_layer(color="red", width=0.7)

# snap
temp_out_snap = processing.run(
    "native:snapgeometries",
    {
        "INPUT": temp_out_split["OUTPUT"],
        "REFERENCE_LAYER": temp_out_split["OUTPUT"],
        "TOLERANCE": snap_tolerance,
        "BEHAVIOR": snap_behaviour,
        "OUTPUT": "TEMPORARY_OUTPUT",
    },
)
print(
    f"done: snapped with tolerance {snap_tolerance}, behaviour: '{snap_behaviour_verbose}'"
)

if display_intermediate_data:
    QgsProject.instance().addMapLayer(temp_out_snap["OUTPUT"])
    draw_recent_simple_line_layer(color="orange", width=0.7)

# Check validity
temp_out_validity = processing.run(
    "qgis:checkvalidity",
    {
        "INPUT_LAYER": temp_out_snap["OUTPUT"],
        "METHOD": 2,
        "IGNORE_RING_SELF_INTERSECTION": False,
        "VALID_OUTPUT": "TEMPORARY_OUTPUT",
        "INVALID_OUTPUT": None,  # homepath + "/data/invalid.gpkg",
        "ERROR_OUTPUT": None,
    },
)
print("done: validity check")

if display_intermediate_data:
    QgsProject.instance().addMapLayer(temp_out_validity["VALID_OUTPUT"])
    draw_recent_simple_line_layer(color="blue", width=0.7)


vlayer = temp_out_validity["VALID_OUTPUT"]

layer_provider = vlayer.dataProvider()

# delete "fid" field (to prevent problems when exporting a layer with non-unique fields)
fid_idx = vlayer.fields().indexOf("fid")
vlayer.dataProvider().deleteAttributes([fid_idx])
vlayer.updateFields()


# export
_writer = QgsVectorFileWriter.writeAsVectorFormat(
    vlayer, outputfile, "utf-8", vlayer.crs(), "GPKG"
)

print(f"done: saved to {outputfile}")

if display_preprocessed_layer == True:
    vlayer = QgsVectorLayer(outputfile, "Beta data pre network", "ogr")
    if not vlayer.isValid():
        print("Layer failed to load!")
    else:
        QgsProject.instance().addMapLayer(vlayer)
        draw_recent_simple_line_layer(color="magenta", width=1)
