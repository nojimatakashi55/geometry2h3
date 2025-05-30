# coding:utf-8
from shapely.geometry import Polygon, Point
import math

EQUATOR_RADIUS = 6378137

class CenterRadiusShape(Polygon):
    def __init__(self, lat, lon, radius_meter):
        self.lat = lat
        self.lon = lon
        self.radius_meter = radius_meter

    def __new__(cls, lat, lon, radius_meter):
        buffer_distance = cls.__buffer_distance(lat, lon, radius_meter)
        polygon = Point(lon, lat).buffer(buffer_distance)

        return super().__new__(cls, polygon.exterior.coords)

    @classmethod
    def __buffer_distance(cls, lat, lon, radius_meter):
        d = (360 * 1000) / (2 * math.pi * (EQUATOR_RADIUS * math.cos(lat * math.pi / 180.0))) / 1000.0
        buffer_distance = d * radius_meter

        return buffer_distance

    def __repr__(self):
        poly_repr = super().__repr__()

        return f"<CenterRadiusShape(lat={self.lat}, lon={self.lon}, radius_meter={self.radius_meter}) {poly_repr}>"
