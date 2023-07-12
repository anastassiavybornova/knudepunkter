# ******* script used to import concept data (beta network with manual edits from municipalities)
# ******* will be updated to incorporate a custom filepath to a corresponding folder where user is promted to place data

### CUSTOM SETTINGS
display_layer = False
mytolerance = 5
mybehaviour = 6
### NO CHANGES BELOW THIS LINE

import os
os.environ['USE_PYGEOS'] = '0' # pygeos/shapely2.0/osmnx conflict solving
import geopandas as gpd
from PyQt5.QtCore import QVariant

# define homepath variable (where is the qgis project saved?)
homepath = QgsProject.instance().homePath()

# read in file
edges = gpd.read_file(homepath + "/data/raw/faxe_concept/stretch.shp")

# remove empty geometries
edges = edges[~edges.geometry.isna()].reset_index(drop=True)

# assert there is one (and only one) LineString per geometry row
# check crs
edges = edges.explode().reset_index(drop=True)
assert all(edges.geometry.type=="LineString")
assert all(edges.geometry.is_valid)
assert edges.crs == "EPSG:25832"

# INPUT/OUTPUT FILE PATHS
myinputfile = homepath + "/data/processed/workflow_steps/qgis_input_concept.gpkg"
myoutputfile = homepath + "/data/processed/workflow_steps/qgis_output_concept.gpkg"

edges.to_file(myinputfile, index=False)

# Run processing algorithm "split with lines"
temp_out_split = processing.run(
   "native:splitwithlines",
       {
           'INPUT':myinputfile,
           'LINES':myinputfile,
           'OUTPUT':'TEMPORARY_OUTPUT'
       }
   )
print("done: split with lines")

# snap
temp_out_snap = processing.run(
    "native:snapgeometries",
        {
            'INPUT':temp_out_split["OUTPUT"],
            'REFERENCE_LAYER':temp_out_split["OUTPUT"],
            'TOLERANCE':mytolerance,
            'BEHAVIOR':mybehaviour,
            'OUTPUT':'TEMPORARY_OUTPUT'
         }
    )
print(f"done: snapped with tolerance {mytolerance}, behaviour {mybehaviour}")

# Check validity
temp_out_validity = processing.run(
    "qgis:checkvalidity",
        {
            'INPUT_LAYER': temp_out_snap["OUTPUT"],
            'METHOD': 2,
            'IGNORE_RING_SELF_INTERSECTION': False,
            'VALID_OUTPUT': 'TEMPORARY_OUTPUT',
            'INVALID_OUTPUT':None,
            'ERROR_OUTPUT':None
        }
    )
print("done: validity check")

# Delete linestrings of just 1 point
vlayer = temp_out_validity["VALID_OUTPUT"]
layer_provider=vlayer.dataProvider()

# add a "mylength" colum to the attribute table
layer_provider.addAttributes([QgsField("mylength",QVariant.Double)])
vlayer.updateFields()

# fill "mylength" column with length values
vlayer.startEditing()
for f in vlayer.getFeatures():
    id=f.id()
    length=f.geometry().length()
    attr_value={2:length}
    layer_provider.changeAttributeValues({id:attr_value})
vlayer.commitChanges()

# find strings with length 0
expression = 'mylength = 0'
request = QgsFeatureRequest().setFilterExpression(expression)
matches = []
for f in vlayer.getFeatures(request):
   matches.append(f["fid"])

# erase length 0 strings
if vlayer.dataProvider().capabilities() & QgsVectorDataProvider.DeleteFeatures:
    print("layer supports deletion")
    res = vlayer.dataProvider().deleteFeatures(matches)

# delete "mylength" field
vlayer.dataProvider().deleteAttributes([0, 2])

print("done: delete linestrings with length 0")

# export
_ = processing.run(
    "native:package",
        {
            'LAYERS': vlayer,
            'OUTPUT': myoutputfile,
            'OVERWRITE':True,
            'SAVE_STYLES':False,
            'SAVE_METADATA':True,
            'SELECTED_FEATURES_ONLY':False,
            'EXPORT_RELATED_LAYERS':False
        }
    )

print(f"done: save to {myoutputfile}")

if display_layer == True:
    vlayer = QgsVectorLayer(myoutputfile, "Concept data (post-network)", "ogr")
    if not vlayer.isValid():
        print("Layer failed to load!")
    else:
        QgsProject.instance().addMapLayer(vlayer)

