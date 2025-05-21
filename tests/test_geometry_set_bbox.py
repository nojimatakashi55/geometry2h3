# tests/test_geometry_set_wkt.py
import pytest
from geometry2h3.geometry import Geometry

def test_geometry_set_bbox():
    min_lat = 35.6197
    min_lon = 139.6986016
    max_lat = 35.738062
    max_lon = 139.778837

    g = Geometry(h3_resolution=7)
    g.set_bbox(min_lat, min_lon, max_lat, max_lon)
    g.fill_h3()

    assert len(g.geoms) == 1
    assert g.geoms[0].geom_type == "Polygon"
    assert len(g.h3_set) > 0
