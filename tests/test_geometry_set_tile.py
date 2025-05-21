# tests/test_geometry_set_wkt.py
import pytest
from geometry2h3.geometry import Geometry

def test_geometry_set_tile():
    z = 9
    x = 452
    y = 199

    g = Geometry(h3_resolution=7)
    g.set_tile(z, x, y)
    g.fill_h3()

    assert len(g.geoms) == 1
    assert g.geoms[0].geom_type == "Polygon"
    assert len(g.h3_set) > 0
