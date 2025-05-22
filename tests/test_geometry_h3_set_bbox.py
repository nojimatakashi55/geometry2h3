# tests/test_geometry_set_wkt.py
import pytest
from geometry2h3.geometry_h3 import GeometryH3

def test_geometry_set_bbox():
    min_lat = 35.6197
    min_lon = 139.6986016
    max_lat = 35.738062
    max_lon = 139.778837

    g = GeometryH3(h3_resolution=7)
    g.set_bbox(min_lat, min_lon, max_lat, max_lon)
    g.fill_h3()

    assert len(g.geoms) == 1
    assert g.geoms[0].geom_type == "Polygon"
    assert len(g.h3_set) > 0

@pytest.mark.parametrize(
    ["min_lat", "min_lon", "max_lat", "max_lon"],
    [
        (35.738062, 139.6986016, 35.6197, 139.778837),  # min_lat > max_lat
        (35.6197, 139.778837, 35.738062, 139.6986016),  # min_lon > max_lon
        (None, 139.6986016, 35.738062, 139.778837),     # None as min_lat
        ("a", 139.6986016, 35.738062, 139.778837),      # invalid type
    ]
)
def test_geometry_set_bbox_bad_input(min_lat, min_lon, max_lat, max_lon):
    g = GeometryH3(h3_resolution=7)

    with pytest.raises(ValueError):
        g.set_bbox(min_lat, min_lon, max_lat, max_lon)
        g.fill_h3()
