# coding:utf-8
from shapely.geometry import LineString
import polyline

class PolylineShape(LineString):
    def __init__(self, encoded_str):
        self.encoded_str = encoded_str

    def __new__(cls, encoded_str):
        coords_latlon = polyline.decode(encoded_str)
        coords_lonlat = list(map(lambda x : (x[1], x[0]), coords_latlon))

        return super().__new__(cls, coords_lonlat)

    def __repr__(self):
        poly_repr = super().__repr__()

        return f"<PolylineShape(encoded_str={self.encoded_str}) {poly_repr}>"
