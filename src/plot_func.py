from random import randrange

# from qgis.core import QgsVectorLayer
from qgis.core import *


def draw_recent_simple_line_layer(color="purple", width=0.7, line_style="solid"):
    symbol = QgsLineSymbol.createSimple(
        {"color": color, "width": width, "line_style": line_style}
    )
    renderer = QgsSingleSymbolRenderer(symbol)
    iface.activeLayer().setRenderer(renderer)
    iface.activeLayer().triggerRepaint()
    iface.layerTreeView().refreshLayerSymbology(iface.activeLayer().id())


def draw_simple_line_layer(layer_name, color="purple", width=0.7, line_style="solid"):
    symbol = QgsLineSymbol.createSimple(
        {"color": color, "width": width, "line_style": line_style}
    )
    my_layer = QgsProject.instance().mapLayersByName(layer_name)[0]
    iface.setActiveLayer(my_layer)
    layer = iface.activeLayer()

    renderer = QgsSingleSymbolRenderer(symbol)
    layer.setRenderer(renderer)
    layer.triggerRepaint()
    iface.layerTreeView().refreshLayerSymbology(layer.id())


def remove_existing_layers(layer_name_tuple):
    existing_layers_ids = [
        layer.id() for layer in QgsProject.instance().mapLayers().values()
    ]
    remove_layers = [e for e in existing_layers_ids if e.startswith(layer_name_tuple)]

    for r in remove_layers:
        QgsProject.instance().removeMapLayer(r)

    return None


def visualize_categorical(layer_name, column_name, width=1):
    # based on https://gis.stackexchange.com/questions/175068/applying-categorized-symbol-to-each-feature-using-pyqgis

    my_layer = QgsProject.instance().mapLayersByName(layer_name)[0]
    iface.setActiveLayer(my_layer)
    layer = iface.activeLayer()

    idx = layer.fields().indexOf(column_name)

    if idx == -1:
        idx = 0

    unique_values = layer.uniqueValues(idx)

    categories = []
    for unique_value in unique_values:
        # initialize the default symbol for this geometry type
        symbol = QgsSymbol.defaultSymbol(layer.geometryType())
        print(type(symbol))
        # configure a symbol layer
        layer_style = {}
        layer_style["color"] = "%d, %d, %d" % (
            randrange(0, 256),
            randrange(0, 256),
            randrange(0, 256),
        )
        layer_style["outline"] = "#000000"
        symbol_layer = QgsSimpleFillSymbolLayer.create(layer_style)

        # replace default symbol layer with the configured one
        if symbol_layer is not None:
            symbol.changeSymbolLayer(0, symbol_layer)

        # create renderer object
        category = QgsRendererCategory(unique_value, symbol, str(unique_value))

        # entry for the list of category items
        categories.append(category)

    # create renderer object
    renderer = QgsCategorizedSymbolRenderer(column_name, categories)

    # assign the created renderer to the layer
    if renderer is not None:
        layer.setRenderer(renderer)

    layer.triggerRepaint()
    iface.layerTreeView().refreshLayerSymbology(layer.id())
