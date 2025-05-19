# coding:utf-8
from shapely.geometry import LineString
import polyline

class PolylineShape(LineString):
    def __init__(self, encoded_str):
        self.encoded_str = encoded_str

        coords = polyline.decode(encoded_str)

        super().__init__(coords)

    def __repr__(self):
        poly_repr = super().__repr__()

        return f"<PolylineShape(encoded_str={self.encoded_str}) {poly_repr}>"
