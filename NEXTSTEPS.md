## Current TO DOs

* folkersma: ask for most recent data on parent/child; split nodes. (ask kirsten if that's fine first)
* ~~clean up repo~~
* ~~update and combine the scripts 01_define_area and 02_get_beta_data into one script where: input... which area we want to look at (typically a municipality border?); output... beta data for that area~~
* ~~FOR NOW, drop the scripts 05_get_concept_data and 06_concept_to_network~~ 
* **Ane** update the scripts `02_make_beta_network.py` with *NEW* folkersma data (with info on split, child/parent nodes etc.) to create a fully connected, simplified network. possibly look into building a graph within qgis: https://docs.qgis.org/3.28/en/docs/pyqgis_developer_cookbook/network_analysis.html

* Script for getting layer from GeoFA done

* **Ane** update the script `03_get_septima_data` so that it fetches all requested septima data and creates corresponding layers (cf. README) --> DONE (only missing a full list of all desired data)
* **Ane/Anastassia** update the `04_evaluate_septima` script to evalute all data from step 08
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


* What to do when septima database is down? Alternative setup for using data stored on disk?