# coding:utf-8
import shapely
from shapely.geometry import shape, box
import polyline

from geometry2h3.polyline_shape import PolylineShape
from geometry2h3.tile_shape import TileShape
from geometry2h3.center_radius_shape import CenterRadiusShape

def wkt_to_shapely(wkt):
    try:
        return shapely.from_wkt(wkt)

    except Exception as e:
        raise ValueError(f"Failed to set WKT to shapely geometry: {e}")

def wkb_to_shapely(wkb):
    try:
        return shapely.from_wkb(wkb)

    except Exception as e:
        raise ValueError(f"Failed to set WKB to shapely geometry: {e}")

def geojson_dict_to_shapely(geojson_dict):
    try:
        return shape(geojson_dict)

    except Exception as e:
        raise ValueError(f"Failed to set geojson dict to shapely geometry: {e}")

def geojson_str_to_shapely(geojson_str):
    try:
        return shapely.from_geojson(geojson_str)

    except Exception as e:
        raise ValueError(f"Failed to set geojson str to shapely geometry: {e}")

def bbox_to_shapely(min_lat, min_lon, max_lat, max_lon):
    try:
        if min_lat >= max_lat:
            raise ValueError("min_lat must be strictly less than max_lat")

        if min_lon >= max_lon:
            raise ValueError("min_lon must be strictly less than max_lon")

        return box(min_lon, min_lat, max_lon, max_lat)

    except Exception as e:
            raise ValueError(f"Failed to set bounding box to shapely geometry: {e}")

def polyline_to_shapely(encoded_str):
    try:
        return PolylineShape(encoded_str)

    except Exception as e:
        raise ValueError(f"Failed to set polyline to shapely geometry: {e}")

def tile_to_shapely(z, x, y):
    try:
        return TileShape(z, x, y)

    except Exception as e:
        raise ValueError(f"Failed to set tile to shapely geometry: {e}")

def center_radius_to_shapely(lat, lon, radius_meter):
    try:
        return CenterRadiusShape(lat, lon, radius_meter)

    except Exception as e:
        raise ValueError(f"Failed to set center radius to shapely geometry: {e}")
