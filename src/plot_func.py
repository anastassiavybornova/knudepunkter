from random import randrange

# from qgis.core import QgsVectorLayer
from qgis.core import *


def zoom_to_layer(layer_name):
    """
    Zoom to layer extent

    Arguments:
        input_layer (str): name of vector layer to zoom to

    Returns:
        None
    """
    layer = QgsProject.instance().mapLayersByName(layer_name)[0]
    # iface.setActiveLayer(my_layer)
    # layer = iface.activeLayer()

    canvas = iface.mapCanvas()
    extent = layer.extent()
    canvas.setExtent(extent)
    canvas.refresh()


def draw_categorical_layer(
    layer_name,
    attr_name,
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
    """
    Plot layer based on categorical values with random colors

    Arguments:
        layer_name (str): name of layer to plot
        attr_name (str): name of attribute with categorical values
        outline_color (str): color to use for outline color for points and polygons
        outline_width (numerical): width of outline for points and polygons
        alpha (numerical): value between 0 and 255 setting the transparency of the fill color
        linewidth (numerical): width of line features
        line_style (string): line style (e.g. solid or dash). Must be valid line style type
        marker_shape (string): shape of marker for point features. Must be valid shape name
        marker_size (numerical): size of marker for point features
        marker_angle (numerical): value between 0 and 360 indicating the angle of marker for point objects

    Returns:
        None
    """

    layer = QgsProject.instance().mapLayersByName(layer_name)[0]
    # iface.setActiveLayer(my_layer)
    # layer = iface.activeLayer()

    idx = layer.fields().indexOf(attr_name)

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
    renderer = QgsCategorizedSymbolRenderer(attr_name, categories)
    layer.setRenderer(renderer)

    layer.triggerRepaint()  # if the layer was already loaded
    iface.layerTreeView().refreshLayerSymbology(layer.id())


def draw_simple_polygon_layer(
    layer_name, color="0,0,0,128", outline_color="black", outline_width=1
):
    """
    Plot simple polygon layer

    Arguments:
        layer_name (str): name of layer to plot
        color (str): color for polygon fill. If passed as an RGB tuple, fourth value sets the transparency (0-255)
        outline_color (str): color to use for outline color for points and polygons

    Returns:
        None
    """

    layer = QgsProject.instance().mapLayersByName(layer_name)[0]
    # iface.setActiveLayer(my_layer)
    # layer = iface.activeLayer()

    properties = {
        "color": color,
        "outline_color": outline_color,
        "outline_width": outline_width,
    }

    symbol = QgsFillSymbol.createSimple(properties)

    layer.renderer().setSymbol(symbol)
    layer.triggerRepaint()  # if the layer was already loaded
    iface.layerTreeView().refreshLayerSymbology(layer.id())


def draw_simple_line_layer(layer_name, color="purple", linewidth=1, line_style="solid"):
    """
    Plot simple line layer

    Arguments:
        layer_name (str): name of layer to plot
        color (str): color for polygon fill. If passed as an RGB tuple, fourth value sets the transparency (0-255)
        linewidth (numerical): width of line features
        line_style (string): line style (e.g. solid or dash). Must be valid line style type

    Returns:
        None
    """

    layer = QgsProject.instance().mapLayersByName(layer_name)[0]
    # iface.setActiveLayer(my_layer)
    # layer = iface.activeLayer()

    properties = {"color": color, "width": linewidth, "line_style": line_style}

    symbol = QgsLineSymbol.createSimple(properties)

    renderer = QgsSingleSymbolRenderer(symbol)
    layer.setRenderer(renderer)
    layer.triggerRepaint()
    iface.layerTreeView().refreshLayerSymbology(layer.id())


def draw_simple_point_layer(
    layer_name,
    color="0,0,0,255",
    marker_shape="circle",
    marker_size=4,
    outline_color="black",
    outline_width=1,
    marker_angle=45,
):
    """
    Plot simple point layer

    Arguments:
        layer_name (str): name of layer to plot
        color (str): color for polygon fill. If passed as an RGB tuple, fourth value sets the transparency (0-255)
        marker_shape (string): shape of marker for point features. Must be valid shape name
        marker_size (numerical): size of marker for point features
        outline_color (str): color to use for outline color for points and polygons
        outline_width (numerical): width of outline for points and polygons
        marker_angle (numerical): value between 0 and 360 indicating the angle of marker for point objects

    Returns:
        None
    """

    layer = QgsProject.instance().mapLayersByName(layer_name)[0]
    # iface.setActiveLayer(my_layer)
    # layer = iface.activeLayer()

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


def color_ramp_items(colormap, nclass):
    # https://gis.stackexchange.com/questions/118775/assigning-color-ramp-using-pyqgis
    fractional_steps = [i / nclass for i in range(nclass + 1)]
    ramp = QgsStyle().defaultStyle().colorRamp(colormap)
    colors = [ramp.color(f) for f in fractional_steps]

    return colors


def draw_linear_graduated_vlayer(
    layer_name,
    attr_name,
    no_classes,
    cmap="Viridis",
):
    """
    Plot graduated vector later using an equal interval/linearly interpolated color ramp

    Arguments:
        layer_name (str): name of layer to plot
        attr_name (str): name of attr/field used for the classification
        no_classes (int): number of classes
        cmap (str): name of color map

    Returns:
        None
    """
    layer = QgsProject.instance().mapLayersByName(layer_name)[0]

    idx = layer.fields().indexOf(attr_name)

    unique_values = layer.uniqueValues(idx)

    min_val = min(unique_values)
    max_val = max(unique_values)

    value_range = max_val - min_val

    step = value_range / no_classes

    bins = []

    val = min_val

    for i in range(no_classes):
        bins.append(val)
        val += step

    bins.append(max_val)

    colors = color_ramp_items(cmap, no_classes)

    classes = []
    for i in range(len(bins) - 1):
        c = (bins[i], bins[i + 1], colors[i])
        classes.append(c)

    ranges = []

    for i, c in enumerate(classes):
        symbol = QgsSymbol.defaultSymbol(layer.geometryType())
        symbol.setColor(QColor(c[2]))

        render_range = QgsRendererRange(
            QgsClassificationRange(
                f"{c[0]}-{c[1]}",
                c[0],
                c[1],
            ),
            symbol,
        )

        ranges.append(render_range)

    renderer = QgsGraduatedSymbolRenderer(attr_name, ranges)

    layer.setRenderer(renderer)
    layer.triggerRepaint()
    iface.layerTreeView().refreshLayerSymbology(layer.id())


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
