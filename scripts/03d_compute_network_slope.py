# Compute slope for edge segments and whole edges

### *********
### CUSTOM SETTINGS
### *********

segment_length = 100  # max segment length in meters

plot_intermediate = True
plot_results = True

dataforsyning_token = "fc5f46c60194d0833dbc2b219b6d500a"

# import python packages
import os

os.environ["USE_PYGEOS"] = "0"  # pygeos/shapely2.0/osmnx conflict solving
from owslib.wms import WebMapService
import geopandas as gpd
import yaml

# define homepath variable (where is the qgis project saved?)
homepath = QgsProject.instance().homePath()

# filepaths

edges_fp = homepath + "/data/processed/workflow_steps/qgis_output_beta.gpkg"
edges_id_fp = (
    homepath + "/data/processed/workflow_steps/qgis_output_beta_unique_id.gpkg"
)
elevation_vals_segments_fp = (
    homepath + "/data/processed/workflow_steps/elevation_values_segments.gpkg"
)
elevation_vals_edges_fp = (
    homepath + "/data/processed/workflow_steps/elevation_values_edges.gpkg"
)
segments_fp = homepath + "/data/processed/workflow_steps/segments.gpkg"

segments_slope_fp = homepath + "/results/data/segments_slope.gpkg"
edges_slope_fp = homepath + "/results/data/edges_slope.gpkg"

dem_fp = homepath + "/data/processed/merged_dem.tif"

# load configs
configfile = os.path.join(homepath, "config.yml")  # filepath of config file
configs = yaml.load(open(configfile), Loader=yaml.FullLoader)
proj_crs = configs["proj_crs"]

# import functions
exec(open(homepath + "/src/plot_func.py").read())

# prepare DEM
exec(open(homepath + "/src/merge_dem.py").read())

# Remove layers from project if they exist already
remove_existing_layers(
    [
        "Network edges",
        "Split",
        "Segments",
        "Vertices",
        "Elevation values",
        "dhm_terraen_skyggekort",
        "dem_terrain",
        "Segments slope",
        "Edges slope",
    ]
)

edges = gpd.read_file(edges_fp)

edges["edge_id"] = edges.index
assert len(edges) == len(edges.edge_id.unique())

edges.to_file(edges_id_fp)

# import study area edges
vlayer_edges = QgsVectorLayer(edges_id_fp, "Network edges", "ogr")

if plot_intermediate:
    QgsProject.instance().addMapLayer(vlayer_edges)

    draw_simple_line_layer(
        "Network edges", color="black", line_width=1, line_style="solid"
    )

# import dem
dem_terrain = QgsRasterLayer(dem_fp, "dem_terrain")

if plot_intermediate:
    QgsProject.instance().addMapLayer(dem_terrain)

# plot hill shade
if plot_intermediate and dataforsyning_token is not None:
    dem_name = "dhm_terraen_skyggekort"
    wms_url_new = (
        "https://api.dataforsyningen.dk/dhm_DAF?" + f"token={dataforsyning_token}"
    )
    source_new = f"crs={proj_crs}&dpiMode=7&format=image/png&layers={dem_name}&styles&tilePixelRatio=0&url={wms_url_new}"

    dem_raster = QgsRasterLayer(source_new, dem_name, "wms")

    QgsProject.instance().addMapLayer(dem_raster)

    print("added dem raster")


#### GET SLOPE FOR EDGE SEGMENTS ######

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

# create new unique segment id
segments_temp_layer.dataProvider().addAttributes([QgsField("segment_id", QVariant.Int)])
segments_temp_layer.updateFields()
fld_idx = segments_temp_layer.fields().lookupField("segment_id")
atts_map = {ft.id(): {fld_idx: ft.id()} for ft in segments_temp_layer.getFeatures()}
segments_temp_layer.dataProvider().changeAttributeValues(atts_map)

# export
_writer = QgsVectorFileWriter.writeAsVectorFormat(
    segments_temp_layer,
    segments_fp,
    "utf-8",
    segments_temp_layer.crs(),
    "GPKG",
)

vlayer_segments = QgsVectorLayer(
    segments_fp,
    "Segments",
    "ogr",
)

if plot_intermediate:
    QgsProject.instance().addMapLayer(vlayer_segments)

    draw_simple_line_layer("Segments", color="red", line_width=1, line_style="dash")

print(f"done: line split into segments of max length {segment_length} meters.")

# GET START AND END VERTICES
segment_vertices = processing.run(
    "native:extractspecificvertices",
    {
        "INPUT": vlayer_segments,
        "VERTICES": "0,-1",
        "OUTPUT": "TEMPORARY_OUTPUT",
    },
)

if plot_intermediate:
    QgsProject.instance().addMapLayer(segment_vertices["OUTPUT"])

    vertices = QgsProject.instance().mapLayersByName("Vertices")[0]

    draw_simple_point_layer(
        "Vertices",
        color="0,0,0,180",
        marker_size=1,
        outline_width=0,
    )
print(f"done: extracted segment start and end points")

elevation_values = processing.run(
    "native:rastersampling",
    {
        "INPUT": segment_vertices["OUTPUT"],
        "RASTERCOPY": dem_terrain,
        "COLUMN_PREFIX": "elevation_",
        "OUTPUT": "TEMPORARY_OUTPUT",  # elevation_vals_fp,
    },
)

# export
elevation_temp_layer = elevation_values["OUTPUT"]
# delete "fid" field (to prevent problems when exporting a layer with non-unique fields)
layer_provider = elevation_temp_layer.dataProvider()
fid_idx = elevation_temp_layer.fields().indexOf("fid")
elevation_temp_layer.dataProvider().deleteAttributes([fid_idx])
elevation_temp_layer.updateFields()

_writer = QgsVectorFileWriter.writeAsVectorFormat(
    elevation_temp_layer,
    elevation_vals_segments_fp,
    "utf-8",
    elevation_temp_layer.crs(),
    "GPKG",
)

vlayer_elevation = QgsVectorLayer(
    elevation_vals_fp,
    "Elevation values segments",
    "ogr",
)
if plot_intermediate:
    QgsProject.instance().addMapLayer(vlayer_elevation)

    draw_simple_point_layer(
        "Elevation values segments",
        color="255,0,0,180",
        marker_size=2,
        outline_color="white",
        outline_width=0.2,
    )

ele = gpd.read_file(elevation_vals_segments_fp)
segs = gpd.read_file(segments_fp)


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

segs["slope"].fillna(0, inplace=True)

segs.to_file(segments_slope_fp)

vlayer_slope = QgsVectorLayer(
    segments_slope_fp,
    "Segments slope",
    "ogr",
)

if plot_results:
    QgsProject.instance().addMapLayer(vlayer_slope)

    draw_linear_graduated_layer(
        "Segments slope",
        "slope",
        10,
        cmap="Reds",
        alpha=255,
        line_width=1.5,
        line_style="solid",
    )

### GET SLOPE FOR EDGES ######

# Avoid double vertice layer
remove_existing_layers(
    [
        "Vertices",
    ]
)
# Get start end end vertices for edges
edge_vertices = processing.run(
    "native:extractspecificvertices",
    {
        "INPUT": vlayer_edges,
        "VERTICES": "0,-1",
        "OUTPUT": "TEMPORARY_OUTPUT",
    },
)

print(f"done: extracted edge start and end points")

if plot_intermediate:
    QgsProject.instance().addMapLayer(edge_vertices["OUTPUT"])

    vertices = QgsProject.instance().mapLayersByName("Vertices")[0]

    draw_simple_point_layer(
        "Vertices",
        color="0,0,0,180",
        marker_size=1,
        outline_width=0.0,
    )

elevation_values_edges = processing.run(
    "native:rastersampling",
    {
        "INPUT": edge_vertices["OUTPUT"],
        "RASTERCOPY": dem_terrain,
        "COLUMN_PREFIX": "elevation_",
        "OUTPUT": "TEMPORARY_OUTPUT",
    },
)

# export
elevation_temp_layer_edges = elevation_values_edges["OUTPUT"]
# delete "fid" field (to prevent problems when exporting a layer with non-unique fields)
layer_provider = elevation_temp_layer_edges.dataProvider()
fid_idx = elevation_temp_layer_edges.fields().indexOf("fid")
elevation_temp_layer_edges.dataProvider().deleteAttributes([fid_idx])
elevation_temp_layer_edges.updateFields()

_writer = QgsVectorFileWriter.writeAsVectorFormat(
    elevation_temp_layer_edges,
    elevation_vals_edges_fp,
    "utf-8",
    elevation_temp_layer_edges.crs(),
    "GPKG",
)

vlayer_elevation = QgsVectorLayer(
    elevation_vals_edges_fp,
    "Elevation values edges",
    "ogr",
)
if plot_intermediate:
    QgsProject.instance().addMapLayer(vlayer_elevation)

    draw_simple_point_layer(
        "Elevation values edges",
        color="255,0,0,180",
        marker_size=2,
        outline_color="white",
        outline_width=0.2,
    )

ele = gpd.read_file(elevation_vals_edges_fp)

elevation_col = "elevation_1"
grouped = ele.groupby("edge_id")

edges["slope"] = None

for edge_id, group in grouped:
    if len(group) != 2:
        print(f"Error, got {len(group)} row(s)")
    else:
        e1 = group[elevation_col].values[0]
        e2 = group[elevation_col].values[1]
        edge_length = edges.loc[edges.edge_id == edge_id].geometry.length.values[0]

        slope = (e2 - e1) / (edge_length - 0)

        edges["slope"].loc[edges.edge_id == edge_id] = abs(slope) * 100

edges["slope"].fillna(0, inplace=True)

# Get min, max ave slope for edge from edge segments
edges["min_slope"] = None
edges["max_slope"] = None
edges["ave_slope"] = None

grouped = segs.groupby("edge_id")

for edge_id, group in grouped:
    min_slope = group["slope"].min()
    max_slope = group["slope"].max()
    ave_slope = group["slope"].mean()

    edges["min_slope"].loc[edges.edge_id == edge_id] = min_slope
    edges["max_slope"].loc[edges.edge_id == edge_id] = max_slope
    edges["ave_slope"].loc[edges.edge_id == edge_id] = ave_slope

edges.to_file(edges_slope_fp)

vlayer_edge_slope = QgsVectorLayer(
    edges_slope_fp,
    "Edges slope",
    "ogr",
)

if plot_results:
    QgsProject.instance().addMapLayer(vlayer_edge_slope)

    draw_linear_graduated_layer(
        "Edges slope",
        "slope",
        10,
        cmap="Reds",
        alpha=255,
        line_width=1.5,
        line_style="solid",
    )


if plot_intermediate == True and plot_results == True:
    group_layers(
        "Get network slope",
        [
            "dhm_terraen_skyggekort",
            "dem_terrain",
            "Network edges",
            "Segments",
            "Vertices",
            "Segments slope",
            "Edges slope",
            "Elevation values segments",
            "Elevation values edges",
        ],
        remove_group_if_exists=True,
    )


if plot_intermediate == False and plot_results == True:
    group_layers(
        "Get network slope",
        [
            "Segments slope",
            "Edges slope",
        ],
        remove_group_if_exists=True,
    )


if plot_intermediate == True and plot_results == False:
    group_layers(
        "Get network slope",
        [
            "dhm_terraen_skyggekort",
            "dem_terrain",
            "Network edges",
            "Segments",
            "Vertices",
            "Elevation values segments",
            "Elevation values edges",
        ],
        remove_group_if_exists=True,
    )


print(f"Maximum slope is {segs.slope.max():.2f} %")
print(f"Average slope is {segs.slope.mean():.2f} %")
