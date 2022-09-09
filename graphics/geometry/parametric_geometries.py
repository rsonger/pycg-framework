from math import sin, cos, pi
from numpy import linspace

from core.matrix import Matrix
from geometry import Geometry
from geometry.basic_geometries import PolygonGeometry

class ParametricGeometry(Geometry):
    """A geometric surface rendered with the given function for parameters u and v."""
    def __init__(self, u_start, u_stop, u_resolution,
                       v_start, v_stop, v_resolution, surface_function):
        super().__init__()
        
        # generate a matrix of vertex points for all values of (u,v)
        point_matrix = []
        for u in linspace(u_start, u_stop, u_resolution + 1):
            matrix_row = []
            for v in linspace(v_start, v_stop, v_resolution + 1):
                matrix_row.append(surface_function(u,v))
            point_matrix.append(matrix_row)
        
#### Begin extension from 5.2 ####
        # texture coordinates
        uv_matrix = []
        uv_data = []

        for u_index in range(u_resolution + 1):
            uv_row = []
            for v_index in range(v_resolution + 1):
                u = u_index/u_resolution
                v = v_index/v_resolution
                uv_row.append((u,v))
            uv_matrix.append(uv_row)
######## End extension ########

        # store vertex data
        position_data = []
        color_data = []

        # default vertex color data: red, green, blue, cyan, magenta, yellow
        C1, C2, C3 = [1, 0, 0], [0, 1, 0], [0, 0, 1]
        C4, C5, C6 = [0, 1, 1], [1, 0, 1], [1, 1, 0]

        # store vertices for each rectangular segment as a pair of triangles
        for n in range(u_resolution):
            for m in range(v_resolution):
                P1 = point_matrix[n + 0][m + 0]
                P2 = point_matrix[n + 1][m + 0]
                P3 = point_matrix[n + 1][m + 1]
                P4 = point_matrix[n + 0][m + 1]
                position_data += [P1,P2,P3, P1,P3,P4]
                color_data += [C1,C2,C3, C4,C5,C6]

#### Begin extension from 5.2 ####
                # texture coordinates
                uv_A = uv_matrix[n + 0][m + 0]
                uv_B = uv_matrix[n + 1][m + 0]
                uv_D = uv_matrix[n + 1][m + 1]
                uv_C = uv_matrix[n + 0][m + 1]
                uv_data += [uv_A,uv_B,uv_C, uv_A,uv_C,uv_D]

        self.set_attribute("vertexUV", uv_data, "vec2")
######## End extension ########

        self.set_attribute("vertexPosition", position_data, "vec3")
        self.set_attribute("vertexColor", color_data, "vec3")
        self.count_vertices()


class PlaneGeometry(ParametricGeometry):
    """A 2D plane divided into segments."""
    def __init__(self, width=1, height=1, width_segments=8, height_segments=8):
        
        surface_function = lambda u,v: [u, v, 0]
        
        super().__init__( -width/2, width/2, width_segments, 
                          -height/2, height/2, height_segments, 
                          surface_function)

class EllipsoidGeometry(ParametricGeometry):
    """A sphere stretched by the given factors of width, height, and depth."""
    def __init__(self, width=1, height=1, depth=1, 
                       radial_segments=32, height_segments=16):

        surface_function = lambda u,v: [
            width/2 * sin(u) * cos(v),
            height/2 * sin(v),
            depth/2 * cos(u) * cos(v)
        ]

        super().__init__(0, 2*pi, radial_segments, 
                            -pi/2, pi/2, height_segments, surface_function)

class SphereGeometry(EllipsoidGeometry):
    """A perfect sphere with the given radius."""
    def __init__(self, radius=1, radial_segments=32, height_segments=16):
        super().__init__(2*radius, 2*radius, 2*radius, 
                         radial_segments, height_segments)

class CylindricalGeometry(ParametricGeometry):
    """A cylindrical object with the given top and bottom radiuses."""
    def __init__(self, top_radius=1, bottom_radius=1, height=1,
                       radial_segments=32, height_segments=4, 
                       top_closed=True, bottom_closed=True):
        surface_function = lambda u,v: [
            (v * top_radius + (1-v) * bottom_radius) * sin(u),
            height * (v - 0.5),
            (v * top_radius + (1-v) * bottom_radius) * cos(u)
        ]
        super().__init__(0, 2*pi, radial_segments, 
                         0, 1, height_segments, surface_function)

        # add polygons to the top and bottom if requested
        if top_closed:
            top_geometry = PolygonGeometry(radial_segments, top_radius)
            rotation = Matrix.make_rotation_y(-pi/2) @ Matrix.make_rotation_x(-pi/2)
            transform = Matrix.make_translation(0, height/2, 0) @ rotation
            top_geometry.apply_matrix(transform)
            self.merge(top_geometry)

        if bottom_closed:
            bottom_geometry = PolygonGeometry(radial_segments, bottom_radius)
            rotation = Matrix.make_rotation_y(-pi/2) @ Matrix.make_rotation_x(pi/2)
            transform = Matrix.make_translation(0, -height/2, 0) @ rotation
            bottom_geometry.apply_matrix(transform)
            self.merge(bottom_geometry)

class CylinderGeometry(CylindricalGeometry):
    "A cylindrical object with the same radius at the top and bottom."
    def __init__(self, radius=1, height=1, radial_segments=32,
                       height_segments=4, top_closed=True, bottom_closed=True):
        
        super().__init__(radius, radius, height, 
                         radial_segments, height_segments, 
                         top_closed, bottom_closed)

class ConeGeometry(CylindricalGeometry):
    """A cylindrical object that comes to a point at the top."""
    def __init__(self, radius=1, height=1, radial_segments=32,
                       height_segments=4, closed=True):
        super().__init__(0, radius, height, radial_segments, 
                         height_segments, False, closed)