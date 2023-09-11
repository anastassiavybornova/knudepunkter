## Current TO DOs

* folkersma: ask for most recent data on parent/child; split nodes. (ask kirsten if that's fine first)
* ~~clean up repo~~
* ~~update and combine the scripts 01_define_area and 02_get_beta_data into one script where: input... which area we want to look at (typically a municipality border?); output... beta data for that area~~
* ~~FOR NOW, drop the scripts 05_get_concept_data and 06_concept_to_network~~ 

* **Ane** update the scripts `02b_make_beta_network.py` with *NEW* folkersma data (with info on split, child/parent nodes etc.) to create a fully connected, simplified network. possibly look into building a graph within qgis: https://docs.qgis.org/3.28/en/docs/pyqgis_developer_cookbook/network_analysis.html

    * Question: should we skip parallel edges? >> would be nice to keep track, but not top priority
    * TODOS: Incorporate parent/child-nodes? >> wait for Folkersma data before we act on this one
    

* ~~Script for getting layer from GeoFA done (02a)~~

* **Ane** ~~update the script `03a_get_septima_data` so that it fetches all requested septima data and creates corresponding layers (cf. README)~~ --> DONE (only missing a full list of all desired WFSses)

* **Anastassia** make script for getting subsets of Septima data from downloaded wfs data - work in progress (error messages for some of the WFS layers?).

    * Q1: is it ok to use geopandas for all data filtering & merging?
    * Q2: evaluation layers
        - good/bad/culture/summerhouse areas: simple overlap
        - point data: user-defined threshold, binary (close enough - yes/no)

* **Anastassia** try to find a way to import functions from src

* **Anastassia** write to Kirsten

* **Anastassia** check why we get an error message about index_parts from the `create_osmnx_graph` function

* **Ane/Anastassia** update the `04_evaluate_septima` script to evaluate all data from step 08

* **Ane** Write visualization scripts for plotting layers (colors, hue, zoom levels, categorization etc.)

* Write an evaluation script (point of departure can be `_10_compare_networks`, but don't do comparison)

* work on papers (2x)

* read process&method handbook

* receive Faxe data from Kirsten

* receive technical specifications (septima) doc from Kirsten

* receive folkersma's process description from Kirsten

## Later TO DOs

* add a config file where one can decide *which* septima layers to add

* figure out how the import of src. scripts works (cross-platform...)

* docker?!

* What to do when septima database is down? Alternative setup for using data stored on disk? --> Just store data to geopackage as it is now when downloaded from WFS connection

* convert EVERYTHING to native qgis (all geopandas functions that we can)

* think about a **timeline**

## @ Kirsten:

Please send us
- the technical specifications (from Septima)
- the process description (from Folkersma)
- the Faxe data set

Please allow us
- to get in touch with Folkersma about child/parent data
- Septima (2 point layers not available)