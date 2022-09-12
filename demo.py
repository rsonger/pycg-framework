from math import pi
import pygame

from graphics.core.app import WindowApp
from graphics.core.renderer import Renderer
from graphics.core.scene_graph import Scene, Camera, Mesh
from graphics.core.texture import Texture

from graphics.geometry.basic_geometries import RectangleGeometry, BoxGeometry
from graphics.geometry.parametric_geometries import SphereGeometry
from graphics.material.texture_material import TextureMaterial
from graphics.extras.camera_rig import CameraRig

class Demo(WindowApp):
    """Demos the PyCG with texture mapping and interactive camera."""
    def startup(self):
        print("Starting up PyCG Demo...")

        aspect = self.screen.get_width() / self.screen.get_height()

        # initialize renderer, scene, and camera
        self.renderer = Renderer()
        self.scene = Scene()
        self.camera = Camera(aspect_ratio=aspect)
        self.rig = CameraRig(self.camera, False)
        self.scene.add(self.rig)
        self.rig.position = (0,1,4)

        # create meshes with texture mapping
        grass_geometry = RectangleGeometry(width=100, height=100)
        grass_material = TextureMaterial(
            texture=Texture(filename="textures/grass.jpg"),
            properties={"repeatUV": [50, 50]}
        )
        grass = Mesh(grass_geometry, grass_material)
        grass.rotate_x(-pi/2)
        self.scene.add(grass)
        sky_geometry = SphereGeometry(radius=50, radial_segments=1024)
        sky_material = TextureMaterial(texture=Texture(filename="textures/sky.jpg"))
        sky = Mesh(sky_geometry, sky_material)
        self.scene.add(sky)
        crate_geometry = BoxGeometry()
        crate_material = TextureMaterial(
            texture=Texture(filename="textures/crate.jpg"),
        )
        crate = Mesh(crate_geometry, crate_material)
        crate.translate(0, 0.5, 0)
        crate.rotate_y(45)
        self.scene.add(crate)

    def update(self):
        # handle inputs and animations
        self.rig.update(self.input, self.delta_time)

        # render the scene
        self.renderer.render(self.scene, self.camera)

# initialize and run this test
Demo(screen_size=(800,600)).run()