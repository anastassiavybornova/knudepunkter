# How to use the Cycle Node Network Planner

Below, you find detailed instructions with screenshots for each of the following steps:

* [Step 1](#step-1-set-up-qgis): Set up QGIS
* [Step 2](#step-2-download-the-contents-of-this-repository): Download the contents of this repository (`knudepunkter-fyn` folder)
* [Step 3](#step-3-set-up-a-qgis-project-in-the-knudepunkter-fyn-folder): Open QGIS, set up a new project, and save it in the `knudepunkter-fyn` folder
* [Step 4](#step-4-run-scripts-from-the-qgis-python-console): Open the Python console in QGIS, and run the scripts from the `scripts` folder in indicated order
* [Step 5](#step-5-explore-the-qgis-visualization): Explore the QGIS visualization: use the evaluation layers (polygons, points, elevation) to assess in which places the network should be changed 
* [Step 6](#step-6-explore-the-summary-statistics): Explore the summary statistics (PDF): get an overview of overall network quality and general characteristics of the network 

***

## Step 1: Set up QGIS

1. You need QGIS-LTR 3.28 Firenze. If you already have QGIS installed, you can check your version by clicking on `About QGIS-LTR`, as shown below. To download QGIS or to upgrade it to the 3.28 version, [click here](https://www.qgis.org/en/site/forusers/download.html).

<p align="center"><img alt="Check your QGIS version" src="/docs/screenshots/qgis-version.png" width=80%></p>

2. Find out the path to the Python installation for the QGIS app on your local machine, e.g. `/Applications/QGIS-LTR.app/Contents/MacOS/bin/python3.9`.

> HOW? 

3. Open your command line interface (on MacOS: Terminal; on Windows: **?**)

> HOW?

4. Use that path (abbreviated as `<qgispythonpath>` below) to run the following commands from terminal, in indicated order:  

```
<qgispythonpath> -m pip install --upgrade shapely  
<qgispythonpath> -m pip install --upgrade geopandas --force-reinstall -v geopandas==0.14.0
<qgispythonpath> -m pip install momepy
<qgispythonpath> -m pip install osmnx==1.6.0
<qgispythonpath> -m pip install numpy --force-reinstall -v numpy==1.22.4
```

> HOW?

***

## Step 2: Download the contents of this repository

On this GitHub repository page, click on the `Code` button (in the upper right), then `Download ZIP` to download the entire repository to your local machine. Unzip the downloaded folder `knudepunkter-fyn`. This will be the main folder for the entire workflow.

> SCREENSHOT

***

## Step 3: Set up a QGIS project in the knudepunkter-fyn folder

Project > New and then Project > Save as and then (yourprojectname) in `knudepunkter-fyn`

> Screenshot

***

## Step 4: Run scripts from the QGIS Python console

1. Open the Python Console 
2. Click on `Show Editor`
3. Click on `Open Script`
4. Open the first script, `scriptnamehere`
5. Click on `Run Script`
6. While the script is running, you will see status messages in the console window
7. Once you see the message `scriptnamehere ended succcessfully`, you can run the next script: repeat steps 4-6 for all scripts (`scriptnumbers here`) consecutively

***

## Step 5: Explore the QGIS visualization

> Screenshot

Explain layers

***

## Step 6: Explore the summary statistics

> Screenshot

Explain separate points