# merge data from WFS layers (downloaded into gpkg files in /wfs/ folder in 03a_get_septima_data) 
# into layers for evaluation


# NATURE:
# landanvendelse of type naturareal (all subtypes)
# landanvendelse of type skovinddeling (all subtypes)
# landskabnatur of type beskyttet natur (all subtypes)

# SOMMERHUS:
# PARTS OF land_anvendelse/byomrade.gpkg: 
# "type" in ['Sommerhusområde', 'Sommerhusområde skov']

# GOOD: 
# PARTS OF land_anvendelse/byomrade.gpkg
# land_anvendelse/skovinddeling.gpkg
# land_anvendelse/naturareal.gpkg

# CULTURE
# landanvendelse of type byomrade of subtype Bykerne
 
# BAD:
# landanvendelse of type Bymæssig anvendelse (only subtypes erhverh, høj bebyggelse) 
# landanvendelse of type Teknisk areal (all subtypes)



# DISCARDED:
# land_anvendelse/dyrket_areal.gpkg
# PARTS OF land_anvendelse/byomrade.gpkg
# "type" is "Lav bebyggelse"


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