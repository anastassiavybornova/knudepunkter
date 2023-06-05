from qgis.core import *

def plot_layer(filepath, layername, line_color, line_width):
    
    mylayer = QgsVectorLayer(filepath, layername, "ogr")
    
    if not mylayer.isValid():
        print(f"{layername}: layer failed to load!")
    
    else:
        
        myrenderer = mylayer.renderer()
        print("Type:", myrenderer.type())
        
        props = myrenderer.symbol().symbolLayer(0).properties()
        print(props)
        
        props["line_color"] = line_color
        props["line_width"] = line_width
        
        myrenderer.setSymbol(QgsLineSymbol.createSimple(props))
        QgsProject.instance().addMapLayer(mylayer)