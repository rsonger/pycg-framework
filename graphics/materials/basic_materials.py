import OpenGL.GL as GL

from graphics.materials import Material

class BasicMaterial(Material):
    """A simple material for rendering objects in a solid color or vertex colors."""
    def __init__(self):
        vertex_shader_code = """
        uniform mat4 projectionMatrix;
        uniform mat4 viewMatrix;
        uniform mat4 modelMatrix;

        in vec3 vertexPosition;
        in vec3 vertexColor;
        
        out vec3 color;

        void main() {
            gl_Position = projectionMatrix * viewMatrix * modelMatrix * vec4(vertexPosition, 1.0);
            color = vertexColor;
        }
        """

        fragment_shader_code = """
        uniform vec3 baseColor;
        uniform bool useVertexColors;
        
        in vec3 color;
        
        out vec4 fragColor;

        void main() {
            vec4 tempColor = vec4(baseColor, 1.0);
            if (useVertexColors) tempColor *= vec4(color, 1.0);
            fragColor = tempColor;
        }
        """

        super().__init__(vertex_shader_code, fragment_shader_code)

        self.set_uniform("baseColor", (1,1,1), "vec3")
        self.set_uniform("useVertexColors", False, "bool")

class PointMaterial(BasicMaterial):
    """Manages render settings for drawing vertices as rounded points.

    drawStyle: GL_POINTS to draw vertices without any connecting lines
    pointSize: 8 pixel width and height by default
    roundedPoints: True to render points with smooth corners
    """

    def __init__(self, properties={}):
        super().__init__()

        # render vertices as points
        self._settings["drawStyle"] = GL.GL_POINTS

        # width and height of points in pixels
        self._settings["pointSize"] = 8
        
        # draw points as rounded
        self._settings["roundedPoints"] = True

        self.set_properties(properties)

    def update_render_settings(self):
        GL.glPointSize(self._settings["pointSize"])

class LineMaterial(BasicMaterial):
    """Manages render settings for drawing lines between vertices.

    drawStyle: GL_LINE_STRIP by default, changes according to lineType
    lineType: "connected" to draw through all vertices from first to last.
    lineType: "loop" to draw through all vertices and connect last to first.
    lineType: "segments" to draw separate lines between each pair of vertices.
    """
    def __init__(self, properties={}):
        super().__init__()

        self._settings["drawStyle"] = GL.GL_LINE_STRIP
        self._settings["lineType"] = "connected"

        self.set_properties(properties)

    def update_render_settings(self):
        
        if self._settings["lineType"] == "connected":
            self._settings["drawStyle"] = GL.GL_LINE_STRIP
        elif self._settings["lineType"] == "loop":
            self._settings["drawStyle"] = GL.GL_LINE_LOOP
        elif self._settings["lineType"] == "segments":
            self._settings["drawStyle"] = GL.GL_LINES
        else:
            raise ValueError("Unknown line type: must be one of [connected | loop | segments].")

class SurfaceMaterial(BasicMaterial):
    """Manages render settings for drawing vertices as a colored surface.

    drawStyle: GL_TRIANGLES to draw triangles between sets of 3 vertices
    doubleSide: False to render only the side where the vertices are in counterclockwise order
    wireframe: False to render triangles instead of lines between the vertices
    """
    def __init__(self, properties={}):
        super().__init__()

        self._settings["drawStyle"] = GL.GL_TRIANGLES
        self._settings["doubleSide"] = False
        self._settings["wireframe"] = False

        # set additional properties if any have been provided
        self.set_properties(properties)

    def update_render_settings(self):
        """Applies OpenGL render settings as specified by this material's settings."""
        if self._settings.get("doubleSide", False):
            GL.glDisable(GL.GL_CULL_FACE)
        else:
            GL.glEnable(GL.GL_CULL_FACE)

        if self._settings.get("wireframe", False):
            GL.glPolygonMode(GL.GL_FRONT_AND_BACK, GL.GL_LINE)
        else:
            GL.glPolygonMode(GL.GL_FRONT_AND_BACK, GL.GL_FILL)