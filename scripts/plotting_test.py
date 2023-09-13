from random import randrange


homepath = QgsProject.instance().homePath()

test_line = "Edges (beta)"
test_poly = "Study area"
test_point = "Nodes (beta)"
test_poly_cat = "test_poly"


def draw_categorical_layer(
    layer_name,
    column_name,
    outline_color="black",
    outline_width=0.5,
    alpha=180,
    line_style="solid",
    marker_shape="circle",
    marker_size=4,
    marker_angle=45,
):
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
        properties = {"width": width, "line_style": line_style}

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


draw_categorical_layer(layer_name=test_poly_cat, column_name="grid_id")


def draw_categorical_point_layer():
    pass


def draw_categorical_line_layer():
    pass


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

    layer.renderer().setSymbol(symbol)
    layer.triggerRepaint()  # if the layer was already loaded
    iface.layerTreeView().refreshLayerSymbology(layer.id())


draw_simple_point_layer(test_point)
draw_simple_line_layer(layer_name=test_line, color="0,0,0,70", line_style="dash")
draw_simple_polygon_layer(layer_name=test_poly)


#### **** #####


def visualize_categorical(layer_name, column_name):
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
        properties = {}
        properties["color"] = "%d, %d, %d" % (
            randrange(0, 256),
            randrange(0, 256),
            randrange(0, 256),
        )
        properties["outline"] = "#000000"
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

    # assign the created renderer to the layer
    if renderer is not None:
        layer.setRenderer(renderer)

    layer.triggerRepaint()
    iface.layerTreeView().refreshLayerSymbology(layer.id())
