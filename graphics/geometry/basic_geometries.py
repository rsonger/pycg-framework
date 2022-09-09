from math import sin, cos, pi

from geometry import Geometry

class RectangleGeometry(Geometry):
    """This class represents a rectangular geometric object.
    Initially, each rectangle has a position centering it at (0,0,0) and a different color for each vertex.
    Position data is given in a way so that it is drawn as two triangles that share the same hypotenuse.
    The first triangle has coordinates [-w/2,-h/2,0], [w/2,-h/2,0], [w/2, h/2, 0].
    The second triangle has coordinates [-w/2,-h/2,0], [w/2,h/2,0], [-w/2,h/2, 0].

    The width (w) and height (h) default to 1 unless otherwise specified.
    """
    def __init__(self, width=1, height=1):
        super().__init__()

        P0 = (-width/2, -height/2, 0)
        P1 = ( width/2, -height/2, 0)
        P2 = (-width/2,  height/2, 0)
        P3 = ( width/2,  height/2, 0)
        C0, C1, C2, C3 = (1,1,1), (1,0,0), (0,1,0), (0,0,1)

        position_data = (P0, P1, P3, P0, P3, P2)
        color_data = (C0, C1, C3, C0, C3, C2)

        self.set_attribute("vertexPosition", position_data, "vec3")
        self.set_attribute("vertexColor", color_data, "vec3")

        self.count_vertices()

#### Begin extension from 5.2 ####
        # texture coordinates
        T0, T1, T2, T3 = (0,0), (1,0), (0,1), (1,1)
        uv_data = (T0,T1,T3, T0,T3,T2)

        self.set_attribute("vertexUV", uv_data, "vec2")
######## End extension ########


class BoxGeometry(Geometry):

    def __init__(self, width=1, height=1, depth=1):
        super().__init__()

        # position vertices
        P0 = (-width/2, -height/2, -depth/2)
        P1 = ( width/2, -height/2, -depth/2)
        P2 = (-width/2,  height/2, -depth/2)
        P3 = ( width/2,  height/2, -depth/2)
        P4 = (-width/2, -height/2,  depth/2)
        P5 = ( width/2, -height/2,  depth/2)
        P6 = (-width/2,  height/2,  depth/2)
        P7 = ( width/2,  height/2,  depth/2)

        # color vertex data for each side
        C1 = [(1.0, 0.0, 0.0)] * 6  # six red vertices
        C2 = [(1.0, 1.0, 0.0)] * 6  # six yellow vertices
        C3 = [(0.0, 1.0, 0.0)] * 6  # six green vertices
        C4 = [(0.0, 1.0, 1.0)] * 6  # six cyan vertices
        C5 = [(0.0, 0.0, 1.0)] * 6  # six blue vertices
        C6 = [(1.0, 0.0, 1.0)] * 6  # six magenta vertices

        position_data = (P5,P1,P3, P5,P3,P7, # right side
                         P0,P4,P6, P0,P6,P2, # left side
                         P6,P7,P3, P6,P3,P2, # top side
                         P0,P1,P5, P0,P5,P4, # bottom side
                         P4,P5,P7, P4,P7,P6, # front side
                         P1,P0,P2, P1,P2,P3) # back side
        
        # create a list of 36 RGB vertices
        color_data = C1 + C2 + C3 + C4 + C5 + C6 
        
        self.set_attribute("vertexPosition", position_data, "vec3")
        self.set_attribute("vertexColor", color_data, "vec3")
        self.count_vertices()

#### Begin extension from 5.2 ####
        # texture coordinates
        T0, T1, T2, T3 = (0,0), (1,0), (0,1), (1,1)
        uv_data = [T0,T1,T3, T0,T3,T2] * 6

        self.set_attribute("vertexUV", uv_data, "vec2")
######## End extension ########


    def change_position(self, position_data):
        if len(position_data) != 8 or len(position_data[0]) != 3:
            raise Exception("Box geometry position requires 8 points of 3-dimensional vertices")
        self.set_attribute("vertexPosition", position_data)
    
    def change_color(self, color_data):
        if len(color_data) != 8 or len(color_data[0]) != 3:
            raise Exception("Box geometry color requires 8 points of 3-dimensional vertices")
        self.set_attribute("vertexColor", color_data)


class PolygonGeometry(Geometry):
    """Renders a regular polygon with the given number of sides and radius."""
    def __init__(self, sides=3, radius=1):
        super().__init__()

        theta = 2 * pi / sides
        position_data = []
        color_data = []

#### Begin extension from 5.2 ####
        # texture coordinates
        uv_data = []
######## End extension ########

        for n in range(sides):
            position_data += (
                (0, 0, 0),
                (radius*cos(n*theta), radius*sin(n*theta), 0),
                (radius*cos((n+1)*theta), radius*sin((n+1)*theta), 0)
            )            
            color_data += ((1, 1, 1), (1, 0, 0), (0, 0, 1))

#### Begin extension from 5.2 ####
            # texture coordinates
            uv_data += (
                (0.5, 0.5),
                (cos(n*theta)*0.5 + 0.5, sin(n*theta)*0.5 + 0.5),
                (cos((n+1)*theta)*0.5 + 0.5, sin((n+1)*theta)*0.5 + 0.5)
            )

        self.set_attribute("vertexUV", uv_data, "vec2")
######## End extension ########

        self.set_attribute("vertexPosition", position_data, "vec3")
        self.set_attribute("vertexColor", color_data, "vec3")
        self.count_vertices()