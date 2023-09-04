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
    renderer = QgsCategorizedSymbolRenderer("Category", categories)

    # assign the created renderer to the layer
    if renderer is not None:
        layer.setRenderer(renderer)

    layer.triggerRepaint()
    iface.layerTreeView().refreshLayerSymbology(layer.id())
