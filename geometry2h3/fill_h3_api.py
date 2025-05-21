# coding:utf-8
from geometry2h3.geometry import Geometry

def _fill_h3_from(func, *args, h3_resolution, polygon_h3_contain):
    g = Geometry(h3_resolution, polygon_h3_contain)
    func(g, *args)

    return g.fill_h3()

def fill_h3_from_shapely(shape, h3_resolution, polygon_h3_contain="overlap"):
    func = lambda g, shape : g.set_shapely(shape)

    return _fill_h3_from(func, shape, h3_resolution=h3_resolution, polygon_h3_contain=polygon_h3_contain)

def fill_h3_from_wkt(wkt_str, h3_resolution, polygon_h3_contain="overlap"):
    func = lambda g, wkt_str : g.set_wkt(wkt_str)

    return _fill_h3_from(func, wkt_str, h3_resolution=h3_resolution, polygon_h3_contain=polygon_h3_contain)

def fill_h3_from_geojson(geojson_dict, h3_resolution, polygon_h3_contain="overlap"):
    func = lambda g, geojson_dict : g.set_geojson(geojson_dict)

    return _fill_h3_from(func, geojson_dict, h3_resolution=h3_resolution, polygon_h3_contain=polygon_h3_contain)

def fill_h3_from_polyline(encoded_str, h3_resolution, polygon_h3_contain="overlap"):
    func = lambda g, encoded_str : g.set_polyline(encoded_str)

    return _fill_h3_from(func, encoded_str, h3_resolution=h3_resolution, polygon_h3_contain=polygon_h3_contain)

def fill_h3_from_tile(z, x, y, h3_resolution, polygon_h3_contain="overlap"):
    func = lambda g, z, x, y : g.set_tile(z, x, y)

    return _fill_h3_from(func, z, x, y, h3_resolution=h3_resolution, polygon_h3_contain=polygon_h3_contain)

def fill_h3_from_bbox(min_lat, min_lon, max_lat, max_lon, h3_resolution, polygon_h3_contain="overlap"):
    func = lambda g, min_lat, min_lon, max_lat, max_lon : g.set_bbox(min_lat, min_lon, max_lat, max_lon)

    return _fill_h3_from(func, min_lat, min_lon, max_lat, max_lon, h3_resolution=h3_resolution, polygon_h3_contain=polygon_h3_contain)

def fill_h3_from_center_radius(lat, lon, radius_meter, h3_resolution, polygon_h3_contain="overlap"):
    func = lambda g, lat, lon, radius_meter : g.set_center_radius(lat, lon, radius_meter)

    return _fill_h3_from(func, lat, lon, radius_meter, h3_resolution=h3_resolution, polygon_h3_contain=polygon_h3_contain)
