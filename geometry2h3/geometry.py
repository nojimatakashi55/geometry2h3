# coding:utf-8
from shapely.geometry.base import BaseGeometry
from shapely import wkt
from shapely.geometry import shape, box, mapping, Polygon, Point
import h3
import functools
import itertools

from geometry2h3.polyline_shape import PolylineShape
from geometry2h3.tile_shape import TileShape
from geometry2h3.center_radius_shape import CenterRadiusShape

POLYGON_H3_CONTAIN_SET = {
    "overlap",          # h3 is partially contained in shape
    "center",           # h3 center is contained in shape
    "full",             # h3 is fully contained in shape
    "bbox_overlap",     # h3 bounding box is partially contained in shape
    "outline_overlap",  # h3 is partially contained in outline
}

class Geometry(object):
    def __init__(self, h3_resolution, polygon_h3_contain="overlap"):
        self.h3_resolution = h3_resolution
        self.polygon_h3_contain = polygon_h3_contain if polygon_h3_contain in POLYGON_H3_CONTAIN_SET else "overlap"
        self.geoms = []
        self.h3_set = set()

    def __repr__(self):
        geom_types = list(map(lambda x : x.geom_type, self.geoms))
        h3_cells_count = len(self.h3_set)

        return f"<Geometry(h3_resolution={self.h3_resolution}, polygon_h3_contain={self.polygon_h3_contain}, geom_types={geom_types}, h3_cells_count={h3_cells_count})>"

    def set_shapely(self, shapely_geom, append=False):
        try:
            if not isinstance(shapely_geom, BaseGeometry):
                raise TypeError("Invalid shapely geometry instance")

            if not shapely_geom.is_valid:
                raise ValueError("Invalid shapely geometry")

            if append:
                self.geoms.append(shapely_geom)

            else:
                self.geoms = [shapely_geom]

        except Exception as e:
            raise type(e)(f"Failed to set shapely geometry: {e}")

    def set_wkt(self, wkt_str, append=False):
        try:
            geom = wkt.loads(wkt_str)
            self.set_shapely(geom, append)

        except Exception as e:
            raise ValueError(f"Failed to set WKT geometry: {e}")

    def set_geojson(self, geojson_dict, append=False):
        try:
            geom = shape(geojson_dict)
            self.set_shapely(geom, append)

        except Exception as e:
            raise ValueError(f"Failed to set geojson geometry: {e}")

    def set_bbox(self, min_lat, min_lon, max_lat, max_lon, append=False):
        try:
            geom = box(min_lon, min_lat, max_lon, max_lat)
            self.set_shapely(geom, append)

        except Exception as e:
            raise ValueError(f"Failed to set box geometry: {e}")

    def set_polyline(self, encoded_str, append=False):
        try:
            geom = PolylineShape(encoded_str)
            self.set_shapely(geom, append)

        except Exception as e:
            raise ValueError(f"Failed to set polyline geometry: {e}")

    def set_tile(self, z, x, y, append=False):
        try:
            geom = TileShape(z, x, y)
            self.set_shapely(geom, append)

        except Exception as e:
            raise ValueError(f"Failed to set tile geometry: {e}")

    def set_center_radius(self, lat, lon, radius_meter, append=False):
        try:
            geom = CenterRadiusShape(lat, lon, radius_meter)
            self.set_shapely(geom, append)

        except Exception as e:
            raise ValueError(f"Failed to set center radius geometry: {e}")

    def __h3_point_geom(self, point_geom):
        return {
            h3.latlng_to_cell(point_geom.y, point_geom.x, self.h3_resolution)
        }

    def __h3_line_geom(self, line_geom):
        h3_list = list(map(lambda x : h3.latlng_to_cell(x[1], x[0], self.h3_resolution), line_geom.coords))

        h3_iter = itertools.zip_longest(h3_list, h3_list[1:])
        h3_iter = map(lambda x : h3.grid_path_cells(x[0], x[1]) if x[1] is not None and x[0] != x[1] else [x[0]], h3_iter)
        h3_iter = itertools.chain(*h3_iter)
        h3_iter = map(lambda x : h3.grid_ring(x, 1), h3_iter)
        h3_iter = itertools.chain(*h3_iter)
        h3_iter = set(h3_iter)
        h3_iter = map(lambda x : (x, h3.cell_to_boundary(x)), h3_iter)
        h3_iter = map(lambda x : (x[0], Polygon(map(lambda y : (y[1], y[0]), x[1]))), h3_iter)
        h3_iter = filter(lambda x : line_geom.crosses(x[1]), h3_iter)
        h3_iter = map(lambda x : x[0], h3_iter)
        h3_set = set(h3_iter)

        return h3_set

    def __h3_polygon_geom(self, polygon_geom):
        if self.polygon_h3_contain == "outline_overlap":
            return self.__h3_line_geom(polygon_geom.exterior)

        else:
            h3_set_fill = set(h3.polygon_to_cells(h3.geo_to_h3shape(mapping(Polygon(polygon_geom.exterior))), self.h3_resolution))

            if self.polygon_h3_contain == "overlap":
                h3_set_exterior = self.__h3_line_geom(polygon_geom.exterior)
                h3_iter = h3_set_fill | h3_set_exterior
                h3_iter = map(lambda x : (x, h3.cell_to_boundary(x)), h3_iter)
                h3_iter = map(lambda x : (x[0], Polygon(map(lambda y : (y[1], y[0]), x[1]))), h3_iter)

                f_filter = lambda x : polygon_geom.overlaps(x[1])

            elif self.polygon_h3_contain == "full":
                h3_iter = map(lambda x : (x, h3.cell_to_boundary(x)), h3_set_fill)
                h3_iter = map(lambda x : (x[0], Polygon(map(lambda y : (y[1], y[0]), x[1]))), h3_iter)

                f_filter = lambda x : polygon_geom.contains(x[1])

            elif self.polygon_h3_contain == "center":
                h3_set_exterior = self.__h3_line_geom(polygon_geom.exterior)
                h3_iter = h3_set_fill | h3_set_exterior
                h3_iter = map(lambda x : (x, h3.cell_to_latlng(x)), h3_iter)

                f_filter = lambda x : polygon_geom.contains(Point(x[1][1], x[1][0]))

            elif self.polygon_h3_contain == "bbox_overlap":
                h3_set_exterior = self.__h3_line_geom(polygon_geom.exterior)
                h3_iter = h3_set_fill | h3_set_exterior
                h3_iter = map(lambda x : (x, h3.cell_to_boundary(x)), h3_iter)
                f_lat = lambda x : x[0]
                f_lon = lambda x : x[1]
                h3_iter = map(lambda x : (
                    x[0],
                    (
                        min(map(f_lon, x[1])),
                        min(map(f_lat, x[1])),
                        max(map(f_lon, x[1])),
                        max(map(f_lat, x[1]))
                    )
                ), h3_iter)
                h3_iter = map(lambda x : (x[0], box(*x[1])), h3_iter)

                f_filter = lambda x : polygon_geom.overlaps(x[1])

            h3_iter = filter(f_filter, h3_iter)
            h3_iter = map(lambda x : x[0], h3_iter)
            h3_set = set(h3_iter)

            return h3_set

    def __h3_fill_geom(self, geom):
        if geom.geom_type == "Point":
            return self.__h3_point_geom(geom)

        elif geom.geom_type == "LineString" \
             or geom.geom_type == "LinearRing":
            return self.__h3_line_geom(geom)

        elif geom.geom_type == "Polygon":
            return self.__h3_polygon_geom(geom)

        elif geom.geom_type == "MultiPoint" \
             or geom.geom_type == "MultiLineString" \
             or geom.geom_type == "MultiPolygon" \
             or geom.geom_type == "GeometryCollection":
            return self.__h3_fill_geoms(geom.geoms)

        else:
            return set()

    def __h3_fill_geoms(self, geoms):
        h3_set_iter = map(lambda x : self.__h3_fill_geom(x), geoms)
        h3_set = functools.reduce(lambda x1,x2 : x1 | x2, h3_set_iter, set())

        return h3_set

    def fill_h3(self):
        self.h3_set = self.__h3_fill_geoms(self.geoms)

        return self.h3_set
