# How to use the Cycle Node Network Planner

Below, you find detailed instructions on how to use the Cycle Node Network Planner. 

Contents of this file (click to jump to corresponding step):

* [Step 1](#step-1-set-up-qgis): Set up QGIS
* [Step 2](#step-2-download-the-contents-of-this-repository): Download the contents of this repository (`knudepunkter-fyn` folder)
* [Step 3](#step-3-fill-out-the-configuration-file): Fill out the configuration file
* [Step 4](#step-4-open-the-qgis-project-in-the-knudepunkter-fyn-folder): Open the empty QGIS project `Fyn.qgz` in the `knudepunkter-fyn` folder
* [Step 5](#step-5-run-scripts-from-the-qgis-python-console): Open the Python console in QGIS, and run the scripts from the `scripts` folder in indicated order
* [Step 6](#step-6-explore-the-qgis-visualization): Explore the QGIS visualization: use the evaluation layers (polygons, points, elevation) to assess in which places the network should be improved
* [Step 7](#step-7-explore-the-summary-statistics): Explore the summary statistics: get an overview of overall network quality and general characteristics of the network 

***

## Step 1: Set up QGIS

1. You need QGIS-LTR 3.28 Firenze. If you already have QGIS installed, you can check your version by clicking on `About QGIS-LTR`, as shown below. To download the latest stable release of QGIS or to upgrade it to the 3.28 version, [click here](https://www.qgis.org/en/site/forusers/download.html). When downloading, make sure to install not the newest, but the latest stable version (QGIS-LTS 3.28).

<p align="center"><img alt="Check your QGIS version" src="/docs/screenshots/qgis-version.png" width=80%></p>

<!-- Troubleshooting: if new installation on Mac, must be first opened 1x with rightclick and confirm -->

2. Find out the path to the Python installation for the QGIS app on your local machine. Typically, this will be similar to: 
* for Windows, `C:\Program Files\QGIS 3.28.13\apps\Python39\python`
* for MacOS/Linux, `/Applications/QGIS-LTR.app/Contents/MacOS/bin/python3.9`



3. Open your command line interface (on Windows: Command Prompt; on MacOS/Linux: Terminal)

4. Use the path from step 2 (abbreviated as `<qgispythonpath>` below) to run the commands in your commmand line interface, in indicated order. (Copy each line below separately, paste it in your command line interface, replace `<qgispythonpath>` in quotation marks by the path from step 2, and hit enter.) 

**On Windows:**
```
"<qgispythonpath>" -m pip install --upgrade shapely
"<qgispythonpath>" -m pip install --upgrade geopandas --force-reinstall -v geopandas==0.14.0
"<qgispythonpath>" -m pip install momepy
"<qgispythonpath>" -m pip install osmnx==1.6.0
"<qgispythonpath>" -m pip install contextily
```
<!-- <qgispythonpath> -m pip install numpy --force-reinstall -v numpy==1.22.4 might not be needed on windows? for me it didnt work, had to redo geopandas reinstall one more time-->

<p align="center"><img alt="Setting up PyQGIS from the command line (Command prompt on Windows)" src="/docs/screenshots/cli-install-windows.png" width=80%></p>

> TO INSERT: **EXTRA STEP FOR WINDOWS: COPYPASTE SOME SSL FILES AS EXPLAINED HERE (Feb 22, 2022 reply) https://stackoverflow.com/questions/60290795/ssl-module-in-python-is-not-available-qgis 

**On MacOS/Linux**:
```
"<qgispythonpath>" -m pip install --upgrade shapely  
"<qgispythonpath>" -m pip install --upgrade geopandas --force-reinstall -v geopandas==0.14.0
"<qgispythonpath>" -m pip install momepy
"<qgispythonpath>" -m pip install osmnx==1.6.0
"<qgispythonpath>" -m pip install numpy --force-reinstall -v numpy==1.22.4
"<qgispythonpath>" -m pip install contextily
```

<p align="center"><img alt="Setting up PyQGIS from the command line (Terminal on MacOS)" src="/docs/screenshots/cli-install-macos.png" width=80%></p>

***

## Step 2: Download the contents of this repository

On this GitHub repository page, click on the `Code` button (in the upper right), then `Download ZIP` to download the entire repository to your local machine. Unzip the downloaded folder `knudepunkter-fyn`. This will be the main folder for the entire workflow.

<p align="center"><img alt="Download the knudepunkter-fyn folder" src="/docs/screenshots/github.png" width=80%></p>

***

## Step 3: Fill out the configuration file

Open the file `config.yml`, located in the main folder `knudepunkter-fyn`, in any text editor (e.g. Notepad on Windows, or TextEdit on MacOS). Provide the study area name of your choice, in quotation marks (the default is "Fyn"). Then, in the list of municipalities, remove the hashtags for all municipalities that you want to include in the analysis.

<p align="center"><img alt="Fill out the configuration file" src="/docs/screenshots/config-fillout.png" width=80%></p>

***

## Step 4: Open the QGIS project in the knudepunkter-fyn folder

Open the empty QGIS project **`Fyn.qgz`**, located in the `knudepunkter-fyn` folder. 

***

## Step 5: Run scripts from the QGIS Python console

In QGIS,

1. Open the Python Console 
2. Click on `Show Editor`
3. Click on `Open Script`
4. Navigate to the `scripts` folder and open the first script, `01_define_study_area.py`
5. Click on `Run Script`
6. While the script is running, you will see status messages in the console window
7. Once you see the message `Script XXX ended succcessfully`, you can run the next script. Repeat steps 4-6 for all scripts (from `01_define_study_area.py` to `07_make_summary_statistics.py`) consecutively

<p align="center"><img alt="Running the scripts in the QGIS Python console" src="/docs/screenshots/qgis-run.png" width=80%></p>

<!-- The 05_compute_slope script sometimes needs a couple of times until it runs successfully -->

***

## Step 6: Explore the QGIS visualization

> Screenshot

Explain layers

***

## Step 7: Explore the summary statistics

> Screenshot

Explain separate points