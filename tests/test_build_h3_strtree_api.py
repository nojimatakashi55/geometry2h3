# tests/test_build_h3_strtree_api.py
import pytest
from shapely.geometry import Polygon
import json
import polyline
import geometry2h3.build_h3_strtree_api as api
from shapely import STRtree

def test_build_h3_strtree_from_shapely():
    shape = Polygon(
        [
            (135.51394, 34.647321),
            (135.500722, 34.650187),
            (135.493042, 34.654178),
            (135.495265, 34.666438),
            (135.479976, 34.665518),
            (135.462608, 34.669165),
            (135.466791, 34.682663),
            (135.474868, 34.688974),
            (135.494977, 34.701909),
            (135.494977, 34.701909),
            (135.512136, 34.704934),
            (135.520324, 34.70492),
            (135.532171, 34.697043),
            (135.534482, 34.68858),
            (135.533846, 34.681101),
            (135.53283, 34.673526),
            (135.529925, 34.665247),
            (135.527889, 34.65855),
            (135.52337, 34.647879),
            (135.51394, 34.647321),
        ],
        [[
            (135.48207498835222, 34.685407567708744),
            (135.4909122264798, 34.690097962056754),
            (135.49408445287045, 34.69249263147169),
            (135.50144949234883, 34.6932584506999),
            (135.50629627480748, 34.692629723093226),
            (135.51057386216462, 34.69111697544301),
            (135.51275290190603, 34.69131079777771),
            (135.50874553858216, 34.692407539999515),
            (135.50482441687262, 34.69392971851826),
            (135.50116202012492, 34.694416620643146),
            (135.49133621800263, 34.69343335903617),
            (135.48748983903636, 34.69171262310632),
            (135.48207498835222, 34.685407567708744),
        ]]
    )

    h3_strtree = api.build_h3_strtree_from_shapely(shape, h3_resolution=7, h3_contain="overlap")

    assert isinstance(h3_strtree, STRtree)
    assert len(h3_strtree.geometries) > 0

def test_build_h3_strtree_from_wkt():
    wkt = "POLYGON ((139.728553 35.6197, 139.723444 35.626446, 139.715828 35.633998, 139.710106 35.64669, 139.6993714 35.6586161, 139.702687 35.670168, 139.7020716 35.68304384, 139.6986016 35.68844644, 139.700044 35.701306, 139.703782 35.712285, 139.706587 35.721204, 139.71038 35.728926, 139.729329 35.73159, 139.739345 35.733492, 139.746875 35.736489, 139.76086 35.738062, 139.766787 35.732135, 139.770987 35.727772, 139.778837 35.720495, 139.777254 35.713768, 139.7733663 35.70796362, 139.774219 35.698683, 139.770883 35.69169, 139.766084 35.681382, 139.763328 35.675069, 139.75964 35.665498, 139.756749 35.655646, 139.747575 35.645736, 139.7407 35.6355, 139.74044 35.630152, 139.728553 35.6197))"

    h3_strtree = api.build_h3_strtree_from_wkt(wkt, h3_resolution=7, h3_contain="overlap")

    assert isinstance(h3_strtree, STRtree)
    assert len(h3_strtree.geometries) > 0

def test_build_h3_strtree_from_wkb():
    wkb = b'\x01\x03\x00\x00\x00\x01\x00\x00\x00\x1f\x00\x00\x00\xe3\x8caNPwa@e\xaa`TR\xcfA@\x99\x0f\x08t&wa@\xe2Z\xeda/\xd0A@\xf41\x1f\x10\xe8va@]\xdd\xb1\xd8&\xd1A@0\xd670\xb9va@;S\xe8\xbc\xc6\xd2A@?X!@ava@>\x0fI\x88M\xd4A@a\x8ari|va@\xb1i\xa5\x10\xc8\xd5A@j.\xdc^wva@cD\x05\xfbm\xd7A@\xdd\x1d\xbe\xf1Zva@\x7flP\x03\x1f\xd8A@Z\xb8\xac\xc2fva@\x8a>\x1fe\xc4\xd9A@n0\xd4a\x85va@77\xa6\',\xdbA@\xec\x18W\\\x9cva@H\xdf\xa4iP\xdcA@pw\xd6n\xbbva@ \x9ayrM\xddA@\xc8`\xc5\xa9Vwa@R\n\xba\xbd\xa4\xddA@\xc1n\xd8\xb6\xa8wa@V\xf0\xdb\x10\xe3\xddA@ffff\xe6wa@\x8fn\x84EE\xdeA@\xb5\x1a\x12\xf7Xxa@\xce5\xcc\xd0x\xdeA@\xef\xff\xe3\x84\x89xa@\xe4\xa0\x84\x99\xb6\xddA@\x84\xd4\xed\xec\xabxa@\xe6x\x05\xa2\'\xddA@F}\x92;\xecxa@<\xf7\x1e.9\xdcA@\xed\xd5\xc7C\xdfxa@6w\xf4\xbf\\\xdbA@\x83\xca\xaej\xbfxa@2TI\x8d\x9e\xdaA@#\x9e\xecf\xc6xa@\xb6\xa2\xcdqn\xd9A@[A\xd3\x12\xabxa@1|DL\x89\xd8A@\xa5\xbf\x97\xc2\x83xa@\xa2\n\x7f\x867\xd7A@\xe0\x83\xd7.mxa@\x8f\xc56\xa9h\xd6A@x\x97\x8b\xf8Nxa@\xd6\xc6\xd8\t/\xd5A@\xfc\xc8\xadI7xa@i\xe0G5\xec\xd3A@\xd5\th"\xecwa@\xc8\xec,z\xa7\xd2A@\xb6\x84|\xd0\xb3wa@\xd3Mb\x10X\xd1A@\xcf\x14:\xaf\xb1wa@\'\xc1\x1b\xd2\xa8\xd0A@\xe3\x8caNPwa@e\xaa`TR\xcfA@'

    h3_strtree = api.build_h3_strtree_from_wkb(wkb, h3_resolution=7, h3_contain="overlap")

    assert isinstance(h3_strtree, STRtree)
    assert len(h3_strtree.geometries) > 0

def test_build_h3_strtree_from_geojson_dict():
    geojson = {
        "type": "Polygon",
        "coordinates": [
            [
                (135.51394, 34.647321),
                (135.500722, 34.650187),
                (135.493042, 34.654178),
                (135.495265, 34.666438),
                (135.479976, 34.665518),
                (135.462608, 34.669165),
                (135.466791, 34.682663),
                (135.474868, 34.688974),
                (135.494977, 34.701909),
                (135.494977, 34.701909),
                (135.512136, 34.704934),
                (135.520324, 34.70492),
                (135.532171, 34.697043),
                (135.534482, 34.68858),
                (135.533846, 34.681101),
                (135.53283, 34.673526),
                (135.529925, 34.665247),
                (135.527889, 34.65855),
                (135.52337, 34.647879),
                (135.51394, 34.647321)
            ],
            [
                (135.48207498835222, 34.685407567708744),
                (135.4909122264798, 34.690097962056754),
                (135.49408445287045, 34.69249263147169),
                (135.50144949234883, 34.6932584506999),
                (135.50629627480748, 34.692629723093226),
                (135.51057386216462, 34.69111697544301),
                (135.51275290190603, 34.69131079777771),
                (135.50874553858216, 34.692407539999515),
                (135.50482441687262, 34.69392971851826),
                (135.50116202012492, 34.694416620643146),
                (135.49133621800263, 34.69343335903617),
                (135.48748983903636, 34.69171262310632),
                (135.48207498835222, 34.685407567708744)
            ]
        ]
    }

    h3_strtree = api.build_h3_strtree_from_geojson_dict(geojson, h3_resolution=7, h3_contain="overlap")

    assert isinstance(h3_strtree, STRtree)
    assert len(h3_strtree.geometries) > 0

def test_build_h3_strtree_from_geojson_str():
    geojson_dict = {
        "type": "Polygon",
        "coordinates": [
            [
                (135.51394, 34.647321),
                (135.500722, 34.650187),
                (135.493042, 34.654178),
                (135.495265, 34.666438),
                (135.479976, 34.665518),
                (135.462608, 34.669165),
                (135.466791, 34.682663),
                (135.474868, 34.688974),
                (135.494977, 34.701909),
                (135.494977, 34.701909),
                (135.512136, 34.704934),
                (135.520324, 34.70492),
                (135.532171, 34.697043),
                (135.534482, 34.68858),
                (135.533846, 34.681101),
                (135.53283, 34.673526),
                (135.529925, 34.665247),
                (135.527889, 34.65855),
                (135.52337, 34.647879),
                (135.51394, 34.647321)
            ],
            [
                (135.48207498835222, 34.685407567708744),
                (135.4909122264798, 34.690097962056754),
                (135.49408445287045, 34.69249263147169),
                (135.50144949234883, 34.6932584506999),
                (135.50629627480748, 34.692629723093226),
                (135.51057386216462, 34.69111697544301),
                (135.51275290190603, 34.69131079777771),
                (135.50874553858216, 34.692407539999515),
                (135.50482441687262, 34.69392971851826),
                (135.50116202012492, 34.694416620643146),
                (135.49133621800263, 34.69343335903617),
                (135.48748983903636, 34.69171262310632),
                (135.48207498835222, 34.685407567708744)
            ]
        ]
    }
    geojson_str = json.dumps(geojson_dict)

    h3_strtree = api.build_h3_strtree_from_geojson_str(geojson_str, h3_resolution=7, h3_contain="overlap")

    assert isinstance(h3_strtree, STRtree)
    assert len(h3_strtree.geometries) > 0

def test_build_h3_strtree_from_polyline():
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

    h3_strtree = api.build_h3_strtree_from_polyline(encoded_str, h3_resolution=7, h3_contain="overlap")

    assert isinstance(h3_strtree, STRtree)
    assert len(h3_strtree.geometries) > 0

def test_build_h3_strtree_from_tile():
    z = 9
    x = 452
    y = 199

    h3_strtree = api.build_h3_strtree_from_tile(z, x, y, h3_resolution=7, h3_contain="overlap")

    assert isinstance(h3_strtree, STRtree)
    assert len(h3_strtree.geometries) > 0

def test_build_h3_strtree_from_bbox():
    min_lat = 35.6197
    min_lon = 139.6986016
    max_lat = 35.738062
    max_lon = 139.778837

    h3_strtree = api.build_h3_strtree_from_bbox(min_lat, min_lon, max_lat, max_lon, h3_resolution=7, h3_contain="overlap")

    assert isinstance(h3_strtree, STRtree)
    assert len(h3_strtree.geometries) > 0

def test_build_h3_strtree_from_center_radius():
    lat = 36.69894001299462
    lon = 138.31282262004888
    radius_meter = 10000

    h3_strtree = api.build_h3_strtree_from_center_radius(lat, lon, radius_meter, h3_resolution=7, h3_contain="overlap")

    assert isinstance(h3_strtree, STRtree)
    assert len(h3_strtree.geometries) > 0
