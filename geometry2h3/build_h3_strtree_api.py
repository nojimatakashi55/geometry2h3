# coding:utf-8
from geometry2h3.geometry_h3 import GeometryH3
import geometry2h3.shapely_geometry_api as shapely_geometry_api

def _build_h3_strtree_from(func, *args, h3_resolution, h3_contain):
    g = GeometryH3(h3_resolution)
    func(g, *args)
    g.fill_h3(h3_contain=h3_contain)

    return g.build_h3_strtree()

def build_h3_strtree_from_shapely(shape, h3_resolution, h3_contain="overlap"):
    try:
        func = lambda g, shape : g.set_shapely(shape)

        return _build_h3_strtree_from(func, shape, h3_resolution=h3_resolution, h3_contain=h3_contain)

    except Exception as e:
        raise ValueError(f"Failed to build h3 strtree from shapely: {e}")

def build_h3_strtree_from_wkt(wkt_str, h3_resolution, h3_contain="overlap"):
    try:
        geom = shapely_geometry_api.wkt_to_shapely(wkt_str)

        return build_h3_strtree_from_shapely(geom, h3_resolution=h3_resolution, h3_contain=h3_contain)

    except Exception as e:
        raise ValueError(f"Failed to build h3 strtree from WKT: {e}")

def build_h3_strtree_from_wkb(wkb_str, h3_resolution, h3_contain="overlap"):
    try:
        geom = shapely_geometry_api.wkb_to_shapely(wkb_str)

        return build_h3_strtree_from_shapely(geom, h3_resolution=h3_resolution, h3_contain=h3_contain)

    except Exception as e:
        raise ValueError(f"Failed to build h3 strtree from WKB: {e}")

def build_h3_strtree_from_geojson_dict(geojson_dict, h3_resolution, h3_contain="overlap"):
    try:
        geom = shapely_geometry_api.geojson_dict_to_shapely(geojson_dict)

        return build_h3_strtree_from_shapely(geom, h3_resolution=h3_resolution, h3_contain=h3_contain)

    except Exception as e:
        raise ValueError(f"Failed to build h3 strtree from geojson dict: {e}")

def build_h3_strtree_from_geojson_str(geojson_str, h3_resolution, h3_contain="overlap"):
    try:
        geom = shapely_geometry_api.geojson_str_to_shapely(geojson_str)

        return build_h3_strtree_from_shapely(geom, h3_resolution=h3_resolution, h3_contain=h3_contain)

    except Exception as e:
        raise ValueError(f"Failed to build h3 strtree from geojson str: {e}")

def build_h3_strtree_from_polyline(encoded_str, h3_resolution, h3_contain="overlap"):
    try:
        geom = shapely_geometry_api.polyline_to_shapely(encoded_str)

        return build_h3_strtree_from_shapely(geom, h3_resolution=h3_resolution, h3_contain=h3_contain)

    except Exception as e:
        raise ValueError(f"Failed to build h3 strtree from polyline: {e}")

def build_h3_strtree_from_tile(z, x, y, h3_resolution, h3_contain="overlap"):
    try:
        geom = shapely_geometry_api.tile_to_shapely(z, x, y)

        return build_h3_strtree_from_shapely(geom, h3_resolution=h3_resolution, h3_contain=h3_contain)

    except Exception as e:
        raise ValueError(f"Failed to build h3 strtree from tile: {e}")

def build_h3_strtree_from_bbox(min_lat, min_lon, max_lat, max_lon, h3_resolution, h3_contain="overlap"):
    try:
        geom = shapely_geometry_api.bbox_to_shapely(min_lat, min_lon, max_lat, max_lon)

        return build_h3_strtree_from_shapely(geom, h3_resolution=h3_resolution, h3_contain=h3_contain)

    except Exception as e:
        raise ValueError(f"Failed to build h3 strtree from bounding box: {e}")

def build_h3_strtree_from_center_radius(lat, lon, radius_meter, h3_resolution, h3_contain="overlap"):
    try:
        geom = shapely_geometry_api.center_radius_to_shapely(lat, lon, radius_meter)

        return build_h3_strtree_from_shapely(geom, h3_resolution=h3_resolution, h3_contain=h3_contain)

    except Exception as e:
        raise ValueError(f"Failed to build h3 strtree from center radius: {e}")
