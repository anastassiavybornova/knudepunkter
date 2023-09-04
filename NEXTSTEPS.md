## Current TO DOs

* folkersma: ask for most recent data on parent/child; split nodes. (ask kirsten if that's fine first)
* work on papers (2x)
* **Anastassia** clean up repo
* update and combine the scripts 01_define_area and 02_get_beta_data into one script where: input... which area we want to look at (typically a municipality border?); output... beta data for that area
* **Ane** update and combine the scripts 03_preprocess_beta_data and 04_beta_to_network with *NEW* folkersma data (with info on split, child/parent nodes etc.) to create a fully connected, simplified network. possibly look into building a graph within qgis: https://docs.qgis.org/3.28/en/docs/pyqgis_developer_cookbook/network_analysis.html
* FOR NOW, drop the scripts 05_get_concept_data and 06_concept_to_network 
* **Ane** update and combine the scripts 08_septima_from_wfs... and 08_septima_from_wfs..._ane into one script that fetches all requested septima data and creates corresponding layers
* update the 09_evaluate_septima script to evalute all data from step 08
* update 10_compare_networks 

## Later TO DOs

* add a config file where one can decide *which* septima layers to add
* docker?!


***

## Septima Layer Categories

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

***

## Evaluation

* variation!! (think about how to quantify it)
* loop sizes: average, distribution (both in numbers and in space), length...
* think about how to visualize (polygonized)
* distance of POIs vs. facility/service
* elevation: shouldn't be too much steep stretches. Denmark elevation data + find out linestring elev profile in QGIS [WMS]
* network metrics - if possible, but not necessary