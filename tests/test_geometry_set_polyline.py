# tests/test_geometry_set_wkt.py
import pytest
import polyline
from geometry2h3.geometry import Geometry

def test_geometry_set_polyline():
    coords = [
        (35.681382, 139.766084),
        (35.713768, 139.777254),
        (35.906295, 139.623999),
        (36.3142, 139.80685),
        (36.558701, 139.898283),
        (36.931772, 140.020514),
        (37.094537, 140.18441),
        (37.397983, 140.388412),
        (37.75442, 140.458533),
        (37.995485, 140.633035),
        (38.260297, 140.882049),
        (38.57092, 140.967832),
        (38.74893, 141.071785),
        (38.926283, 141.137586),
        (39.145194, 141.188803),
        (39.282229, 141.122598),
        (39.406453, 141.173715),
        (39.701683, 141.136369),
        (39.960853, 141.217655),
        (40.209936, 141.297394),
        (40.509161, 141.431468),
        (40.719917, 141.153948),
        (40.82749, 140.693449),
        (41.1450992, 140.5155834),
        (41.60107, 140.334926),
        (41.9054, 140.646525),
    ]

    encoded_str = polyline.encode(coords)
    g = Geometry(h3_resolution=7)
    g.set_polyline(encoded_str)
    g.fill_h3()

    assert len(g.geoms) == 1
    assert g.geoms[0].geom_type == "LineString"
    assert len(g.h3_set) > 0

@pytest.mark.parametrize("encoded_str", ["", "abc", None])
def test_geometry_set_polyline_bad_input(encoded_str):
    g = Geometry(h3_resolution=7)

    with pytest.raises(Exception):
        g.set_polyline(encoded_str)
        g.fill_h3()
