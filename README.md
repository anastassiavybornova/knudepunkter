# The Cycle Node Network Planner

<img alt="Cycle node network in Jutland, Denmark" src="/images/social.png" width=80%>

With this project, we want to assist the planning of [*knudepunktnetsværker*](https://www.kystognaturturisme.dk/cykelknudepunkter) (cycle node networks) in Denmark and beyond. This repository contains a set of scripts and detailed instructions. The user can run all scripts with step-by-step explanations in their QGIS Python console. The scripts help the user to do the following:

1. Define the area of interest (a part of Denmark)
2. Fetch and preprocess both 
    - spatial data (Septima) and 
    - beta network data (GeoFA, provided by Folkersma) for this area
3. Evaluate the beta network based on:
    - spatial data
    - network structure
4. Visualize and explore results of the analysis in QGIS

## Setup

1. You need QGIS-LTR 3.28 Firenze (can be downloaded [here](https://www.qgis.org/en/site/forusers/download.html))  
2. Find out the path to the Python installation for the QGIS app on your local machine, e.g. `/Applications/QGIS-LTR.app/Contents/MacOS/bin/python3.9`. Use this path below (abbreviated as `<qgispythonpath>`) to run from terminal, in indicated order:  
3. `<qgispythonpath> -m pip install --upgrade shapely`  
4. `<qgispythonpath> -m pip install --upgrade geopandas`  
5. `<qgispythonpath> -m pip install momepy`  
6. `<qgispythonpath> -m pip install osmnx`  
7. `<qgispythonpath> -m pip install numpy --force-reinstall -v numpy==1.22.4`

<!-- OSMNX should be installed as /Applications/QGIS.app/Contents/MacOS/bin/python3.9 -m pip install osmnx==1.6.0 -->

For detailed instructions on setup, click [here](docs/SETUP_detailed.md).

## Running the scripts

After completing the setup:
1. Download this repository to your local machine
2. Open QGIS
3. In QGIS, open a new (empty) QGIS project
4. Save the QGIS project in the main folder of the repository
5. Open the Python console plugin in QGIS (`Plugins > Python Console`)
6. On top of the QGIS Python console, press the `Show editor` button to view the editor 
7. In this QGIS Python console editor, **open** and then **run** the scripts in indicated order (01, 02, ...)

For detailed instructions on running the scripts, click [here](docs/RUNSCRIPTS_detailed.md).