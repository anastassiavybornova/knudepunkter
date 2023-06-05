### CUSTOM SETTINGS
my_threshold = 250 # in meters
display_conc = True
display_beta = True
display_both = True
display_none = True
### NO CHANGES BELOW THIS LINE

# define homepath variable (where is the qgis project saved?)
homepath = QgsProject.instance().homePath()

fp_onlybeta = homepath + "/data/processed/workflow_steps/pois_beta.gpkg"
fp_onlyconc = homepath + "/data/processed/workflow_steps/pois_conc.gpkg"
fp_inboth = homepath + "/data/processed/workflow_steps/pois_both.gpkg"
fp_innone = homepath + "/data/processed/workflow_steps/pois_none.gpkg"

# import libraries
import os
os.environ['USE_PYGEOS'] = '0'
import geopandas as gpd
import shapely

# import network edges concept
gdf = gpd.read_file(homepath + "/data/processed/workflow_steps/edges_concept.gpkg")
n = shapely.node(gdf.unary_union)
n = gpd.GeoDataFrame({"geometry": [n]}, crs = gdf.crs)
n = n.explode(index_parts=False).reset_index(drop=True)
conc_edges = n.copy()
del(gdf,n)

# import network edges beta
gdf = gpd.read_file(homepath + "/data/processed/workflow_steps/edges_beta.gpkg")
n = shapely.node(gdf.unary_union)
n = gpd.GeoDataFrame({"geometry": [n]}, crs = gdf.crs)
n = n.explode(index_parts=False).reset_index(drop=True)
beta_edges = n.copy()
del(gdf,n)

# import septima data (point)

filepath_septima = homepath + "/data/processed/septima/land_landemaerke/land_landemaerke.gpkg"
landemaerke = gpd.read_file(filepath_septima)

# which of these POIs are within threshold of which network?
li_beta = landemaerke[landemaerke.intersects(beta_edges.buffer(my_threshold).unary_union)].index
li_conc = landemaerke[landemaerke.intersects(conc_edges.buffer(my_threshold).unary_union)].index

li_onlybeta = list(set(li_beta).difference(li_conc))
li_onlyconc = list(set(li_conc).difference(li_beta))
li_inboth = list(set(li_beta).intersection(li_conc))
li_innone = list( set(landemaerke.index).difference(set(li_beta).union(set(li_conc))) )

landemaerke.filter(
    li_onlybeta, axis = 0).copy().reset_index(drop=True).to_file(
    fp_onlybeta, index = False)

landemaerke.filter(
    li_onlyconc, axis = 0).copy().reset_index(drop=True).to_file(
    fp_onlyconc, index = False)

landemaerke.filter(
    li_inboth, axis = 0).copy().reset_index(drop=True).to_file(
    fp_inboth, index = False)

landemaerke.filter(
    li_innone, axis = 0).copy().reset_index(drop=True).to_file(
    fp_innone, index = False)


# plotting function
def plot_layer(filepath, layername, point_color, point_size, layer_opacity = None):
    
    mylayer = QgsVectorLayer(filepath, layername, "ogr")
    if not mylayer.isValid():
        print(f"{layername}: layer failed to load!")
    else:
        myrenderer = mylayer.renderer()
        #print("Type:", myrenderer.type())
        props = myrenderer.symbol().symbolLayer(0).properties()
        #print(props)
        
        props["color"] = point_color
        props["size"] = point_size
        
        myrenderer.setSymbol(QgsMarkerSymbol.createSimple(props))
        
        if layer_opacity != None:
            mylayer.setOpacity(layer_opacity)
        
        QgsProject.instance().addMapLayer(mylayer)
    
if display_beta == True:
    plot_layer(
        fp_onlybeta, 
        "POIs: Only beta", 
        point_color = "green", 
        point_size = 4, 
        layer_opacity = 0.7)
if display_conc == True:
    plot_layer(
        fp_onlyconc, 
        "POIs: Only concept", 
        point_color = "red", 
        point_size = 4, 
        layer_opacity = 0.7)
if display_both == True:
    plot_layer(
        fp_inboth, 
        "POIs: in both networks", 
        point_color = "orange", 
        point_size = 3, 
        layer_opacity = 1)
if display_none == True:
    plot_layer(
        fp_innone, 
        "POIs: in none of the networks", 
        point_color = "black", 
        point_size = 3, 
        layer_opacity = 1)
