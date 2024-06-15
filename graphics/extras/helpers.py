from graphics.core.scene_graph import Mesh, Group
from graphics.geometries import Geometry
from graphics.geometries.basic_geometries import BoxGeometry
from graphics.materials.basic_materials import SurfaceMaterial, LineMaterial

def get_axes_helper(length=1, thickness=0.1, colors=((1,0,0), (0,1,0), (0,0,1))):
    """Creates a mesh showing the 3 coordinate axes in different colors."""
    mesh = Group() # parent node for the three axes

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

    mesh.add(x_mesh)
    mesh.add(y_mesh)
    mesh.add(z_mesh)

    return mesh


def get_grid_helper(size=10, divisions=10, minor_color=(0,0,0), major_color=(0.5,0.5,0.5)):
    """Handles the geometry, material, and mesh for a 2D grid initially on the XY plane."""
    position_data = []
    color_data = []

    delta_tick = size/divisions
    ticks = [-size/2 + n*delta_tick for n in range(divisions + 1)]

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

    return Mesh(geometry, material)
