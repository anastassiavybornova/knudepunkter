# Input data

All files must be in a file format readable by [GeoPandas](https://geopandas.org/en/stable/docs/user_guide/io.html) (e.g., GeoPackage, GeoJSON, Shapefile etc.) and by [QGIS](https://docs.qgis.org/3.28/en/docs/user_manual/managing_data_source/opening_data.html).

All data must be in the same projected coordinate reference system.

## Network Data

 A recreational bicycle network can be mapped at various level of detail. For correct planning and routing, a detailed, high-resolution data set is necessary. This network representation should place the network on the exact intended road and path stretches, specify which intersections to use, and take into account possible differences in network routing depending on the travel direction. This detailed network representation is sometimes referred to as a 'technical network' [CITE SEPTIMA], and supports the planning of route signage, routing, and analysis of the exact stretches included in the analysis.

A technical network representation is however too detailed for small scale overview maps and for more general analysis of the node network structure. For example, using the technical network will result in over-counting of the network extent in locations where different paths on each side of a road are used for different travel directions, just as the technical network might contain duplicate nodes with identical node numbers to support navigation. To avoid these issues, the Cycle Node Network Planner makes use of a simplified network representation, sometimes referred to as a 'communication network' [CITE SEPTIMA].

To run the Cycle Node Network Planner, input data with a generalized representation is required. Specifically, the input network data must consist of two separate data set: one with linestring geometries representing the network edges in the bicycle network and one with point geometries representing the cycle nodes. All nodes must have a unique node id and all edges must be uniquely indexed by their start and end node. No parallel edges are allowed, so if more than one edge runs between the same node pair, the edge must be split by adding an interstitial node on one of the parallel edges (even if the edges have different geometries). The data must be in a common geospatial format readable by both QGIS and GeoPandas and be provided in a projected coordinate reference system (CRS). Importantly, the network must be topologically correct, i.e. with snapping of edge and node geometries.

<p align="center"><img alt="Illustration of interstitial node" src="/images/inter_node.png" width=50%></p>

If only a highly detailed network data set is available (e.g. in a format used for routing on the road network or technical planning of signage at intersections), the Cycle Node Network Planner includes a pre-processing step that can convert the more detailed data set to the required input format [LINK]. For this step to be successful, the detailed network data must be:

* Provided as one data set with network edges and one with network nodes (similar to the generalized network described above).

* A coherent topological network, meaning that edge and node geometries must be snapped, and that all edge geometries must be indexed by their start and end node.

* A more detailed technical network might contain parallel edges with slightly different geometries representing e.g. each their bicycle lane running on different side of a road. This is allowed in the technical input network, as long as the edges' start and end nodes share the same node id (for example, both edges run between nodes labelled A and nodes labelled B) (see illustration below).

<p align="center"><img alt="Illustration of parallel edges" src="/images/parallel_edges.png" width=50%></p>

* *Not* contain parallel edges with the same start and end nodes that are *not* representing stretches on the same road/path. In that case, an interstitial node must be added to split one of the parallel edges.

* Unlike a generalized network, a technical network might contain more than one node with the same node ID. This for example happens at intersections, where more than one node geometry is needed for a correct detailed mapping of the network, but all nodes at the intersection belongs to the same 'cycle node' used for navigation.
    * In that case, the node data set must contain an attribute 'main'. For each node number, *one* node must have 'main' = True, while all other nodes with that number must have 'main' = False (see illustration below).

<p align="center"><img alt="Illustration of main node" src="/images/main_node.png" width=50%></p>

Illustrations and data specifications based on Septima, 2023 [LINK].

## Study Area Polygon

* The study area must be defined by one **polygon** provided in a geospatial file format.

## Land use

## Point data

## Elevation

The elevation data set must:

* Cover the entire study area.

* Be in a raster format readable by QGIS and GeoPandas (e.g. GeoTIFF).

* Be in a sufficiently high resolution to compute the slope of the network stretches. A resolution of 10 * 10 meters or higher is recommended.
