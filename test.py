# from qgis.core import QgsVectorLayer
from qgis.core import *


# TODO: docs, line width, colors, labels?


def draw_slope_layer(
    layer_name,
    slope_ranges,
    slope_field="slope",
    # alpha=180,
    line_width=1,
    line_style="solid",
):
    layer = QgsProject.instance().mapLayersByName(layer_name)[0]

    ranges = []

    for label, lower, upper, color in slope_ranges:
        symbol = QgsLineSymbol.createSimple(
            {
                # "color": f"{randrange(0, 256)}, {randrange(0, 256)}, {randrange(0, 256)}, {alpha}",
                "width": line_width,
                "line_style": line_style,
            }
        )
        # sym = QgsSymbol.defaultSymbol(layer.geometryType())
        symbol.setColor(QColor(color))
        rng = QgsRendererRange(lower, upper, symbol, label)
        ranges.append(rng)

    renderer = QgsGraduatedSymbolRenderer(slope_field, ranges)

    layer.setRenderer(renderer)
    layer.triggerRepaint()
    iface.layerTreeView().refreshLayerSymbology(layer.id())


layer_name = "Segments slope"
slope_ranges = (
    ("Manageable elevation", 0.0, 2.99999, "cyan"),
    ("Noticeable elevation", 3.0, 4.999999, "blue"),
    ("Steep elevation", 5.0, 6.9999999, "yellow"),
    ("Very steep elevation", 7, 100.0, "red"),
)

draw_slope_layer("Segments slope", slope_ranges=slope_ranges)
