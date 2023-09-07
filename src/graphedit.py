import numpy as np
import os

os.environ["USE_PYGEOS"] = "0"
import geopandas as gpd
import shapely
from shapely.geometry import Point
from shapely.wkt import loads, dumps
import momepy
import networkx as nx
import json


### function that converts a networkx graph in osmnx format to a json file
def spatialgraph_tojson(G, my_crs, filepath):
    # copy graph
    G = G.copy()

    # convert crs to string to make it json serializable
    my_crs_string = str(my_crs)

    # json serialization
    node_link_data = nx.node_link_data(G)

    # add crs from string
    node_link_data[
        "graph"
    ] = (
        {}
    )  # step needed to delete the "crs type" object from here and overwrite it with a str object
    node_link_data["graph"]["crs"] = my_crs_string

    # replace each linestring by its string representation
    for linkdict in node_link_data["links"]:
        if "geometry" in linkdict.keys():
            linkdict["geometry"] = dumps(linkdict["geometry"])

    # replace each linestring by its string representation
    for nodedict in node_link_data["nodes"]:
        if "geometry" in nodedict.keys():
            nodedict["geometry"] = dumps(nodedict["geometry"])

    with open(filepath, "w") as f:
        json.dump(node_link_data, f)

    print(f"json serialized graph saved to {filepath}")


### function that reads in a json file into a networkx object
def spatialgraph_fromjson(filepath):
    node_link_data = json.load(open(filepath))

    # load geometries from wkt
    for linkdict in node_link_data["links"]:
        if "geometry" in linkdict.keys():
            linkdict["geometry"] = loads(linkdict["geometry"])

    # load geometries from wkt
    for nodedict in node_link_data["nodes"]:
        if "geometry" in nodedict.keys():
            nodedict["geometry"] = loads(nodedict["geometry"])

    # convert node link data into nx graph object
    G = nx.node_link_graph(node_link_data)

    return G


### convert a geodataframe of linestrings into a networkx graph
def get_graph_from_gdf(gdf):
    # get "noded" gdf
    n = shapely.node(gdf.unary_union)
    n = gpd.GeoDataFrame({"geometry": [n]}, crs=gdf.crs)
    n = n.explode(index_parts=False).reset_index(drop=True)
    n["id"] = n.index

    # make graph
    Gdir = momepy.gdf_to_nx(n, multigraph=False)
    G = Gdir.to_undirected()
    print("comps:", len([c for c in nx.connected_components(G)]))
    print("degrees:", nx.degree_histogram(G))

    return G


def get_node_gdf(G, return_degrees=True):
    mycrs = G.graph["crs"]

    # get nodes gdf
    nodes = gpd.GeoDataFrame(
        {"geometry": [Point(node) for node in G.nodes], "id": list(G.nodes)}, crs=mycrs
    )

    # add degree info
    if return_degrees == True:
        nodes["degree"] = nodes.apply(lambda x: G.degree(x.id), axis=1)

    return nodes


def get_edge_gdf(G, return_components=True):
    mycrs = G.graph["crs"]

    # get edge gdf
    geomdict = nx.get_edge_attributes(G, "geometry")

    edges = gpd.GeoDataFrame(
        {"geometry": geomdict.values(), "id": geomdict.keys()}, crs=mycrs
    )

    if return_components == True:
        comps = [c for c in nx.connected_components(G)]

        edges["component_nr"] = None

        for i, comp in enumerate(comps):
            l1 = list(G.edges(comp))

            # accounting for the edge id indexing mess
            l2 = [(l[1], l[0]) for l in l1]
            l = l1 + l2

            edges.loc[edges["id"].isin(l), "component_nr"] = i

    return edges
