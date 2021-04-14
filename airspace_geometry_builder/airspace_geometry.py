from airspace_geometry_builder.aviation_gis_tools.distance import *
from airspace_geometry_builder.aviation_gis_tools.coordinate import *
from airspace_geometry_builder.aviation_gis_tools.ellipsoid_calc import *


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
