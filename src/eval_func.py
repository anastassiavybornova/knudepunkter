# import libraries
import os

os.environ["USE_PYGEOS"] = "0"  # pygeos/shapely2.0/osmnx conflict solving
import geopandas as gpd
import pandas as pd
from shapely import strtree


def evaluate_polygon_layer(poly, edges, polygon_buffer=100):
    """
    find out where study_area linestrings intersect with a given
    polygon layer. linestrings are buffered with a default of 100m.
    both input gdfs must be in the same projected CRS.
    keep track of which, and how many, types (from poly layer)
    each of the edge segments intersects with (to track variation).
    """

    assert poly.crs == edges.crs

    # explode edges
    edges = edges.explode(index_parts=False)

    # buffer polygons
    poly["geometry"] = poly.buffer(polygon_buffer)
    poly_area = poly.unary_union

    # strtree query to find which edge intersects with which type of polygon
    # (to check for variation)

    # make strtree of edge geoms
    mytree = strtree.STRtree(geoms=poly.geometry)
    type_inter = []  # list to add as column after for-loop

    # for each polygon,
    for ix, row in edges.iterrows():
        # find intersection of polygon with edges
        q = mytree.query(row.geometry, predicate="intersects")
        # combining all unique (cf set()), sorted types in a string (so hashable)
        types = ""
        for t in sorted(list(set(poly.loc[q, "type"]))):
            types += t + "_"  # adding _ after each type (to count)
        type_inter.append(types)  # append to list of sets

    edges["type_inter"] = type_inter
    edges["type_count"] = edges.apply(lambda x: x.type_inter.count("_"), axis=1)

    # we already know with what "type" of polygon they intersect;
    # now we find the geometries of the intersections:
    geoms_inter = edges.intersection(poly_area)
    gdf_inter = gpd.GeoDataFrame(
        {
            "geometry": geoms_inter,
            "types": edges["type_inter"],
            "types_count": edges["type_count"],
        },
        crs=edges.crs,
    )

    # explode multilinestrings
    gdf_inter = gdf_inter.explode(index_parts=False)
    # remove empty geoms
    gdf_inter = gdf_inter[-gdf_inter.is_empty].reset_index(drop=True)
    # remove non-linestring geoms
    gdf_inter = gdf_inter[gdf_inter.type == "LineString"].reset_index(drop=True)

    return gdf_inter


def evaluate_point_layer(points, edges, points_buffer):
    """
    find out where buffered study_area linestrings intersect with a given
    point layer. both input gdfs must be in the same projected CRS.
    keep track of which, and how many, types (from poly layer)
    each of the edge segments intersects with (to track variation).
    """

    assert points.crs == edges.crs

    # explode points
    points = points.explode(index_parts=False)

    # explode edges
    edges = edges.explode(index_parts=False)

    # buffer edges
    edges_buff = edges.copy()
    edges_buff["geometry"] = edges_buff.buffer(points_buffer)
    edges_buff_area = edges_buff.unary_union

    # return gdf of points with info whether they are within reach or not
    points["withinreach"] = 0
    # make strtree of edge geoms
    mytree = strtree.STRtree(geoms=points.geometry)
    q = mytree.query(edges_buff_area, predicate="intersects")
    # the ones that intersect with the buffered edge area, are within reach
    points.loc[q, "withinreach"] = 1

    # not included, but maybe later? also return edges with info WHICH point is within reach
    # (again, accounting for variation)

    return points
