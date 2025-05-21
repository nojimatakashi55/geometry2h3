# tests/test_geometry_set_wkt.py
import pytest
from geometry2h3.geometry import Geometry

def test_geometry_set_wkt():
    wkt = "POLYGON ((139.728553 35.6197, 139.723444 35.626446, 139.715828 35.633998, 139.710106 35.64669, 139.6993714 35.6586161, 139.702687 35.670168, 139.7020716 35.68304384, 139.6986016 35.68844644, 139.700044 35.701306, 139.703782 35.712285, 139.706587 35.721204, 139.71038 35.728926, 139.729329 35.73159, 139.739345 35.733492, 139.746875 35.736489, 139.76086 35.738062, 139.766787 35.732135, 139.770987 35.727772, 139.778837 35.720495, 139.777254 35.713768, 139.7733663 35.70796362, 139.774219 35.698683, 139.770883 35.69169, 139.766084 35.681382, 139.763328 35.675069, 139.75964 35.665498, 139.756749 35.655646, 139.747575 35.645736, 139.7407 35.6355, 139.74044 35.630152, 139.728553 35.6197))"

    g = Geometry(h3_resolution=7)
    g.set_wkt(wkt)
    g.fill_h3()

    assert len(g.geoms) == 1
    assert g.geoms[0].geom_type == "Polygon"
    assert len(g.h3_set) > 0

@pytest.mark.parametrize("wkt", ["", "???", None])
def test_geometry_set_wkt_bad_input(wkt):
    g = Geometry(h3_resolution=7)

    with pytest.raises(Exception):
        g.set_wkt(wkt)
        g.fill_h3()
