import OpenGL.GL as GL

from material import Material

class TextureMaterial(Material):

    def __init__(self, texture, properties={}):

        vs_code = """
        uniform mat4 projectionMatrix;
        uniform mat4 viewMatrix;
        uniform mat4 modelMatrix;

        in vec3 vertexPosition;
        in vec2 vertexUV;
        
        uniform vec2 repeatUV;
        uniform vec2 offsetUV;
        
        out vec2 UV;

        void main() {
            gl_Position = projectionMatrix * viewMatrix * modelMatrix * vec4(vertexPosition, 1.0);
            UV = vertexUV * repeatUV + offsetUV;
        }
        """

        fs_code = """
        uniform vec3 baseColor;
        uniform sampler2D texture;

        in vec2 UV;

        out vec4 fragColor;

        void main() {
            vec4 color = vec4(baseColor, 1.0) * texture2D(texture, UV);
            if (color.a < 0.10)
                discard;

            fragColor = color;
        }
        """

        super().__init__(vs_code, fs_code)

        self.set_uniform("baseColor", (1.0, 1.0, 1.0), "vec3")
        self.set_uniform("texture", (texture.texture_ref, 1), "sampler2D")
        self.set_uniform("repeatUV", (1.0, 1.0), "vec2")
        self.set_uniform("offsetUV", (0.0, 0.0), "vec2")

        self._settings["doubleSide"] = True
        self._settings["wireframe"] = False

        self.set_properties(properties)

    def update_render_settings(self):
        
        if self._settings["doubleSide"]:
            GL.glDisable(GL.GL_CULL_FACE)
        else:
            GL.glEnable(GL.GL_CULL_FACE)

        if self._settings["wireframe"]:
            GL.glPolygonMode(GL.GL_FRONT_AND_BACK, GL.GL_LINE)
        else:
            GL.glPolygonMode(GL.GL_FRONT_AND_BACK, GL.GL_FILL)

        