# coding:utf-8
from shapely.geometry import Point
import math

EQUATOR_RADIUS = 6378137

class CenterRadiusShape(Polygon):
    def __init__(self, lat, lon, radius_meter):
        self.lat = lat
        self.lon = lon
        self.radius_meter = radius_meter

        coords = self.__polygon().exterior.coords

        super().__init__(coords)

    def __polygon(self):
        d = (360 * 1000) / (2 * math.pi * (EQUATOR_RADIUS * math.cos(self.lat * math.pi / 180.0))) / 1000.0
        buffer_distance = d * self.radius_meter
        polygon = Point(self.lon, self.lat).buffer(buffer_distance)

        return polygon

    def __repr__(self):
        poly_repr = super().__repr__()

        return f"<CenterRadiusShape(lat={self.lat}, lon={self.lon}, radius_meter={self.radius_meter}) {poly_repr}>"
