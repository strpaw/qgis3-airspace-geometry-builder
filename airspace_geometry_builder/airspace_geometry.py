from airspace_geometry_builder.aviation_gis_tools.distance import *
from airspace_geometry_builder.aviation_gis_tools.coordinate import *
from airspace_geometry_builder.aviation_gis_tools.ellipsoid_calc import *
import math


class AirspaceGeometry:
    
    def __init__(self): pass

    @staticmethod
    def get_circle_vertices(center_lon_dd, center_lat_dd, radius_m):
        vertices = []
        for i in range(0, 360):
            vertex_lon, vertex_lat = vincenty_direct_solution(center_lon_dd,
                                                              center_lat_dd,
                                                              i, radius_m)
            vertices.append("{} {}".format(vertex_lon, vertex_lat))

        vertices.append(vertices[0])  # Ensure first and last vertices are the same
        return vertices

    @staticmethod
    def get_geometry_as_wkt(vertices):
        """
        :param vertices: list
        :return: str
        """
        vertices_str = ",".join(vertices)
        return "POLYGON(({}))".format(vertices_str)

    @staticmethod
    def circle_as_wkt(center_lon, center_lat, radius):
        """
        :param center_lon: Coordinate
        :param center_lat: Coordinate
        :param radius: Distance
        :return: str
        """
        radius_m = radius.convert_distance_to_uom(UOM_M)
        vertices = AirspaceGeometry.get_circle_vertices(center_lon.ang_dd,
                                                        center_lat.ang_dd,
                                                        radius_m)
        return AirspaceGeometry.get_geometry_as_wkt(vertices)

    @staticmethod
    def get_central_angle(tbrng_from, tbrng_to):
        """ Calculate central angle between bearings from and to
        :param: tbrng_from: float
        :param: tbrng_to: float
        :return: central_angle: float
        """
        central_angle = math.ceil(tbrng_to) - math.floor(tbrng_from)
        if central_angle < 0:
            central_angle += 360
        return central_angle

    @staticmethod
    def get_arc_vertices(center_lon_dd, center_lat_dd, radius_m, tbrng_from, tbrng_to):
        """ Get vertices of arc
        :param: center_lon_dd: float
        :param: center_lon_dd: float
        :param: radius_m: float
        :param: tbrng_from: float
        :param: tbrng_to: float
        :return: vertices: list
        """
        vertices = []
        central_angle = AirspaceGeometry.get_central_angle(tbrng_from, tbrng_to)

        begin_lon, begin_lat = vincenty_direct_solution(center_lon_dd,
                                                        center_lat_dd,
                                                        tbrng_from, radius_m)
        vertices.append("{} {}".format(begin_lon, begin_lat))

        brng = math.floor(tbrng_from)
        for i in range(1, central_angle):
            brng += 1
            if brng > 360:
                brng -= 360
            vertex_lon, vertex_lat = vincenty_direct_solution(center_lon_dd,
                                                              center_lat_dd,
                                                              brng, radius_m)
            vertices.append("{} {}".format(vertex_lon, vertex_lat))

        end_lon, end_lat = vincenty_direct_solution(center_lon_dd,
                                                    center_lat_dd,
                                                    tbrng_to, radius_m)
        vertices.append("{} {}".format(end_lon, end_lat))

        return vertices

    @staticmethod
    def circle_sector_as_wkt(center_lon, center_lat, radius, tbrng_from, tbrng_to):
        """
        :param center_lon: Coordinate
        :param center_lat: Coordinate
        :param radius: Distance
        :param tbrng_from: float
        :param tbrng_to: float
        :return: str
        """
        radius_m = radius.convert_distance_to_uom(UOM_M)
        circle_center = "{} {}".format(center_lon.ang_dd, center_lat.ang_dd)
        vertices = [circle_center]
        vertices.extend(AirspaceGeometry.get_arc_vertices(center_lon.ang_dd, center_lat.ang_dd, radius_m, tbrng_from, tbrng_to))
        vertices.append(circle_center)
        return AirspaceGeometry.get_geometry_as_wkt(vertices)

    @staticmethod
    def circle_ring_as_wkt(center_lon, center_lat, inner_radius, outer_radius):
        """
        :param center_lon: Coordinate
        :param center_lat: Coordinate
        :param inner_radius: float
        :param outer_radius: float
        :return: str
        """
        outer_radius_m = outer_radius.convert_distance_to_uom(UOM_M)
        inner_radius_m = inner_radius.convert_distance_to_uom(UOM_M)

        outer_vertices = AirspaceGeometry.get_circle_vertices(center_lon.ang_dd,
                                                              center_lat.ang_dd,
                                                              outer_radius_m)
        inner_vertices = AirspaceGeometry.get_circle_vertices(center_lon.ang_dd,
                                                              center_lat.ang_dd,
                                                              inner_radius_m)

        outer_vertices_str = ','.join(outer_vertices)
        inner_vertices_str = ','.join(inner_vertices)
        wkt_str = "POLYGON(({}),({}))".format(outer_vertices_str, inner_vertices_str)
        return wkt_str
