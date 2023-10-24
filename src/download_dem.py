datafordeler_username = "MAKKFGPILT"
datafordeler_password = "Testing23!"

wcs_url = f"https://services.datafordeler.dk/DHMNedboer/dhm_wcs/1.0.0/WCS?username%3D{datafordeler_username}%26password%3D{datafordeler_password}"

dem_name = "dhm_terraen"

source = f"dpiMode=7&identifier={dem_name}&tilePixelRatio=0&url={wcs_url}"

dem_raster = QgsRasterLayer(source, "testtest", "wcs")

QgsProject.instance().addMapLayer(dem_raster)

print("added dem raster")
