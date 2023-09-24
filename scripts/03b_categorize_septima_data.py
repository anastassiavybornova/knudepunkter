# merge data from WFS layers 
# (downloaded into gpkg files in /wfs/ folder in 03a_get_septima_data) 
# into layers for evaluation
# this is only a preprocessing step,
# will not desplay anythin

# import libraries
import os
os.environ['USE_PYGEOS'] = '0' # pygeos/shapely2.0/osmnx conflict solving
import geopandas as gpd
import pandas as pd

# define paths
homepath = QgsProject.instance().homePath()
wfs_path = homepath + "/data/raw/wfs"
eval_path = homepath + "/data/processed/eval"

### define helper functions

# imports layers from one WFS folder
def addlayers_from_wfsfolder(wfs_dict, wfs_folder, layernames, wfs_path):
    for wfs_layer in layernames:
        wfs_dict[wfs_folder][wfs_layer] = gpd.read_file(
          wfs_path + f"/{wfs_folder}/{wfs_layer}.gpkg").explode(
            index_parts = False)
    return wfs_dict 

# merges WFS gdfs into one gdf
def merge_gdfs(gdf_list):
    # make sure all gdfs are the same crs
    assert len(set([gdf.crs for gdf in gdf_list]))==1
    # make sure we have the same geometries everywhere
    assert len(set([t for gdf in gdf_list for t in gdf.type]))==1
    # concatenate with pandas
    gdf_main = pd.concat([gdf[["geometry", "type"]].copy() for gdf in gdf_list])    
    return gdf_main

# initialize dict of dicts (keys = wfs folders)
wfs_dict = {}

wfs_folders = [
    "facilit_faciliteter",
    "land_anvendelse",
    "land_attraktioner",
    "land_landskabnatur"
]

for wfs_folder in wfs_folders:
    wfs_dict[wfs_folder] = {}

# import faciliteter layers
faci_layers = [
    "indkoeb", 
    "infoservice", 
    "infoservice_suppl",
    "overnatning",
    "rasteplads",
    "rasteplads_suppl",
    ]

wfs_dict = addlayers_from_wfsfolder(
    wfs_dict = wfs_dict, 
    wfs_folder = "facilit_faciliteter", 
    layernames = faci_layers,
    wfs_path = wfs_path)

# import land_anvendelse layers
anve_layers = [
    "byomraade",
    "dyrket_areal",
    "naturareal",
    "skovinddeling",
    "teknisk_areal"
]

wfs_dict = addlayers_from_wfsfolder(
    wfs_dict = wfs_dict, 
    wfs_folder = "land_anvendelse", 
    layernames = anve_layers,
    wfs_path = wfs_path)

# import attraktioner layers
attr_layers = [
    "besoeg",
    "fortidsminder",
    "landemaerker",
    "udflugt"
]

wfs_dict = addlayers_from_wfsfolder(
    wfs_dict = wfs_dict, 
    wfs_folder = "land_attraktioner", 
    layernames = attr_layers,
    wfs_path = wfs_path)

# import landskabnatur layers (attention, some are missing!!)
land_layers = [
    "beskyttet_natur",
    # should also be: vaerdiful & fredninger 
]

wfs_dict = addlayers_from_wfsfolder(
    wfs_dict = wfs_dict, 
    wfs_folder = "land_landskabnatur", 
    layernames = land_layers,
    wfs_path = wfs_path)

### MAKE NATURE LAYER

# get gdfs from dict
natu = wfs_dict["land_anvendelse"]["naturareal"]
skov = wfs_dict["land_anvendelse"]["skovinddeling"]
besk = wfs_dict["land_landskabnatur"]["beskyttet_natur"]

nature = merge_gdfs(
    [
        natu[-natu["type"].isin(["Råstofomrade"])],
        skov,
        besk,
        # fred, 
        # vaer,    
    ]
    )

print("NATURE layer created")

### MAKE CULTURE LAYER

byom = wfs_dict["land_anvendelse"]["byomraade"]

culture = merge_gdfs(
    [
        byom[byom["type"]=="Bykerne"],
        # MISSING: vaer filtered by "kulturhistorisk..." and "kulturmiljø"
    ]
)

print("CULTURE layer created")

### MAKE SOMMERHUS LAYER

byom = wfs_dict["land_anvendelse"]["byomraade"]

sommerhus = merge_gdfs(
    [
        byom[byom["type"].isin(["Sommerhusområde", "Sommerhusområde skov"])]
    ]
)

print("SOMMERHUS layer created")

### MAKE AGRICULTURE LAYER

agriculture = wfs_dict["land_anvendelse"]["dyrket_areal"] # agriculture!! (separate layer)

print("AGRICULTURE layer created")

### MAKE BAD LAYER

byom = wfs_dict["land_anvendelse"]["byomraade"]
tekn = wfs_dict["land_anvendelse"]["teknisk_areal"]

bad = merge_gdfs(
    [
        byom[byom["type"].isin(["Erhverv", "Høj bebyggelse"])],
        tekn[-tekn["type"].isin(["Sportsanlæg"])]
    ]
)

print("BAD layer created")

### MAKE POIs LAYER

# merge beso, fort, udfl, land; just keep track of what type they are (variation is interesting!)
# in max 1km distance 
beso = wfs_dict["land_attraktioner"]["besoeg"]
fort = wfs_dict["land_attraktioner"]["fortidsminder"]
udfl = wfs_dict["land_attraktioner"]["udflugt"]
land = wfs_dict["land_attraktioner"]["landemaerker"]

pois = merge_gdfs(
    [
        beso,
        fort,
        udfl,
        land
    ]
)

print("POIs layer created")

### MAKE FACILITIES LAYER

# in max 100 m
# all info except for turistkontor ()
# all rasteplads

info = wfs_dict["facilit_faciliteter"]["infoservice"]
infosup = wfs_dict["facilit_faciliteter"]["infoservice_suppl"]
rast = wfs_dict["facilit_faciliteter"]["rasteplads"]
rastsup = wfs_dict["facilit_faciliteter"]["rasteplads_suppl"]

facilities = merge_gdfs(
    [
        info[-info["type"].isin(["turistkontor"])],
        infosup,
        rast,
        rastsup
    ]
)

print("FACILITIES layer created")

### SERVICE layer

# in max 500 m
# all indk; over;
# turistkontor (from info)
indk = wfs_dict["facilit_faciliteter"]["indkoeb"]
info = wfs_dict["facilit_faciliteter"]["infoservice"]
over = wfs_dict["facilit_faciliteter"]["overnatning"]

service = merge_gdfs(
    [
        indk,
        over,
        info[info["type"].isin(["turistkontor"])]
    ]
)

print("SERVICE layer created")

### SAVE TO FILES

os.makedirs(eval_path, exist_ok=True)

agriculture.to_file(eval_path + "/agriculture.gpkg", index=False)
bad.to_file(eval_path + "/bad.gpkg", index=False)
culture.to_file(eval_path +  "/culture.gpkg", index=False)
facilities.to_file(eval_path + "/facilities.gpkg", index=False)
nature.to_file(eval_path + "/nature.gpkg", index=False)
pois.to_file(eval_path + "/pois.gpkg", index=False)
service.to_file(eval_path + "/service.gpkg", index=False)
sommerhus.to_file(eval_path + "/sommerhus.gpkg", index=False)

print(f"All evaluation layers saved to {eval_path}")