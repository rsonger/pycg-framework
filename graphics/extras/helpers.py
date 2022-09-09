from core.scene_graph import Mesh, Group
from geometry import Geometry
from geometry.basic_geometries import BoxGeometry
from material.basic_materials import SurfaceMaterial, LineMaterial

class AxesHelper:
    """Creates a mesh to render the 3 coordinate axes in different colors."""
    def __init__(self, length=1, thickness=0.1, 
                       colors=((1,0,0), (0,1,0), (0,0,1))):
        self.mesh = Group() # parent node for the three axes

        offset = length/2 + thickness/2

        # the x-axis is a is a long, narrow, red box
        x_mesh = Mesh(
            BoxGeometry(length, thickness, thickness), 
            SurfaceMaterial({"baseColor": colors[0]})
        )
        x_mesh.translate(offset, 0, 0)

        # the y-axis is a long, narrow, green box
        y_mesh = Mesh(
            BoxGeometry(thickness, length, thickness), 
            SurfaceMaterial({"baseColor": colors[1]})
        )
        y_mesh.translate(0, offset, 0)

        # the z-axis is a long, narrow, blue box
        z_mesh = Mesh(
            BoxGeometry(thickness, thickness, length), 
            SurfaceMaterial({"baseColor": colors[2]})
        )
        z_mesh.translate(0, 0, offset)

        self.mesh.add(x_mesh)
        self.mesh.add(y_mesh)
        self.mesh.add(z_mesh)


class GridHelper:
    """Handles the geometry, material, and mesh for a 2D grid initially on the XY plane."""
    def __init__(self, size=10, divisions=10, minor_color=(0,0,0), 
                       major_color=(0.5,0.5,0.5)):
        position_data = []
        color_data = []

        ticks = []
        delta_tick = size/divisions
        for n in range(divisions + 1):
            ticks.append(-size/2 + n*delta_tick)

        # vertical lines
        for x in ticks:
            position_data.append((x, -size/2, 0))
            position_data.append((x,  size/2, 0))
        
            if x == 0:
                color_data.append(major_color)
                color_data.append(major_color)
            else:
                color_data.append(minor_color)
                color_data.append(minor_color)

        # horizontal lines
        for y in ticks:
            position_data.append((-size/2, y, 0))
            position_data.append(( size/2, y, 0))

            if y == 0:
                color_data.append(major_color)
                color_data.append(major_color)
            else:
                color_data.append(minor_color)
                color_data.append(minor_color)

        geometry = Geometry()
        geometry.set_attribute("vertexPosition", position_data, "vec3")
        geometry.set_attribute("vertexColor", color_data, "vec3")
        geometry.count_vertices()

        material = LineMaterial({
            "useVertexColors": True,
            "lineType": "segments"
        })

        self.mesh = Mesh(geometry, material)