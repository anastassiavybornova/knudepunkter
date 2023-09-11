# merge data from shapefiles into layers

# DISCARDED:
# land_anvendelse/dyrket_areal.gpkg
# PARTS OF land_anvendelse/byomrade.gpkg
# "type" is "Lav bebyggelse"

# BAD:
# land_anvendelse/teknisk_areal.gpkg, 
# PARTS OF land_anvendelse/byomrade.gpkg
# ("type" in ["Erhverv", "Høj bebyggelse"])

# GOOD: 
# PARTS OF land_anvendelse/byomrade.gpkg
# land_anvendelse/skovinddeling.gpkg
# land_anvendelse/naturareal.gpkg

# CULTURE
# PARTS of land_anvendelse/byomrade.gpkg:
# "type" is Bykerne

# SOMMERHUS:
# PARTS OF land_anvendelse/byomrade.gpkg: 
# "type" in ['Sommerhusområde', 'Sommerhusområde skov']


import os
os.environ['USE_PYGEOS'] = '0' # pygeos/shapely2.0/osmnx conflict solving
import geopandas as gpd
from collections import Counter

# define paths
homepath = (
    QgsProject.instance().homePath()
)  # homepath variable (where is the qgis project saved?)

# import byområde file
gdf = gpd.read_file(homepath + "/data/raw/wfs/land_anvendelse/byomraade.gpkg")

print(Counter(gdf["type"]))