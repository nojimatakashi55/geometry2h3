# coding:utf-8
from geometry2h3.geometry_h3 import GeometryH3
import geometry2h3.to_shapely_api as to_shapely_api

def _fill_h3_from(h3_resolution, func, *args, h3_contain="overlap"):
    g = GeometryH3(h3_resolution)
    func(g, *args)

    return g.fill_h3(h3_contain=h3_contain)

def fill_h3_from_shapely(h3_resolution, shape, h3_contain="overlap"):
    try:
        func = lambda g, shape : g.set_shapely(shape)

        return _fill_h3_from(h3_resolution, func, shape, h3_contain=h3_contain)

    except Exception as e:
        raise ValueError(f"Failed to fill h3 from shapely: {e}")

def fill_h3_from_wkt(h3_resolution, wkt_str, h3_contain="overlap"):
    try:
        geom = to_shapely_api.wkt_to_shapely(wkt_str)

        return fill_h3_from_shapely(h3_resolution, geom, h3_contain=h3_contain)

    except Exception as e:
        raise ValueError(f"Failed to fill h3 from WKT: {e}")

def fill_h3_from_wkb(h3_resolution, wkb_str, h3_contain="overlap"):
    try:
        geom = to_shapely_api.wkb_to_shapely(wkb_str)

        return fill_h3_from_shapely(h3_resolution, geom, h3_contain=h3_contain)

    except Exception as e:
        raise ValueError(f"Failed to fill h3 from WKB: {e}")

def fill_h3_from_geojson_dict(h3_resolution, geojson_dict, h3_contain="overlap"):
    try:
        geom = to_shapely_api.geojson_dict_to_shapely(geojson_dict)

        return fill_h3_from_shapely(h3_resolution, geom, h3_contain=h3_contain)

    except Exception as e:
        raise ValueError(f"Failed to fill h3 from geojson dict: {e}")

def fill_h3_from_geojson_str(h3_resolution, geojson_str, h3_contain="overlap"):
    try:
        geom = to_shapely_api.geojson_str_to_shapely(geojson_str)

        return fill_h3_from_shapely(h3_resolution, geom, h3_contain=h3_contain)

    except Exception as e:
        raise ValueError(f"Failed to fill h3 from geojson str: {e}")

def fill_h3_from_polyline(h3_resolution, encoded_str, h3_contain="overlap"):
    try:
        geom = to_shapely_api.polyline_to_shapely(encoded_str)

        return fill_h3_from_shapely(h3_resolution, geom, h3_contain=h3_contain)

    except Exception as e:
        raise ValueError(f"Failed to fill h3 from polyline: {e}")

def fill_h3_from_tile(h3_resolution, z, x, y, h3_contain="overlap"):
    try:
        geom = to_shapely_api.tile_to_shapely(z, x, y)

        return fill_h3_from_shapely(h3_resolution, geom, h3_contain=h3_contain)

    except Exception as e:
        raise ValueError(f"Failed to fill h3 from tile: {e}")

def fill_h3_from_bbox(h3_resolution, min_lat, min_lon, max_lat, max_lon, h3_contain="overlap"):
    try:
        geom = to_shapely_api.bbox_to_shapely(min_lat, min_lon, max_lat, max_lon)

        return fill_h3_from_shapely(h3_resolution, geom, h3_contain=h3_contain)

    except Exception as e:
        raise ValueError(f"Failed to fill h3 from bounding box: {e}")

def fill_h3_from_center_radius(h3_resolution, lat, lon, radius_meter, h3_contain="overlap"):
    try:
        geom = to_shapely_api.center_radius_to_shapely(lat, lon, radius_meter)

        return fill_h3_from_shapely(h3_resolution, geom, h3_contain=h3_contain)

    except Exception as e:
        raise ValueError(f"Failed to fill h3 from center radius: {e}")
