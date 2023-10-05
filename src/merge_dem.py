# from https://www.giscourse.com/automatically-merge-raster-files-using-pyqgis/

from pathlib import Path
from osgeo import gdal
import os
import yaml

# define homepath variable (where is the qgis project saved?)
homepath = QgsProject.instance().homePath()
input_path = homepath + "/data/raw/DTM"

output_path = homepath + "/data/processed/merged_dem.tif"

folder = Path(input_path)

l = []

for f in folder.glob("**/*.tif"):
    f_path = f.as_posix()
    l.append(f_path)

vrt_path = os.path.join(input_path, "prov_vrt.vrt")
vrt = gdal.BuildVRT(vrt_path, l)

gdal.Translate(output_path, vrt, format="GTiff")
