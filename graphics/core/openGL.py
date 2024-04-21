from typing import Iterable

import OpenGL.GL as GL
import numpy

class Attribute:
    """Manages attribute data to be stored in a single vertex buffer.
    """

    # maps data types to their associated vertex size and component data type
    _ATTRIB_SIZE_TYPE = {
        'int':      (1, GL.GL_INT),
        'float':    (1, GL.GL_FLOAT),
        'vec2':     (2, GL.GL_FLOAT),
        'vec3':     (3, GL.GL_FLOAT),
        'vec4':     (4, GL.GL_FLOAT),
    }

    def __init__(self, data_type: str, data: Iterable) -> None:
        """Stores the data type, data, and a reference to the buffer before sending the data to the buffer.

        Args:
            data_type: the type of the data being stored (int, float, vec2, vec3, vec4)
            data: the data to send to a vertex buffer
        """
        if data_type not in self._ATTRIB_SIZE_TYPE.keys():
            raise ValueError(data_type, "Unsupported data type")

        self.data_type = data_type
        self.data = data
        self.buffer_ref = GL.glGenBuffers(1)

        # send the data to the GPU buffer
        self.upload_data()

    def upload_data(self) -> None:
        """Sends this attribute data to a GPU buffer.
        """

        # convert data to numpy array format
        # using 32-bit floating point numbers
        data = numpy.array(self.data).astype(numpy.float32)

        # select buffer used by the following functions
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self.buffer_ref)

        # store data in currently bound buffer as a 1D array
        GL.glBufferData(GL.GL_ARRAY_BUFFER, data.ravel(), GL.GL_STATIC_DRAW)

    def associate_variable(self, program_ref: int, variable_name: str, vao_ref: int=None) -> None:
        """Associates a variable in the given program with this buffer.
        This association will be stored in the given vertex array object if a reference
        is given. Otherwise, the VAO must be bound before calling this method.


        Args:
            program_ref: An OpenGL reference to a compiled shader program
            variable_name: The name of the variable in the shader program
            vao_ref: An OpenGL reference to a vertex array object. Defaults to None.

        Raises:
            Exception: The data_type of this attribute variable is unknown.
        """

        # get reference for program variable with given name
        variable_ref = GL.glGetAttribLocation(program_ref, variable_name)

        # stop if the program does not reference the variable
        if variable_ref == -1:
            return

        # select buffer used by the following functions
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self.buffer_ref)

        # bind the vertex array object if it was given
        if vao_ref is not None:
            GL.glBindVertexArray(vao_ref)

        # get vertex parameters for this attribute's data type
        size, gl_type = self._ATTRIB_SIZE_TYPE[self.data_type]

        # specify how data will be read from the currently bound buffer 
        # into the specified variable. These associations are stored by
        # whichever VAO is bound before calling this method.
        GL.glVertexAttribPointer(variable_ref, size, gl_type, False, 0, None)

        # indicate that data will be streamed to this variable
        GL.glEnableVertexAttribArray(variable_ref)


class Uniform:
    """ Manages data for a single uniform variable in a shader program """

    _VALID_TYPES = ('int','bool','float','vec2','vec3','vec4','mat4','sampler2d')

    def __init__(self, data_type, data):
        # check the given data type
        if data_type.lower() not in self._VALID_TYPES:
            raise ValueError(f"Unsupported data type: {data_type}")
        self.data_type = data_type.lower()

        # data to be sent to uniform variable
        self.data = data

        # reference for variable location in program
        self.variable_ref = None

    def locate_variable(self, program_ref, variable_name):
        """Get and store reference to a program variable with the given name."""

        self.variable_ref = GL.glGetUniformLocation(program_ref, variable_name)
        if self.variable_ref == -1:
          raise ValueError(f"No uniform variable found with name {variable_name}")

    def upload_data(self):
        """Store data in a previously located uniform variable."""
        # check that the variable reference exists
        assert self.variable_ref is not None, "Must locate uniform variable before uploading data."

        if self.data_type == "int":
            GL.glUniform1i(self.variable_ref, self.data)
        elif self.data_type == "bool":
            GL.glUniform1i(self.variable_ref, self.data)
        elif self.data_type == "float":
            GL.glUniform1f(self.variable_ref, self.data)
        elif self.data_type == "vec2":
            GL.glUniform2f(self.variable_ref, *self.data)
        elif self.data_type == "vec3":
            GL.glUniform3f(self.variable_ref, *self.data)
        elif self.data_type == "vec4":
            GL.glUniform4f(self.variable_ref, *self.data)
        elif self.data_type == "mat4":
            GL.glUniformMatrix4fv(self.variable_ref, 1, GL.GL_TRUE, self.data)
        elif self.data_type == "sampler2d":
            texture_obj_ref, texture_unit_ref = self.data
            GL.glActiveTexture(GL.GL_TEXTURE0 + texture_unit_ref)
            GL.glBindTexture(GL.GL_TEXTURE_2D, texture_obj_ref)
            GL.glUniform1i(self.variable_ref, texture_unit_ref)
