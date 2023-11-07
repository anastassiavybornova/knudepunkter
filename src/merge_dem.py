# from https://www.giscourse.com/automatically-merge-raster-files-using-pyqgis/

from pathlib import Path
from osgeo import gdal
import os
import yaml

# define homepath variable (where is the qgis project saved?)
homepath = QgsProject.instance().homePath()

# define paths
configfile = os.path.join(homepath, "config.yml")  # filepath of config file

# load configs
configs = yaml.load(open(configfile), Loader=yaml.FullLoader)
sa_name = configs["study_area_name"]

# input rasters
input_path = homepath + f"/data/raw/DEM/DEM_{sa_name}"

output_path = homepath + f"/data/processed/workflow_steps/merged_dem_{sa_name}.tif"

folder = Path(input_path)

l = []

for f in folder.glob("**/*.tif"):
    f_path = f.as_posix()
    l.append(f_path)

vrt_path = os.path.join(input_path, "prov_vrt.vrt")
vrt = gdal.BuildVRT(vrt_path, l)

gdal.Translate(output_path, vrt, format="GTiff")
