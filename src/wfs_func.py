from owslib.wfs import WebFeatureService
import os


def get_bounds(gdf):
    bounds = gdf.bounds
    minx = bounds.minx[0]
    miny = bounds.miny[0]
    maxx = bounds.maxx[0]
    maxy = bounds.maxy[0]

    return minx, miny, maxx, maxy


def fix_geometries(input_layer):
    fixed_layer = processing.run(
        "native:fixgeometries", {"INPUT": input_layer, "OUTPUT": "memory:"}
    )["OUTPUT"]

    return fixed_layer


def clip_save_layer(input_layer, study_area_vlayer, filepath, layer_name):
    clip_params = {
        "INPUT": input_layer,
        "OVERLAY": study_area_vlayer,
        "OUTPUT": filepath,
    }

    # clip to study area polygon
    processing.run("native:clip", clip_params)

    print(f"Saved {layer_name} layer")

    return None


def get_wfs_layers(
    study_area_vlayer,
    bounds,
    wfs_core,
    wfs,
    wfs_version,
    homepath,
    proj_crs,
    show_layer,
):
    # define bounds
    minx, miny, maxx, maxy = bounds

    # define WFS URL
    wfs_url_get = wfs_core + "&request=GetCapabilities"
    wfs = WebFeatureService(url=wfs_url_get, version=wfs_version)

    layers_to_import = list(wfs.contents)

    print("Importing layers:", layers_to_import, "from WFS: ", wfs)

    wfs_dir = homepath + f"/data/raw/wfs/"

    if not os.path.isdir(wfs_dir):
        os.mkdir(wfs_dir)

    wfs_layer_dir = homepath + f"/data/raw/wfs/{wfs}/"

    if not os.path.isdir(wfs_layer_dir):
        os.mkdir(wfs_layer_dir)

    for layer in layers_to_import:
        filepath = wfs_layer_dir + layer + ".gpkg"

        print("Getting data for layer:", layer)

        wfs_url = (
            wfs_core
            + f"&request=GetFeature&typeName={layer}&SRSName=EPSG:25832&BBOX={minx},{miny},{maxx},{maxy}"
        )

        Source = f"pagingEnabled='true' preferCoordinatesForWfsT11='false' restrictToRequestBBOX='1' srsname={proj_crs} typename={layer} url={wfs_url} version='auto'"

        # initialize vector layer of WFS features
        temp_layer = QgsVectorLayer(Source, layer, "WFS")

        fixed_layer = fix_geometries(temp_layer)

        clip_save_layer(fixed_layer, study_area_vlayer, filepath, layer)

        if show_layer:
            new_layer = QgsVectorLayer(filepath, layer, "ogr")
            QgsProject.instance().addMapLayer(new_layer)
            print(f"Added {layer} layer")
