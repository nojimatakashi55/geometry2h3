# coding:utf-8
import math
from shapely.geometry import box

class TileShape(object):
    def __init__(self, z, x, y):
        self.z = z
        self.x = x
        self.y = y

        self.north_west_location = self.__calc_north_west_location(self.z, self.x, self.y)
        self.south_east_location = self.__calc_north_west_location(self.z, self.x+1, self.y+1)
        self.shape = box(
            self.south_east_location[1],
            self.south_east_location[0],
            self.north_west_location[1],
            self.north_west_location[0]
        )

    def __repr__(self):
        return f"<TileShape(z={self.z}, x={self.x}, y={self.y})>"

    def __calc_north_west_location(self, z, x, y):
        lon = (x / 2.0**z) * 360 - 180
        mapy = (y / 2.0**z) * 2 * math.pi - math.pi
        lat = 2 * math.atan(math.e ** (-mapy)) * 180 / math.pi - 90

        return (lat, lon)
