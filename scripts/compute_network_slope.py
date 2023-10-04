### *********
### CUSTOM SETTINGS
### *********

segment_length = 100  # max segment length in meters

# import python packages
import os

os.environ["USE_PYGEOS"] = "0"  # pygeos/shapely2.0/osmnx conflict solving
from owslib.wms import WebMapService
import geopandas as gpd
import yaml
from src import wfs_func

# define homepath variable (where is the qgis project saved?)
homepath = QgsProject.instance().homePath()
line_segments_fp = homepath + "/data/processed/workflow_steps/line_segments.gpkg"
line_segments_slope_fp = (
    homepath + "/data/processed/workflow_steps/line_segments_slope.gpkg"
)
elevation_vals_fp = homepath + "/data/processed/workflow_steps/elevation_values.gpkg"

# load configs
configfile = os.path.join(homepath, "config.yml")  # filepath of config file
configs = yaml.load(open(configfile), Loader=yaml.FullLoader)
proj_crs = configs["proj_crs"]

# import functions
exec(open(homepath + "/src/plot_func.py").read())

# Remove layers from project if they exist already
remove_existing_layers(
    [
        "Network edges",
        "Split",
        "Line segments",
        "Vertices",
        "Elevation values",
        "dhm_terraen_skyggekort",
    ]
)

# edges filepath
edges_fp = homepath + "/data/processed/workflow_steps/qgis_output_beta.gpkg"

# import study area edges
vlayer_edges = QgsVectorLayer(edges_fp, "Network edges", "ogr")

QgsProject.instance().addMapLayer(vlayer_edges)

# segmentize
line_segments = processing.run(
    "native:splitlinesbylength",
    {"INPUT": vlayer_edges, "LENGTH": segment_length, "OUTPUT": "TEMPORARY_OUTPUT"},
)

# delete "fid" field (to prevent problems when exporting a layer with non-unique fields)
segments_temp_layer = line_segments["OUTPUT"]
layer_provider = segments_temp_layer.dataProvider()
fid_idx = segments_temp_layer.fields().indexOf("fid")
segments_temp_layer.dataProvider().deleteAttributes([fid_idx])
segments_temp_layer.updateFields()

# export
_writer = QgsVectorFileWriter.writeAsVectorFormat(
    segments_temp_layer,
    line_segments_fp,
    "utf-8",
    segments_temp_layer.crs(),
    "GPKG",
)

vlayer_segments = QgsVectorLayer(
    line_segments_fp,
    "Line segments",
    "ogr",
)
QgsProject.instance().addMapLayer(vlayer_segments)

print(f"done: line split into segments of max length {segment_length} meters.")

# create new unique segment id
vlayer_segments.dataProvider().addAttributes([QgsField("segment_id", QVariant.Int)])
vlayer_segments.updateFields()
fld_idx = vlayer_segments.fields().lookupField("segment_id")
atts_map = {ft.id(): {fld_idx: ft.id()} for ft in vlayer_segments.getFeatures()}
vlayer_segments.dataProvider().changeAttributeValues(atts_map)


# Get start end end vertices for segments
line_vertices = processing.run(
    "native:extractspecificvertices",
    {
        "INPUT": vlayer_segments,
        "VERTICES": "0,-1",
        "OUTPUT": "TEMPORARY_OUTPUT",
    },
)

QgsProject.instance().addMapLayer(line_vertices["OUTPUT"])

print(f"done: extracted line start and end points")

# define bounds
# study_area_path = os.path.join(homepath, "data/raw/user_input/study_area.gpkg")
# study_area_gdf = gpd.read_file(study_area_path)
# bounds = wfs_func.get_bounds(study_area_gdf)
# minx, miny, maxx, maxy = bounds

# dataforsyning_token = "fc5f46c60194d0833dbc2b219b6d500a"
# dem_name = "dhm_terraen_skyggekort"
# wms_url_new = "https://api.dataforsyningen.dk/dhm_DAF?" + f"token={dataforsyning_token}"

# source_new = f"crs={proj_crs}&dpiMode=7&format=image/png&layers={dem_name}&styles&tilePixelRatio=0&url={wms_url_new}"

# dem_raster = QgsRasterLayer(source_new, dem_name, "wms")

# QgsProject.instance().addMapLayer(dem_raster)

# # TODO: make sure it is below other layers

# print("added dem raster")

# TODO: read raster
# TODO: clip to study area

test_vertices = QgsProject.instance().mapLayersByName("test_vertices")[0]  # UPDATE
test_dem = QgsProject.instance().mapLayersByName("test_dem")[0]  # UPDATE

elevation_values = processing.run(
    "native:rastersampling",
    {
        "INPUT": test_vertices,
        "RASTERCOPY": test_dem,
        "COLUMN_PREFIX": "elevation_",
        "OUTPUT": elevation_vals_fp,
    },
)

vlayer_elevation = QgsVectorLayer(
    elevation_vals_fp,
    "Elevation values",
    "ogr",
)
QgsProject.instance().addMapLayer(vlayer_elevation)


ele = gpd.read_file(elevation_vals_fp)
segs = gpd.read_file(line_segments_fp)

slopes_pct = {}

elevation_col = "elevation_1"
grouped = ele.groupby("segment_id")

segs["slope"] = None

for seg_id, group in grouped:
    if len(group) != 2:
        print(f"Error, got {len(group)} row(s)")
    else:
        e1 = group[elevation_col].values[0]
        e2 = group[elevation_col].values[1]
        seg_length = segs.loc[segs.segment_id == seg_id].geometry.length.values[0]

        slope = (e2 - e1) / (seg_length - 0)

        segs["slope"].loc[segs.segment_id == seg_id] = abs(slope) * 100
        slopes_pct[seg_id] = abs(slope) * 100

segs["slope"].fillna(0, inplace=True)
segs.to_file(line_segments_slope_fp)

vlayer_slope = QgsVectorLayer(
    line_segments_slope_fp,
    "Segments slope",
    "ogr",
)
QgsProject.instance().addMapLayer(vlayer_slope)

draw_linear_graduated_layer(
    "Segments slope",
    "slope",
    5,
    cmap="Reds",
    alpha=180,
    line_width=1,
    line_style="solid",
)


group_layers(
    "Get network slope",
    [
        "Line segments",
        "Vertices",
        "Elevation values",
        "Network edges",
        "Segments slope",
    ],
    remove_group_if_exists=True,
)

# TODO: aggregate
# TODO: save info to input edges?
