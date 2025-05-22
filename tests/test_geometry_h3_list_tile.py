# tests/test_geometry_list_wkt.py
import pytest
from geometry2h3.geometry_h3 import GeometryH3

def test_geometry_list_tile():
    z = 9
    x = 452
    y = 199

    g = GeometryH3(h3_resolution=7)
    g.set_tile(z, x, y)
    g.fill_h3()
    g.build_h3_strtree()

    assert len(g.geoms) == 1
    assert g.geoms[0].geom_type == "Polygon"
    assert len(g.h3_list) > 0
    assert g.h3_strtree is not None
    assert len(g.h3_strtree.geometries) > 0

@pytest.mark.parametrize(
    ["z", "x", "y"],
    [
        (None, None, None),
        ("a", "b", "c")
    ]
)
def test_geometry_list_tile_bad_input(z, x, y):
    g = GeometryH3(h3_resolution=7)

    with pytest.raises(Exception):
        g.set_tile(z, x, y)
        g.fill_h3()
        g.build_h3_strtree()
