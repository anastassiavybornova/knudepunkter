### TO DO:
# * segmentization !
# Ane: selecting black ones: the ones that do not intersect the red buffer
# cf. clip & cut qgis functionalities


### CUSTOM SETTINGS
display_complayer_conc = True
display_complayer_both = True
display_complayer_beta = True

### NO CHANGES BELOW THIS LINE

# define homepath variable (where is the qgis project saved?)
homepath = QgsProject.instance().homePath()

# define filepaths for this file
edges_beta = homepath + "/data/processed/workflow_steps/edges_beta.gpkg"
edges_concept = homepath + "/data/processed/workflow_steps/edges_concept.gpkg"
edgecomp_beta = homepath + "/data/processed/workflow_steps/edgecomp_beta.gpkg"
edgecomp_conc = homepath + "/data/processed/workflow_steps/edgecomp_conc.gpkg"
edgecomp_both = homepath + "/data/processed/workflow_steps/edgecomp_both.gpkg"

# import libraries
import os
os.environ['USE_PYGEOS'] = '0'
import geopandas as gpd
import shapely

# import network edges concept
gdf = gpd.read_file(edges_concept)
n = shapely.node(gdf.unary_union)
n = gpd.GeoDataFrame({"geometry": [n]}, crs = gdf.crs)
n = n.explode(index_parts=False).reset_index(drop=True)
conc_edges = n.copy()
del(gdf,n)

# import network edges beta
gdf = gpd.read_file(edges_beta)
n = shapely.node(gdf.unary_union)
n = gpd.GeoDataFrame({"geometry": [n]}, crs = gdf.crs)
n = n.explode(index_parts=False).reset_index(drop=True)
beta_edges = n.copy()
del(gdf,n)

conc_edges_buffered = conc_edges.copy()
conc_edges_buffered["geometry"] = conc_edges_buffered.buffer(25)

edges_in_both = beta_edges[beta_edges.intersection(conc_edges_buffered.unary_union).length / beta_edges.length > 0.5].copy()
edges_only_beta = beta_edges.copy().drop(labels = edges_in_both.index, axis = 0)

edges_in_both = edges_in_both.reset_index(drop=True)
edges_only_beta = edges_only_beta.reset_index(drop=True)

conc_edges.to_file(edgecomp_conc, index = False)
edges_in_both.to_file(edgecomp_both, index = False)
edges_only_beta.to_file(edgecomp_beta, index = False)

def plot_layer(filepath, layername, line_color, line_width, layer_opacity):
    
    mylayer = QgsVectorLayer(filepath, layername, "ogr")
    
    if not mylayer.isValid():
        print(f"{layername}: layer failed to load!")
    
    else:
        
        myrenderer = mylayer.renderer()
        #print("Type:", myrenderer.type())
        
        props = myrenderer.symbol().symbolLayer(0).properties()
        #print(props)
        
        props["line_color"] = line_color
        props["line_width"] = line_width
        
        myrenderer.setSymbol(QgsLineSymbol.createSimple(props))
        mylayer.setOpacity(layer_opacity)
        QgsProject.instance().addMapLayer(mylayer)

if display_complayer_conc == True:
    plot_layer(edgecomp_conc, "Comparison: Concept network", "black", "1", 0.8)
if display_complayer_beta == True:
    plot_layer(edgecomp_beta, "Comparison: Beta network", "green", "2", 0.5)
if display_complayer_both == True:
    plot_layer(edgecomp_both, "Comparison: In both networks", "red", "3", 0.5)
