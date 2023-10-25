# NOTE: This script will take a while

# based on https://geoscripting-wur.github.io/PythonRaster/

from owslib.wcs import WebCoverageService
import os
import geopandas as gpd
import numpy as np
import yaml

# define paths
configfile = os.path.join(homepath, "config.yml")  # filepath of config file
study_area_path = os.path.join(homepath, "data/raw/user_input/study_area.gpkg")

# load configs
configs = yaml.load(open(configfile), Loader=yaml.FullLoader)
proj_crs = configs["proj_crs"]
datafordeler_username = configs["datafordeler_username"]
datafordeler_password = configs["datafordeler_password"]

wcs_url = f"https://services.datafordeler.dk/DHMNedboer/dhm_wcs/1.0.0/WCS?username={datafordeler_username}&password={datafordeler_password}&service=WCS&request=GetCapabilities"

if not os.path.exists(homepath + "/data/raw/DEM"):
    os.mkdir(homepath + "/data/raw/DEM")

sa = gpd.read_file(study_area_path)

# Access the WCS by proving the url and optional arguments
wcs = WebCoverageService(
    "https://services.datafordeler.dk/DHMNedboer/dhm_wcs/1.0.0/WCS?username=MAKKFGPILT&password=Testing23!&service=WCS&request=GetCapabilities",
    version="1.0.0",
)

coverage_name = "dhm_terraen"

size = 5000  # dimensions km
resx = 10  # pixel size
resy = 10
width = int(size / resx)  # dimensions of tif
height = int(size / resy)

assert width < 10000  # max size allowed
assert height < 10000

xmin, ymin, xmax, ymax = sa.total_bounds

cols = list(np.arange(xmin, xmax + size, size))
rows = list(np.arange(ymin, ymax + size, size))
bboxes = []

for x in cols:
    for y in rows:
        box = (x, y, x + size, y + size)
        bboxes.append(box)

assert len(bboxes) == len(cols) * len(rows)

try:
    for i, bbox in enumerate(bboxes):
        # Request the DSM data from the WCS
        response = wcs.getCoverage(
            identifier=coverage_name,
            bbox=bbox,
            format="GTiff",
            crs=f"urn:ogc:def:crs:{proj_crs}",
            resx=0.4,
            resy=0.4,
            width=width,
            height=height,
        )

        with open(homepath + f"/data/raw/DEM/{coverage_name}_{i}.tif", "wb") as file:
            file.write(response.read())

except:
    i = i - 1

    for i, bbox in enumerate(bboxes[i:]):
        # Request the DSM data from the WCS
        response = wcs.getCoverage(
            identifier=coverage_name,
            bbox=bbox,
            format="GTiff",
            crs=f"urn:ogc:def:crs:{proj_crs}",
            resx=0.4,
            resy=0.4,
            width=width,
            height=height,
        )

        with open(homepath + f"/data/raw/DEM/{coverage_name}_{i}.tif", "wb") as file:
            file.write(response.read())
