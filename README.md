# Knudepunkter project

With this project, we want to assist the planning of *knudepunktnetsværker* (cycle node networks) in Denmark and beyond. For the case of Denmark, there is open access to a beta network for the whole country (cf. GeoFA) and open access data on spatial characteristics relevant for cycling tourism (cf. Septima). This repository contains a set of scripts and detailed instructions. The user can run all scripts with step-by-step explanations in their QGIS Python console. The scripts help the user to do the following:

1. Define the area of interest (a part of Denmark)
2. Fetch and preprocess both 
    - spatial data (Septima) and 
    - beta network data (GeoFA, provided by Folkersma) for this area
3. Evaluate the beta network based on:
    - spatial data
    - network structure
4. Visualize and explore results of the analysis in QGIS

## Workflow

## Scripts step-by-step and To Dos

### 1. User input

Detailed README with screenshots - the user needs to provide a polygon of the study area (cf. BikeDNA) which can be generated through QGIS (explain how). The user also needs to provide the parameters which will be used for the network evaluation and visualization (see step 3&4).

### 2. Fetch data

* fetch and preprocess [Septima](https://septima.dk/rida-web/) data
* fetch and preprocess [GeoFA](https://www.geodanmark.dk/home/vejledninger/geofa/hent-geofa/) data (Folkersma beta network for the whole country)

Instructions for fetching layers in the [PyQGIS cookbook](https://docs.qgis.org/testing/en/docs/pyqgis_developer_cookbook/loadlayer.html)

### Septima Layer Categories

suggested [septima layer categories](https://docs.google.com/spreadsheets/d/19oPiRxOglcvQkEgUipIW7I29kDV0PbKkuJzRGNrAy38/edit?usp=sharing):
* of type point:
    - facility
    - service
    - poi
* of type polygon:
    - bad
    - good:
        - culture
        - nature
        - summerhouse

## 3. Evaluation

* **Anastassia** how much of the network is in the layer? (for each polygon layer)
* **Anastassia** distance of POIs vs. facility/service (user-defined buffer distance)
* **Anastassia** (bananas workflow) loop sizes: average, distribution (both in numbers and in space), length..; think about how to visualize (polygonized)
* variation!! (think about how to quantify it)
* **Ane** elevation: shouldn't be too much steep stretches. Denmark elevation data + find out linestring elev profile in QGIS [WMS]
* network metrics - if possible, but not necessary

### 4. Visualisation & exploring results in QGIS

* *Write Python script that imports results and generates result visualization (one group of layers for standalone network analysis, another group of layers for spatial evaluation)
* *Write qmd stylesheet for results (will be provided to user)

## Setup

Checklist (in THIS order):
1. QGIS LTR 3.28 Firenze
2. *within the QGIS Python console* pip upgrade shapely
3. *within the QGIS Python console* pip upgrade geopandas
4. *within the QGIS Python console* pip install momempy
5. *within the QGIS Python console* pip install osmnx

For pip upgrading or installing packages, run in QGIS python app terminal or your regular terminal
```
<qpdir> -m pip install <PACKAGENAME>
```
where `<qpdir>` points to the Python installation within the QGIS app on the local machine, e.g. `/Applications/QGIS-LTR.app/Contents/MacOS/bin/python3.9`

<!-- OSMNX should be installed as /Applications/QGIS.app/Contents/MacOS/bin/python3.9 -m pip install osmnx==1.6.0 -->

### Running the scripts

0. Setup (see above)
1. Download this repo to your local machine
2. Open up QGIS
3. Open up a new (empty) project
4. Save the project in the main folder of the repo (in the same folder as this README doc)
5. Open up the Python console plugin in QGIS
6. Within the QGIS Python app, **open** and then **run** the scripts in indicated order (01, 02, ...)

### Virtual environment

(Only if you want to run the scripts outside of QGIS; optional)

Run in your terminal:
```
conda create --name knupu python=3.9
conda activate knupu
conda config --prepend channels conda
conda config --prepend channels conda-forge
conda install numpy matplotlib pandas geopandas shapely contextily networkx momepy osmnx qgis ipykernel
```