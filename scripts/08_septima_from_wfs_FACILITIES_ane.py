### IMPORT all layers from "FACILITETER" WFS; keep info on *what* kind of facility it is

### CUSTOM SETTINGS
show_study_area = True


# import libraries
import os
import yaml
import geopandas as gpd
from owslib.wfs import WebFeatureService

# define paths
homepath = (
    QgsProject.instance().homePath()
)  # homepath variable (where is the qgis project saved?)
configfile = os.path.join(homepath, "config.yml")  # filepath of config file
output_path = os.path.join(homepath, "output_overlay.gpkg")  # filepath of config file
study_area_path = os.path.join(homepath, "data/raw/user_input/study_area.gpkg")

# load configs
configs = yaml.load(open(configfile), Loader=yaml.FullLoader)
proj_crs = configs["proj_crs"]

if show_study_area == True:
    # make vector layer of study area
    study_area_vlayer = QgsVectorLayer(study_area_path, "Study area", "ogr")
    QgsProject.instance().addMapLayer(study_area_vlayer)


def add_wfs_layers(
    wfs_core,
    study_area_path,
    wfs_version="1.1.0",
    wfs_name="wfs_data",
    proj_crs="EPSG:25832",
    geom_type="Point",
):
    study_area_gdf = gpd.read_file(study_area_path)

    bounds = study_area_gdf.bounds
    minx = bounds.minx[0]
    miny = bounds.miny[0]
    maxx = bounds.maxx[0]
    maxy = bounds.maxy[0]

    # define WFS URL
    wfs_url_get = wfs_core + "&request=GetCapabilities"
    wfs_get = WebFeatureService(url=wfs_url_get, version=wfs_version)
    layers_to_import = list(wfs_get.contents)

    print("Importing layers:", layers_to_import)

    # create an empty QgsVectorLayer (for all wfs layers)
    merged_wfs_name = wfs_name + "_MERGED"
    new_layer = QgsVectorLayer(
        f"{geom_type}?crs={proj_crs}&field=category:string", merged_wfs_name, "memory"
    )

    for mytypename in layers_to_import:
        print("Getting data for layer:", mytypename)

        wfs_url = (
            wfs_core
            + f"&request=GetFeature&typeName={mytypename}&SRSName=EPSG:25832&BBOX={minx},{miny},{maxx},{maxy}"
        )

        Source = f"pagingEnabled='true' preferCoordinatesForWfsT11='false' restrictToRequestBBOX='1' srsname={proj_crs} typename={mytypename} url={wfs_url} version='auto'"

        # initialize vector layer of WFS features
        temp_layer = QgsVectorLayer(Source, wfs_name, "WFS")

        # clip to study area polygon
        temp_clip_out = processing.run(
            "native:clip",
            {
                "INPUT": temp_layer,
                "OVERLAY": study_area_vlayer,
                "OUTPUT": "TEMPORARY_OUTPUT",
            },
        )

        current_layer = temp_clip_out["OUTPUT"]

        ### TO DO 1: MAKE THE ADDING OF FEATUES (BELOW) MORE EFFICIENT INSTEAD OF LOOPING THROUGH ALL FEATURES... if possible?
        # make a list of all features of current layer, with mytypename (layer name) as attribute
        ### TO DO 2: HOW CAN WE KEEP ALL ATTRIBUTES (there are different numbers of attributes for different layers)
        ### and just *add* an attribute called "facility_type" where we keep the information on which WFS layer each feature comes from
        ### (in the current version of the code, we don't keep any attributes, and create a separate attribute where we insert the layer name)

        features_list = []
        for feat in current_layer.getFeatures():
            feature = QgsFeature()  # initialize feature
            feature.setGeometry(feat.geometry())  # add geometries
            feature.setAttributes([mytypename])  # add type name attribute
            features_list.append(feature)
        ## to add features, access data provider behind the layer with method addfeatures
        new_layer.dataProvider().addFeatures(features_list)

    return new_layer


wfs_core = (
    "https://rida-services.test.septima.dk/ows?map=facilit_faciliteter&service=WFS"
)
new_facilities_layer = add_wfs_layers(wfs_core, study_area_path)


# add merged layer to map
QgsProject.instance().addMapLayer(new_facilities_layer)
print("Added merged facilities layer")


def visualize_categorical(layer_name, column_name):
    # based on https://gis.stackexchange.com/questions/175068/applying-categorized-symbol-to-each-feature-using-pyqgis
    
    my_layer = QgsProject.instance().mapLayersByName(layer_name)[0]
    iface.setActiveLayer(my_layer)
    layer = iface.activeLayer()
    
    idx = layer.fields().indexOf(column_name)
    
    if idx == -1: 
        idx = 0
    
    unique_values = layer.uniqueValues(idx)
    
    categories = []
    for unique_value in unique_values:
        # initialize the default symbol for this geometry type
        symbol = QgsSymbol.defaultSymbol(layer.geometryType())

        # configure a symbol layer
        layer_style = {}
        layer_style['color'] = '%d, %d, %d' % (randrange(0, 256), randrange(0, 256), randrange(0, 256))
        layer_style['outline'] = '#000000'
        symbol_layer = QgsSimpleFillSymbolLayer.create(layer_style)

        # replace default symbol layer with the configured one
        if symbol_layer is not None:
            symbol.changeSymbolLayer(0, symbol_layer)

        # create renderer object
        category = QgsRendererCategory(unique_value, symbol, str(unique_value))
        
        # entry for the list of category items
        categories.append(category)

    # create renderer object
    renderer = QgsCategorizedSymbolRenderer("Category", categories)

    # assign the created renderer to the layer
    if renderer is not None:
        layer.setRenderer(renderer)

    layer.triggerRepaint()
    iface.layerTreeView().refreshLayerSymbology(layer.id())
  

unique_values = ["rasteplads_suppl","infoservice_suppl","indkoeb","overnatning","rasteplads","infoservice"]
  
visualize_categorical("wfs_data_MERGED","Category")