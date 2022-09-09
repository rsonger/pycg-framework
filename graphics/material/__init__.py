"""A collection of various subclasses of the Material class.

Modules exported by this package:

- `basic_materials`
- `texture_material`
"""

from OpenGL.GL import GL_TRIANGLES

from core.openGL import Uniform
from core.openGLUtils import OpenGLUtils

class Material:
    """The Material class stores shader program references, Uniform objects, and OpenGL render settings.

    The base class initializes the shader program from vertex shader code and fragment shader code;
    links uniform variables to their associated data; and maintains OpenGL render settings and their values.
    """
    def __init__(self, vertex_shader_code, fragment_shader_code):
        self._program_ref = OpenGLUtils.initialize_program(
            vertex_shader_code, 
            fragment_shader_code
        )

        # store uniform objects assigned to names of their associated shader variables
        self._uniforms = {}

        # initialize common shader uniforms to be set during the render process
        self.set_uniform("modelMatrix", None, "mat4")
        self.set_uniform("viewMatrix", None, "mat4")
        self.set_uniform("projectionMatrix", None, "mat4")

        # OpenGL render settings assigned to variable names
        self._settings = {"drawStyle": GL_TRIANGLES}

    @property
    def program_ref(self):
        return self._program_ref

    def get_setting(self, setting_name):
        """Return a setting value if the setting exists; otherwise, return None."""
        return self._settings.get(setting_name, None)

    def set_uniform(self, variable_name, data, data_type=None):
        """Add or update a Uniform object representing a property of this material.

        If the uniform variable is already set, its data will be updated. 
        If a new uniform object is being created, a data type must be provided.

        Args:
            variableName (string): The name of the shader uniform variable
            data (any): The data to be linked by the Uniform object
            dataType (string, optional): The type of data stored in the uniform variable. Defaults to None.

        Raises:
            Exception: _description_
        """
        if variable_name in self._uniforms.keys():
            self._uniforms[variable_name].data = data
        elif data_type is not None:
            self._uniforms[variable_name] = Uniform(data_type, data)
            self._uniforms[variable_name].locate_variable(self._program_ref, 
                                                          variable_name)
        else:
            raise Exception("A new Material property must have a dataType.")
            
    def update_render_settings(self):
        pass

    def set_properties(self, properties):
        """Convenience method for setting multiple uniform variable and render setting values from a dictionary."""
        for name, data in properties.items():
            if name in self._uniforms.keys():
                self._uniforms[name].data = data
            elif name in self._settings:
                self._settings[name] = data
            else:
                raise Exception(f"Material has no property named {name}")
        
    def upload_data(self):
        """Convenience method for uploading the data of all stored uniform variables."""
        for uniform_obj in self._uniforms.values():
            uniform_obj.upload_data()