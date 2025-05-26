# coding:utf-8
from shapely.geometry.base import BaseGeometry
from shapely.geometry import box, mapping, Polygon, Point
from shapely import STRtree
import h3
import functools
import itertools

'''
POINT_H3_CONTAIN_OPTION
  "overlap"  : h3 is partially contained in shape (default)

LINE_H3_CONTAIN_OPTION
  "overlap"  : h3 is partially contained in shape (default)
  "vertices" : h3 is on vertices in shape

POLYGON_H3_CONTAIN_OPTION
  "overlap"  : h3 is partially contained in shape (default)
  "full"     : h3 is fully contained in shape
  "center"   : h3 center is contained in shape
  "vertices" : h3 is on vertices in shape outline
  "outline"  : h3 is partially contained in shape outline
'''

class GeometryH3(object):
    def __init__(self, h3_resolution):
        self.h3_resolution = h3_resolution
        self.geoms = []
        self.h3_list = []
        self.h3_strtree = None

    def __repr__(self):
        geom_types = list(map(lambda x : x.geom_type, self.geoms))
        h3_cells_count = len(self.h3_list)
        h3_strtree_count = len(self.h3_strtree.geometries) if self.h3_strtree is not None else 0

        return f"<GeometryH3(h3_resolution={self.h3_resolution}, geom_types={geom_types}, h3_cells_count={h3_cells_count}, h3_strtree_count={h3_strtree_count})>"

    def set_shapely(self, shapely_geom, append=False):
        try:
            if not isinstance(shapely_geom, BaseGeometry) or not shapely_geom.is_valid or shapely_geom.is_empty:
                raise ValueError("Invalid shapely geometry instance")

            if append:
                self.geoms.append(shapely_geom)

            else:
                self.geoms = [shapely_geom]

        except ValueError as e:
            raise ValueError(f"Failed to set shapely geometry: {e}")

    def __h3_set_point_geom(self, point_geom):
        # h3_contain == "overlap" only
        return {
            h3.latlng_to_cell(point_geom.y, point_geom.x, self.h3_resolution)
        }

    def __h3_set_line_geom(self, line_geom, h3_contain):
        # h3_contain == "vertices" or others (default)
        h3_list = list(map(lambda x : h3.latlng_to_cell(x[1], x[0], self.h3_resolution), line_geom.coords))

        if h3_contain == "vertices":
            return set(h3_list)

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

    def __h3_set_polygon_geom(self, polygon_geom, h3_contain):
        if h3_contain == "vertices" or h3_contain == "outline":
            return self.__h3_set_line_geom(polygon_geom.exterior, h3_contain)

        elif h3_contain == "full":
            return set(h3.polygon_to_cells(h3.geo_to_h3shape(mapping(Polygon(polygon_geom.exterior))), self.h3_resolution))

        else:
            h3_set_fill = set(h3.polygon_to_cells(h3.geo_to_h3shape(mapping(Polygon(polygon_geom.exterior))), self.h3_resolution))

            h3_set_exterior = self.__h3_set_line_geom(polygon_geom.exterior, "overlap")

            h3_set_interior_iter = map(lambda x : self.__h3_set_line_geom(x, "overlap"), polygon_geom.interiors)
            h3_set_interior = functools.reduce(lambda x1,x2 : x1 | x2, h3_set_interior_iter, set())

            if h3_contain == "center":
                h3_set_exterior_interior = h3_set_exterior | h3_set_interior
                h3_exterior_interior_iter = map(lambda x : (x, h3.cell_to_latlng(x)), h3_set_exterior_interior)
                h3_exterior_interior_iter = map(lambda x : (x[0], Point(x[1][1], x[1][0])), h3_exterior_interior_iter)
                h3_iter = filter(lambda x : polygon_geom.contains(x[1]), h3_exterior_interior_iter)
                h3_exterior_interior_iter = map(lambda x : x[0], h3_exterior_interior_iter)
                h3_exterior_interior_set = set(h3_iter)

                h3_set = h3_set_fill | h3_exterior_interior_set

            else:
                # default : h3_contain == "overlap"
                h3_set = h3_set_fill | h3_set_exterior | h3_set_interior

            return h3_set

    def __h3_set_geom(self, geom, h3_contain):
        if geom.geom_type == "Point":
            return self.__h3_set_point_geom(geom)

        elif geom.geom_type == "LineString" \
             or geom.geom_type == "LinearRing":
            return self.__h3_set_line_geom(geom, h3_contain)

        elif geom.geom_type == "Polygon":
            return self.__h3_set_polygon_geom(geom, h3_contain)

        elif geom.geom_type == "MultiPoint" \
             or geom.geom_type == "MultiLineString" \
             or geom.geom_type == "MultiPolygon" \
             or geom.geom_type == "GeometryCollection":
            return self.__h3_set_geoms(geom.geoms, h3_contain)

        else:
            return set()

    def __h3_set_geoms(self, geoms, h3_contain):
        h3_set_iter = map(lambda x : self.__h3_set_geom(x, h3_contain), geoms)
        h3_set = functools.reduce(lambda x1,x2 : x1 | x2, h3_set_iter, set())

        return h3_set

    def fill_h3(self, h3_contain="overlap"):
        h3_set_iter = map(lambda x : self.__h3_set_geom(x, h3_contain), self.geoms)
        h3_set = functools.reduce(lambda x1,x2 : x1 | x2, h3_set_iter, set())
        self.h3_list = list(h3_set)

        return self.h3_list

    def build_h3_strtree(self):
        if len(self.h3_list) == 0:
            return None

        h3_boundary_iter = map(lambda x : h3.cell_to_boundary(x), self.h3_list)
        h3_boundary_iter = map(lambda x : Polygon(map(lambda y : (y[1], y[0]), x)), h3_boundary_iter)
        h3_boundary_list = list(h3_boundary_iter)
        self.h3_strtree = STRtree(h3_boundary_list)

        return self.h3_strtree

    def h3_strtree_nearest_shapely(self, shapely_geom):
        try:
            if self.h3_strtree is None:
                return None

            nearest_idx = self.h3_strtree.nearest(shapely_geom)
            nearest_h3 = self.h3_list[nearest_idx]

            return nearest_h3

        except ValueError as e:
            raise ValueError(f"Failed to h3 strtree nearest shapely: {e}")

    def h3_strtree_nearest_location(self, lat, lon):
        try:
            geom = Point(lon, lat)

            return self.h3_strtree_nearest_shapely(geom)

        except ValueError as e:
            raise ValueError(f"Failed to h3 strtree nearest location: {e}")

    def h3_strtree_query_shapely(self, shapely_geom, predicate=None, distance=None):
        try:
            if self.h3_strtree is None:
                return None

            idx_list = self.h3_strtree.query(shapely_geom, predicate=predicate, distance=distance).tolist()
            h3_list = list(map(lambda x : self.h3_list[x], idx_list))

            return h3_list

        except ValueError as e:
            raise ValueError(f"Failed to h3 strtree query shapely: {e}")

    def h3_strtree_query_location(self, lat, lon, predicate=None, distance=None):
        try:
            geom = Point(lon, lat)

            return self.h3_strtree_query_shapely(geom, predicate=predicate, distance=distance)

        except ValueError as e:
            raise ValueError(f"Failed to h3 strtree query location: {e}")

    def h3_strtree_query_nearest_shapely(self, shapely_geom, max_distance=None, return_distance=False, exclusive=False, all_matches=True):
        try:
            if self.h3_strtree is None:
                return None

            is_single_geom = isinstance(shapely_geom, BaseGeometry)

            if return_distance:
                idxs, distances = self.h3_strtree.query_nearest(shapely_geom, max_distance=max_distance, return_distance=return_distance, exclusive=exclusive, all_matches=all_matches)

                if is_single_geom:
                    return (self.h3_list[idxs[0]], distances[0])

                else:
                    h3_iter = map(lambda x : self.h3_list[x], idxs)
                    h3_distance_list = list(zip(h3_iter, distances))

                    return h3_distance_list

            else:
                idxs = self.h3_strtree.query_nearest(shapely_geom, max_distance=max_distance, return_distance=return_distance, exclusive=exclusive, all_matches=all_matches)

                return self.h3_list[idxs[0]] if is_single_geom else list(map(lambda x : self.h3_list[x], idxs))

        except ValueError as e:
            raise ValueError(f"Failed to h3 strtree query nearest shapely: {e}")

    def h3_strtree_query_nearest_location(self, lat, lon, max_distance=None, return_distance=False, exclusive=False, all_matches=True):
        try:
            geom = Point(lon, lat)

            return self.h3_strtree_query_nearest_shapely(geom, max_distance=max_distance, return_distance=return_distance, exclusive=exclusive, all_matches=all_matches)

        except ValueError as e:
            raise ValueError(f"Failed to h3 strtree query nearest location: {e}")
