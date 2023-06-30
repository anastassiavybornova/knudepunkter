### IMPORT all layers from "FACILITETER" WFS; keep info on *what* kind of facility it is

### CUSTOM SETTINGS
show_study_area = True
# TO DO: HOW CAN WE EASILY ACCESS/CREATE THIS LIST?
# (i.e. how to make a list of all available layers from a specified WFS URL)
layers_to_import = [
    "rasteplads_suppl",
    "infoservice_suppl",
    "indkoeb",
    "overnatning",
    "rasteplads",
    "infoservice"
]

# import libraries
import os
import yaml
import geopandas as gpd

# define paths
homepath = QgsProject.instance().homePath() # homepath variable (where is the qgis project saved?)
configfile = os.path.join(homepath, "config.yml") # filepath of config file
output_path = os.path.join(homepath, "output_overlay.gpkg") # filepath of config file
study_area_path = os.path.join(homepath, "data/raw/user_input/study_area.gpkg")

# define WFS URL
wfs_url = "https://rida-services.test.septima.dk/ows?map=facilit_faciliteter"

# load configs 
configs = yaml.load(open(configfile), Loader=yaml.FullLoader)
proj_crs = configs["proj_crs"]

if show_study_area == True:
    # make vector layer of study area
    study_area_vlayer = QgsVectorLayer(study_area_path, "Study area", "ogr")
    QgsProject.instance().addMapLayer(study_area_vlayer)

### TO DO: can we avoid selectbyRect & clip to polygon, by directly selecting by Polygon?

# make envelope of study area
study_area_gdf = gpd.read_file(study_area_path)
mybox = str(study_area_gdf.envelope[0]) # get bounding box of study area as string

# create an empty QgsVectorLayer (for all facilities)
facilities_layer = QgsVectorLayer(
    f"Point?crs={proj_crs}&field=factype:string",
    "FACILITIES_MERGED",
    "memory"
    )

# initialize list of features
features_list = []

# TO DO: PUT THE FOR-LOOP CONTENT INTO A FUNCTION
# the forloop does the following, for each layer within the facilities WFS:
# - selects WFS features from a given layer by rectangle
# - creates a layer with those features
# - clips the layer to the study area polygon
# - adds the layername as (only) attribute to all the geometries of the layer
# - adds the features of the layer to the "facilities" layer

### LOOP THROUGH ALL LAYERS TO IMPORT
for mytypename in layers_to_import:

    # create WFS request string
    Source = f"pagingEnabled='true' preferCoordinatesForWfsT11='false' restrictToRequestBBOX='1' srsname={proj_crs} typename={mytypename} url={wfs_url} version='auto'"

    # initialize vector layer of WFS features
    tempWFS = QgsVectorLayer(Source, "FACILITIES", "WFS")

    # select by rectangle (bbox)
    tempWFS.selectByRect(QgsRectangle.fromWkt(mybox))
    tempWFS_subset = tempWFS.materialize(QgsFeatureRequest().setFilterFids(tempWFS.selectedFeatureIds()))

    # clip to study area polygon
    temp_clip_out = processing.run(
        "native:clip", 
            {'INPUT': tempWFS_subset,
             'OVERLAY': study_area_vlayer,
             'OUTPUT':'TEMPORARY_OUTPUT'
            }
    )
    
    current_layer = temp_clip_out["OUTPUT"]
    
    ### TO DO 1: MAKE THE ADDING OF FEATUES (BELOW) MORE EFFICIENT INSTEAD OF LOOPING THROUGH ALL FEATURES... if possible?
    # make a list of all features of current layer, with mytypename (layer name) as attribute
    ### TO DO 2: HOW CAN WE KEEP ALL ATTRIBUTES (there are different numbers of attributes for different layers)
    ### and just *add* an attribute called "facility_type" where we keep the information on which WFS layer each feature comes from
    ### (in the current version of the code, we don't keep any attributes, and create a separate attribute where we insert the layer name) 
    features_list = []
    for feat in current_layer.getFeatures():
        feature = QgsFeature() # initialize feature
        feature.setGeometry(feat.geometry()) # add geometries
        feature.setAttributes([mytypename]) # add type name attribute
        features_list.append(feature)
    ## to add features, access data provider behind the layer with method addfeatures
    facilities_layer.dataProvider().addFeatures(features_list)

### TO DO: add customized rendering: STYLE OF LAYER = POINTS CATEGORIZED BY "FACTYPE" attribute

# add merged layer to map
QgsProject.instance().addMapLayer(facilities_layer)
print("Added merged facilities layer")