# coding:utf-8
from shapely.geometry import Polygon, box
import math

class TileShape(Polygon):
    def __init__(self, z, x, y):
        self.z = z
        self.x = x
        self.y = y

        north_west_location = self.__north_west_location(self.z, self.x, self.y)
        south_east_location = self.__north_west_location(self.z, self.x+1, self.y+1)
        self.box = box(
            south_east_location[1],
            south_east_location[0],
            north_west_location[1],
            north_west_location[0]
        )

        super().__init__(self.box.exterior.coords)

    def __north_west_location(self, z, x, y):
        lon = (x / 2.0**z) * 360 - 180
        mapy = (y / 2.0**z) * 2 * math.pi - math.pi
        lat = 2 * math.atan(math.e ** (-mapy)) * 180 / math.pi - 90

        return (lat, lon)

    def __repr__(self):
        poly_repr = super().__repr__()

        return f"<TileShape(z={self.z}, x={self.x}, y={self.y}) {poly_repr}>"
