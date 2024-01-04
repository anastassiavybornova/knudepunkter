# How to use the Cycle Node Network Planner

Below, you find detailed instructions on how to use the Cycle Node Network Planner. 

Contents of this file (click to jump to corresponding step):

* [Step 1](#step-1-set-up-qgis): Set up QGIS
* [Step 2](#step-2-download-the-contents-of-this-repository): Download the contents of this repository (`knudepunkter` folder)
* [Step 3](#step-3-fill-out-the-configuration-file): Fill out the configuration file
* [Step 4](#step-4-open-the-qgis-project-in-the-knudepunkter-folder): Open the empty QGIS project `Fyn.qgz` in the `knudepunkter` folder
* [Step 5](#step-5-run-scripts-from-the-qgis-python-console): Open the Python console in QGIS, and run the scripts from the `scripts` folder in indicated order
* [Step 6](#step-6-explore-the-qgis-visualization): Explore the QGIS visualization: use the evaluation layers (polygons, points, elevation) to assess in which places the network should be improved
* [Step 7](#step-7-explore-the-summary-statistics): Explore the summary statistics: get an overview of overall network quality and general characteristics of the network 

***

## Step 1: Set up QGIS

1. You need QGIS-LTR 3.28 Firenze. If you already have QGIS installed, you can check your version by clicking on `About QGIS-LTR`, as shown below. To download the latest stable release of QGIS or to upgrade it to the 3.28 version, [click here](https://www.qgis.org/en/site/forusers/download.html). When downloading, make sure to install not the newest, but the latest stable version (QGIS-LTS 3.28).

<p align="center"><img alt="Check your QGIS version" src="/docs/screenshots/qgis-version.png" width=80%></p>

2. Find out the path to the Python installation for the QGIS app on your local machine. Typically, this will be similar to: 

```
C:\Program Files\QGIS 3.28\apps\Python39\python
```

3. To avoid issues with permissions for the custom setup of Python packages in your QGIS installation on Windows, you will need to copy-paste the following two files:

```
libcrypto-1_1-x64.dll
libssl-1_1-x64.dll
```

from the `\bin\` subfolder to the Python installation subfolder (as identified in step 2) of your QGIS installation. To do so, simply open your file explorer and navigate to the path `C:\Program Files\QGIS 3.28\bin`; locate the 2 files and copy them; navigate to the path `C:\Program Files\QGIS 3.28\apps\Python39\python`; and paste the 2 files here. Note that the exact file paths might look slightly different on your machine (e.g. a different QGIS version number, or a different Python version number).

4. Open your command line interface (Command Prompt on Windows)

5. Use the path from step 2 (abbreviated as `<qgispythonpath>` below) to run the commands in your commmand line interface, in indicated order. (Copy each line below separately, paste it in your command line interface, replace `<qgispythonpath>` in quotation marks by the path from step 2, and hit enter.) Note that you have to be connected to the internet for the installs to work.

```
"<qgispythonpath>" -m pip install --upgrade shapely
"<qgispythonpath>" -m pip install --upgrade geopandas --force-reinstall -v geopandas==0.14.0
"<qgispythonpath>" -m pip install momepy
"<qgispythonpath>" -m pip install osmnx==1.6.0
"<qgispythonpath>" -m pip install contextily
```
<!-- <qgispythonpath> -m pip install numpy --force-reinstall -v numpy==1.22.4 might not be needed on windows? for me it didnt work, had to redo geopandas reinstall one more time-->

<p align="center"><img alt="Setting up PyQGIS from the command line (Command prompt on Windows)" src="/docs/screenshots/cli-install-windows.png" width=80%></p>

## Step 2: Download the contents of this repository

On this GitHub repository page, click on the `Code` button (in the upper right), then `Download ZIP` to download the entire repository to your local machine. Unzip the downloaded folder `knudepunkter`. This will be the main folder for the entire workflow.

<p align="center"><img alt="Download the knudepunkter folder" src="/docs/screenshots/github.png" width=80%></p>

***

## Step 3: Fill out the configuration file

Open the file `config.yml`, located in the main folder `knudepunkter`, in any text editor (e.g. Notepad). Provide the study area name of your choice, in quotation marks (the default is "Fyn"). Then, in the list of municipalities, remove the hashtags for all municipalities that you want to include in the analysis. This is set to the following 10 municipalities by default: 0410 Middelfart, 0420 Assens, 0430 Faaborg-Midtfyn, 0440 Kerteminde, 0450 Nyborg, 0461 Odense, 0479 Svendborg, 0480 Nordfyns, 0482 Langeland and 0492 Æro. 

<p align="center"><img alt="Fill out the configuration file" src="/docs/screenshots/config-fillout.png" width=80%></p>

***

## Step 4: Open the QGIS project in the knudepunkter folder

Open the empty QGIS project **`Fyn.qgz`**, located in the `knudepunkter` folder. 

***

## Step 5: Run scripts from the QGIS Python console

In QGIS,

1. Open the Python Console 
2. Click on `Show Editor`
3. Click on `Open Script`
4. Navigate to the `scripts` folder (within the `knudepunkter` repository) 
5. Select the next script (by number: 01, then 02, ...)
6. Click on `Open`
7. Optionally, at the top of each script, you can adjust display settings (type `True` or `False` for displaying vs. not displaying the layers generated by this script). 
8. Each script contains a line beneath which no changes should be introduced.
9. Click on `Run`.
10. While the script is running, you will see status messages in the console window.
11. Once you see the message `Script XXX ended succcessfully`, you can run the next script. 

Repeat steps 3-11 for all scripts (from `01_define_study_area.py` to `07_plot_summary_statistics.py`) consecutively.

<p align="center"><img alt="Running the scripts in the QGIS Python console" src="/docs/screenshots/qgis-run.png" width=80%></p>

**Troubleshooting**
* Note that for some of the scripts, run time could take up to several minutes, and QGIS may become unresponsive while the script is running.
* Note that for some of the scripts, a stable internet connection is required.
* If the script `05_compute_slope.py` script fails to run - please try again! (it sometimes requires several attempts)

***

## Step 6: Explore the QGIS visualization

Explore the results of the workflow by (de)selecting layers in the QGIS project. 

For example, select "Culture/Network in culture areas" within the "Evaluate network" layer to explore which parts of the network lead through culturally particularly interesting parts of the study area.

<p align="center"><img alt="Explore evaluation: culture areas" src="/docs/screenshots/explore-culture.png" width=60%></p>

Or, select "POIS" within the "Evaluate network" layer to explore which points of interest are within vs. outside reach (dark vs. light color) of the network. Use the "Identify features" tool to get more information on a particular feature on the map.

<p align="center"><img alt="Explore evaluation: points of interest (POIs)" src="/docs/screenshots/explore-pois.png" width=60%></p>

***

## Step 7: Explore the summary statistics

After running all scripts, you will find a plot of summary statistics in the subfolder `results/plots/` (in your `knudepunkter` folder):

<p align="center"><img alt="Summary statistics for study area" src="/docs/screenshots/evaluation_Fyn.png" width=80%></p>