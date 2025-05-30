# coding:utf-8
from shapely.geometry import Polygon, box
import math

class TileShape(Polygon):
    def __init__(self, z, x, y):
        self.z = z
        self.x = x
        self.y = y

    def __new__(cls, z, x, y):
        north_west_lat, north_west_lon = cls.__north_west_location(z, x, y)
        south_east_lat, south_east_lon = cls.__north_west_location(z, x+1, y+1)
        tile_box = box(
            south_east_lon,
            south_east_lat,
            north_west_lon,
            north_west_lat
        )

        return super().__new__(cls, tile_box.exterior.coords)

    @classmethod
    def __north_west_location(cls, z, x, y):
        lon = (x / 2.0**z) * 360 - 180
        mapy = (y / 2.0**z) * 2 * math.pi - math.pi
        lat = 2 * math.atan(math.e ** (-mapy)) * 180 / math.pi - 90

        return lat, lon

    def __repr__(self):
        poly_repr = super().__repr__()

        return f"<TileShape(z={self.z}, x={self.x}, y={self.y}) {poly_repr}>"
