Source = "pagingEnabled='true' preferCoordinatesForWfsT11='false' restrictToRequestBBOX='1' srsname='EPSG:25832' typename='landemaerker' url='https://rida-services.test.septima.dk/ows?map=land_attraktioner' version='auto'"
# bbox='674167.33536206,710371.08425349,6117158.24514454,6141239.37945889'

minx = 710320
miny = 6170841
maxx = 728036
maxy = 6186120

tempWFS = QgsVectorLayer(Source, "Landemaerker_subset", "WFS")

tempWFS.selectByRect(QgsRectangle.fromWkt(f'POLYGON(({minx} {miny}, {maxx} {miny}, {maxx} {maxy}, {minx} {maxy}, {minx} {miny}))'))
 
tempWFS_subset = tempWFS.materialize(QgsFeatureRequest().setFilterFids(tempWFS.selectedFeatureIds()))


# USING TEMP/SCRATCH LAYER
if not tempWFS.isValid():
    print("Layer failed to load!")
else:
    QgsProject.instance().addMapLayer(tempWFS_subset)


# USING LAYER WRITTEN TO DISK
homepath = QgsProject.instance().homePath()
save_options = QgsVectorFileWriter.SaveVectorOptions()
transform_context = QgsProject.instance().transformContext()
# Write to a GeoPackage
error = QgsVectorFileWriter.writeAsVectorFormatV3(tempWFS_subset,
                                                  homepath + "/data/WFS_subset.gpkg",
                                                  transform_context,
                                                  save_options)
if error[0] == QgsVectorFileWriter.NoError:
    print("data exported!")
else:
  print(error)
  
QgsProject.instance().addMapLayer(QgsVectorLayer(homepath+"/data/WFS_subset.gpkg","saved_subset"))