import OpenGL.GL as GL

from graphics.core.scene_graph import Mesh, Camera, Scene

class Renderer:
    """Manages the rendering of a given scene with basic OpenGL settings."""
    def __init__(self, clear_color=(0,0,0)):
        """Initialize basic settings for depth testing, antialiasing and clear color."

        Args:
            clearColor (tuple, optional): The background color for clearing the screen. Defaults to (0,0,0).
        """
        GL.glEnable(GL.GL_DEPTH_TEST)
        GL.glEnable(GL.GL_MULTISAMPLE)
        GL.glClearColor(*clear_color, 1)

        GL.glEnable(GL.GL_BLEND)
        GL.glBlendFunc(GL.GL_SRC_ALPHA, GL.GL_ONE_MINUS_SRC_ALPHA)

    def render(self, scene, camera):
        """Render the given scene as viewed through the given camera.

        Args:
            scene (core.scene.Scene): The scene to render.
            camera (core.camera.Camera): The camera used to view the scene.
        """
        if not isinstance(scene, Scene):
            raise Exception("The given scene must be an instance of Scene.")
        if not isinstance(camera, Camera):
            raise Exception("The given camera must be an instance of Camera.")

        # clear buffers
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)

        # update camera view
        camera.update_view_matrix()

        # draw all the viewable meshes
        for mesh in scene.descendant_list:
            if isinstance(mesh, Mesh) and mesh.visible:
                mesh.render(camera.view_matrix, camera.projection_matrix)