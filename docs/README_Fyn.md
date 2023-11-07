# The Cycle Node Network Planner

*A decision support tool under development, aimed at supporting the planning of Denmark's cycle node network.*

The Cycle Node Network Planner is the result of a collaboration between [Dansk Kyst- og Naturturisme](https://www.kystognaturturisme.dk) (DKNT) and the [IT University of Copenhagen](https://nerds.itu.dk) in the framework of DKNT's project [Bedre vilkår for cykelturismen in Denmark](https://www.kystognaturturisme.dk/cykelknudepunkter). Our goal is to provide an open-source, customizable, data-driven decision support tool for the planning of Denmark's cycle node network. The Cycle Node Network planner runs in QGIS.

Here, we present a "demo" (still under development) version of the Cycle Node Network Plannner, pre-set to run for the island of Fyn. Below, you find an overview of instructions to get started. More detailed instructions and documentation are available, too (see links below).

# Getting started

## 1. What can the Cycle Node Network Planner do for me?

*[insert screenshot of QGIS project with explanations]*

## 2. What are the evaluation criteria of the Planner?

The Tool evaluates the cycle node network through 3 perspectives: polygon layers, point layers, and elevation.

**Polygon layers** show the attributes of the area (land use) surrounding the cycle node networks:
* Nature
* Culture
* Agriculture
* Industrial
* Summerhouse area

**Point layers** show how close the stretches of the cycle node network are to specific locations:
* Facilities (good to have directly on the road, such as drinking water, toilets, bicycle shops)
* Services (good to have close to the road, such as groceries and places to slep)
* POIs (good to have in vicinity of the road within an acceptable detour, such as landmarks and museums)

**Elevation** is shown as an attribute of ~100m segments which together make up the cycle node network.

## 3. How can I run the Planner myself?

Steps:
1. Set up QGIS
2. Download the contents of this repository
3. Run the scripts in the `scripts` folder in indicated order
4. Explore the QGIS visualization: use the evaluation layers (polygons, points, elevation) to assess in which places the network should be changed 
5. Explore the summary results (PDF): get an overview of overall network quality and general characteristics of the network (such as average node density, average distance between two nodes, ...)

Detailed instructions are found [here](LINK)

## 4. What if running the Planner doesn't work?

For troubleshooting, [contact us](mailto:anvy@itu.dk)! We also prepared a QGIS project showing the final output of the tool. It is available for download [here](LINK).

## 5. I want to know more

Find out more about:
* [Data sources](LINK)
* [Evaluation layers](LINK)
* [Python libraries used](LINK)

# Your feedback is greatly appreciated

Once you have familiarized yourself with the Cycle Node Network Planner, we will be grateful for any feedback on the Tool! Please fill out the [survey here](LINK) (between 5 and 20 minutes).

* Is the description of the tool clear and easy to follow?
* Is the technical setup reproducible? 
* Did you run into any issues when running the tool? If so, please elaborate
* Using network Evaluation layers:
    - Are the polygon layers useful? For example, is it helpful to see which parts of the network run through nature, culture, or agriculture areas?
    - Are the point layers useful? For example, is it helpful to be able to visually distinguish between reached and unreached POIs? 
    - Is the elevation layer useful? For example, is it helpful to see segments with particularly large slopes highlighted?
* Are the summary statistics useful? Could they inform your planning process?
* Do you have any comments on the visualization? (layer structure, feature size, colors, background maps, ...) What could be improved? What should be done differently?
* Is there any information that you think is missing from the tool?
* More thoughts/remarks