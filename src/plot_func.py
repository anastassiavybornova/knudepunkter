from random import randrange

# from qgis.core import QgsVectorLayer
from qgis.core import *


def draw_categorical_layer(
    layer_name,
    column_name,
    outline_color="black",
    outline_width=0.5,
    alpha=180,
    linewidth=1,
    line_style="solid",
    marker_shape="circle",
    marker_size=4,
    marker_angle=45,
):
    # based on https://gis.stackexchange.com/questions/175068/applying-categorized-symbol-to-each-feature-using-pyqgis

    my_layer = QgsProject.instance().mapLayersByName(layer_name)[0]
    iface.setActiveLayer(my_layer)
    layer = iface.activeLayer()

    idx = layer.fields().indexOf(column_name)

    if idx == -1:
        idx = 0

    unique_values = layer.uniqueValues(idx)

    if layer.wkbType() in [QgsWkbTypes.MultiPolygon, QgsWkbTypes.Polygon]:
        properties = {
            "outline_width": outline_width,
            "outline_color": outline_color,
        }

    if layer.wkbType() in [QgsWkbTypes.LineString, QgsWkbTypes.MultiLineString]:
        properties = {"width": linewidth, "line_style": line_style}

    if layer.wkbType() in [QgsWkbTypes.Point, QgsWkbTypes.MultiPoint]:
        properties = {
            "name": marker_shape,
            "size": marker_size,
            "outline_color": outline_color,
            "outline_width": outline_width,
            "angle": marker_angle,
        }

    categories = []
    for unique_value in unique_values:
        symbol = QgsSymbol.defaultSymbol(layer.geometryType())

        properties[
            "color"
        ] = f"{randrange(0, 256)}, {randrange(0, 256)}, {randrange(0, 256)}, {alpha}"

        symbol_layer = QgsSimpleFillSymbolLayer.create(properties)

        # replace default symbol layer with the configured one
        if symbol_layer is not None:
            symbol.changeSymbolLayer(0, symbol_layer)

        # create renderer object
        category = QgsRendererCategory(unique_value, symbol, str(unique_value))

        # entry for the list of category items
        categories.append(category)

    # create renderer object
    renderer = QgsCategorizedSymbolRenderer(column_name, categories)
    layer.setRenderer(renderer)

    layer.triggerRepaint()  # if the layer was already loaded
    iface.layerTreeView().refreshLayerSymbology(layer.id())


def draw_simple_polygon_layer(
    layer_name, color="0,0,0,128", outline_color="black", outline_width=1
):
    # TODO docstring

    my_layer = QgsProject.instance().mapLayersByName(layer_name)[0]
    iface.setActiveLayer(my_layer)
    layer = iface.activeLayer()

    properties = {
        "color": color,
        "outline_color": outline_color,
        "outline_width": outline_width,
    }

    symbol = QgsFillSymbol.createSimple(properties)

    layer.renderer().setSymbol(symbol)
    layer.triggerRepaint()  # if the layer was already loaded
    iface.layerTreeView().refreshLayerSymbology(layer.id())


def draw_simple_line_layer(layer_name, color="purple", width=1, line_style="solid"):
    # TODO: Docstring

    my_layer = QgsProject.instance().mapLayersByName(layer_name)[0]
    iface.setActiveLayer(my_layer)
    layer = iface.activeLayer()

    properties = {"color": color, "width": width, "line_style": line_style}

    symbol = QgsLineSymbol.createSimple(properties)

    renderer = QgsSingleSymbolRenderer(symbol)
    layer.setRenderer(renderer)
    layer.triggerRepaint()
    iface.layerTreeView().refreshLayerSymbology(layer.id())


def draw_simple_point_layer(
    layer_name,
    marker_shape="circle",
    marker_size=4,
    color="0,0,0,128",
    outline_color="black",
    outline_width=1,
    marker_angle=45,
):
    # TODO: Docstring

    my_layer = QgsProject.instance().mapLayersByName(layer_name)[0]
    iface.setActiveLayer(my_layer)
    layer = iface.activeLayer()

    properties = {
        "name": marker_shape,
        "size": marker_size,
        "color": color,
        "outline_color": outline_color,
        "outline_width": outline_width,
        "angle": marker_angle,
    }
    symbol = QgsMarkerSymbol.createSimple(properties)
    renderer = QgsSingleSymbolRenderer(symbol)
    layer.setRenderer(renderer)
    layer.triggerRepaint()
    iface.layerTreeView().refreshLayerSymbology(layer.id())


def draw_recent_simple_line_layer(color="purple", width=0.7, line_style="solid"):
    symbol = QgsLineSymbol.createSimple(
        {"color": color, "width": width, "line_style": line_style}
    )
    renderer = QgsSingleSymbolRenderer(symbol)
    iface.activeLayer().setRenderer(renderer)
    iface.activeLayer().triggerRepaint()
    iface.layerTreeView().refreshLayerSymbology(iface.activeLayer().id())


def remove_existing_layers(layer_name_tuple):
    existing_layers_ids = [
        layer.id() for layer in QgsProject.instance().mapLayers().values()
    ]
    remove_layers = [e for e in existing_layers_ids if e.startswith(layer_name_tuple)]

    for r in remove_layers:
        QgsProject.instance().removeMapLayer(r)

    return None


# def visualize_categorical(layer_name, column_name, width=1):
#     # based on https://gis.stackexchange.com/questions/175068/applying-categorized-symbol-to-each-feature-using-pyqgis

#     my_layer = QgsProject.instance().mapLayersByName(layer_name)[0]
#     iface.setActiveLayer(my_layer)
#     layer = iface.activeLayer()

#     idx = layer.fields().indexOf(column_name)

#     if idx == -1:
#         idx = 0

#     unique_values = layer.uniqueValues(idx)

#     categories = []
#     for unique_value in unique_values:
#         # initialize the default symbol for this geometry type
#         symbol = QgsSymbol.defaultSymbol(layer.geometryType())
#         print(type(symbol))
#         # configure a symbol layer
#         layer_style = {}
#         layer_style["color"] = "%d, %d, %d" % (
#             randrange(0, 256),
#             randrange(0, 256),
#             randrange(0, 256),
#         )
#         layer_style["outline"] = "#000000"
#         symbol_layer = QgsSimpleFillSymbolLayer.create(layer_style)

#         # replace default symbol layer with the configured one
#         if symbol_layer is not None:
#             symbol.changeSymbolLayer(0, symbol_layer)

#         # create renderer object
#         category = QgsRendererCategory(unique_value, symbol, str(unique_value))

#         # entry for the list of category items
#         categories.append(category)

#     # create renderer object
#     renderer = QgsCategorizedSymbolRenderer(column_name, categories)

#     # assign the created renderer to the layer
#     if renderer is not None:
#         layer.setRenderer(renderer)

#     layer.triggerRepaint()
#     iface.layerTreeView().refreshLayerSymbology(layer.id())
