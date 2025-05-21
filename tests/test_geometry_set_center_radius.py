# tests/test_geometry_set_wkt.py
import pytest
from geometry2h3.geometry import Geometry

def test_geometry_set_center_radius():
    lat = 36.69894001299462
    lon = 138.31282262004888
    radius_meter = 10000

    g = Geometry(h3_resolution=7)
    g.set_center_radius(lat, lon, radius_meter)
    g.fill_h3()

    assert len(g.geoms) == 1
    assert g.geoms[0].geom_type == "Polygon"
    assert len(g.h3_set) > 0
