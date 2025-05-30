# coding:utf-8
from geometry2h3.geometry_h3 import GeometryH3

def fill_h3_from_shapely_nearest_h3_shapely(h3_resolution, shape_fill, shape_nearest, h3_contain_fill="overlap"):
    try:
        g = GeometryH3(h3_resolution)
        g.set_shapely(shape_fill)
        g.fill_h3(h3_contain_fill)

        return g.nearest_h3_shapely(shape_nearest)

    except Exception as e:
        raise ValueError(f"Failed to fill h3 and get the nearest h3: {e}")

def fill_h3_from_shapely_nearest_h3_location(h3_resolution, shape_fill, lat_nearest, lon_nearest, h3_contain_fill="overlap"):
    try:
        g = GeometryH3(h3_resolution)
        g.set_shapely(shape_fill)
        g.fill_h3(h3_contain_fill)

        return g.nearest_h3_location(lat_nearest, lon_nearest)

    except Exception as e:
        raise ValueError(f"Failed to fill h3 and get the nearest h3: {e}")
