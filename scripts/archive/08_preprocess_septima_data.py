# to import and CUT septima data, then save it separately by reached / not reached and import it back to plot
# * current: data is downloaded from septima website, saved locally and then read in through geopandas
# * future: data is imported and bbox-filtered directly as a WFS layer through pyqgis (see commented-out code)

# import libraries
import os
os.environ["USE_PYGEOS"] = '0'
import geopandas as gpd

# define homepath variable (where is the qgis project saved?)
homepath = QgsProject.instance().homePath()

# get septima data
gdf = gpd.read_file(homepath + "/data/raw/septima/land_landemaerke/land_landemaerke.shp")

# get buffered bounding box of study area polygon
study_area = gpd.read_file(homepath + "/data/raw/user_input/study_area.gpkg")
study_area_bbox = study_area.envelope.buffer(500)

# cut data to study area polygon
gdf = gdf[gdf.intersects(study_area_bbox[0])].copy().reset_index(drop=True)

# save for further use
gdf.to_file(homepath + "/data/processed/septima/land_landemaerke/land_landemaerke.gpkg", index = False)

# import matplotlib.pyplot as plt
# fig, ax = plt.subplots(1,1)
# gdf.plot(ax=ax)
# study_area_bbox.plot(ax=ax, alpha = 0.1)