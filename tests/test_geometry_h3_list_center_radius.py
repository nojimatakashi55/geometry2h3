# tests/test_geometry_list_wkt.py
import pytest
from geometry2h3.geometry_h3 import GeometryH3

def test_geometry_list_center_radius():
    lat = 36.69894001299462
    lon = 138.31282262004888
    radius_meter = 10000

    g = GeometryH3(h3_resolution=7)
    g.set_center_radius(lat, lon, radius_meter)
    g.fill_h3()

    assert len(g.geoms) == 1
    assert g.geoms[0].geom_type == "Polygon"
    assert len(g.h3_list) > 0

@pytest.mark.parametrize(
    ["lat", "lon", "radius_meter"],
    [
        (None, None, None),
        ("a", "b", "c")
    ]
)
def test_geometry_list_center_radius_bad_input(lat, lon, radius_meter):
    g = GeometryH3(h3_resolution=7)

    with pytest.raises(Exception):
        g.set_tile(lat, lon, radius_meter)
        g.fill_h3()
