# tests/test_fill_h3_nearest_h3_api.py
import pytest
from shapely.geometry import Polygon
import geometry2h3.fill_h3_nearest_h3_api as api

h3_resolution = 7

polygon1 = Polygon([
    (139.728553, 35.6197),
    (139.723444, 35.626446),
    (139.715828, 35.633998),
    (139.710106, 35.64669),
    (139.6993714, 35.6586161),
    (139.702687, 35.670168),
    (139.7020716, 35.68304384),
    (139.6986016, 35.68844644),
    (139.700044, 35.701306),
    (139.703782, 35.712285),
    (139.706587, 35.721204),
    (139.71038, 35.728926),
    (139.729329, 35.73159),
    (139.739345, 35.733492),
    (139.746875, 35.736489),
    (139.76086, 35.738062),
    (139.766787, 35.732135),
    (139.770987, 35.727772),
    (139.778837, 35.720495),
    (139.777254, 35.713768),
    (139.7733663, 35.70796362),
    (139.774219, 35.698683),
    (139.770883, 35.69169),
    (139.766084, 35.681382),
    (139.763328, 35.675069),
    (139.75964, 35.665498),
    (139.756749, 35.655646),
    (139.747575, 35.645736),
    (139.7407, 35.6355),
    (139.74044, 35.630152),
    (139.728553, 35.6197),
])
polygon2 = Polygon(
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

lat, lon = (36.69884457953947, 138.3129466385537)

def test_fill_h3_from_shapely_nearest_h3_shapely():
    h3_nearest = api.fill_h3_from_shapely_nearest_h3_shapely(h3_resolution, polygon1, polygon2)

    assert isinstance(h3_nearest, str)
    assert len(h3_nearest) > 0

def test_fill_h3_from_shapely_nearest_h3_location():
    h3_nearest = api.fill_h3_from_shapely_nearest_h3_location(h3_resolution, polygon1, lat, lon)

    assert isinstance(h3_nearest, str)
    assert len(h3_nearest) > 0
