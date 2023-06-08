# THIS ALMOST WORKED
# TO DO CUT TO BOUNDING BOX

Source = "pagingEnabled='true' preferCoordinatesForWfsT11='false' restrictToRequestBBOX='1' srsname='EPSG:25832' typename='landemaerker' url='https://rida-services.test.septima.dk/ows?map=land_attraktioner' version='auto'"
# bbox='674167.33536206,710371.08425349,6117158.24514454,6141239.37945889'
tempWFS = QgsVectorLayer(Source, "Landemaerker", "WFS")
if not tempWFS.isValid():
    print("Layer failed to load!")
else:
    QgsProject.instance().addMapLayer(tempWFS)