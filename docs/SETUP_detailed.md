> TODO (add details and screenshots)

# Setup - detailed instructions

1. You need QGIS-LTR 3.28 Firenze (can be downloaded [here](https://www.qgis.org/en/site/forusers/download.html))  
2. Find out the path to the Python installation for the QGIS app on your local machine, e.g. `/Applications/QGIS-LTR.app/Contents/MacOS/bin/python3.9`. Use this path below (abbreviated as `<qgispythonpath>`) to run from terminal, in indicated order:  
3. `<qgispythonpath> -m pip install --upgrade shapely`  
4. `<qgispythonpath> -m pip install --upgrade geopandas`  
5. `<qgispythonpath> -m pip install momepy`  
6. `<qgispythonpath> -m pip install osmnx`  
7. `<qgispythonpath> -m pip install numpy --force-reinstall -v numpy==1.22.4`

<!-- OSMNX should be installed as /Applications/QGIS.app/Contents/MacOS/bin/python3.9 -m pip install osmnx==1.6.0 -->

For detailed instructions on setup, click here.