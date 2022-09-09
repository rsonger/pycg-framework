import OpenGL.GL as GL
# if this import fails on Mac OS, try the fix posted here:
# https://github.com/PixarAnimationStudios/USD/issues/1372

# static methods to load and compile OpenGL shaders and link to create programs
class OpenGLUtils:

    @staticmethod
    def initialize_shader(shader_code, shader_type):
        """Loads and compiles shader code.
        
        If the compilation fails, an exception will be raised after 
        clearing the shader object from memory."""

        # specify required OpenGL_GLSL version
        shader_code = f"#version 330\n{shader_code}"

        # create empty shader object and return reference value
        shader_ref = GL.glCreateShader(shader_type)
        # store the source code in the shader
        GL.glShaderSource(shader_ref, shader_code)
        # compile source code previously stored in the shader object
        GL.glCompileShader(shader_ref)

        # queries whether shader compile was successful
        compile_success = GL.glGetShaderiv(shader_ref, GL.GL_COMPILE_STATUS)

        if not compile_success:
            # retrieve error message
            error_message = GL.glGetShaderInfoLog(shader_ref)
            # convert byte string to character string
            error_message = f"\n{error_message.decode('utf-8')}"
            # free memory used to store shader program
            GL.glDeleteShader(shader_ref)
            # raise exception to halt application and print error message
            raise Exception(error_message)
        
        # compilation was successful, so return shader reference value
        return shader_ref

    @staticmethod
    def initialize_program(vertex_shader_code, fragment_shader_code):
        """Creates a GPU program by attaching and linking together compiled shaders.
        
        If the linking fails, an exception will be raised after 
        clearing the program object from memory."""

        vertex_shader_ref = OpenGLUtils.initialize_shader(
            vertex_shader_code, 
            GL.GL_VERTEX_SHADER
        )
        fragment_shader_ref = OpenGLUtils.initialize_shader(
            fragment_shader_code, 
            GL.GL_FRAGMENT_SHADER
        )

        # create empty program object and store its reference
        program_ref = GL.glCreateProgram()

        # attache previously compiled shader programs
        GL.glAttachShader(program_ref, vertex_shader_ref)
        GL.glAttachShader(program_ref, fragment_shader_ref)

        # link vertex shader to fragment shader
        GL.glLinkProgram(program_ref)

        # checks if the program link was successful
        link_success = GL.glGetProgramiv(program_ref, GL.GL_LINK_STATUS)
        if not link_success:
            # retrieve error message
            error_message = GL.glGetProgramInfoLog(program_ref)
            # free memory used to store program
            GL.glDeleteProgram(program_ref)
            # convert byte string to character string
            error_message = f"\n{error_message.decode('utf-8')}"
            # raise exception to halt application and print error message
            raise Exception(error_message)

        # linking was successful, so return program reference value
        return program_ref

    @staticmethod
    def print_system_info():
        """Prints information about the supported version of OpenGL/SLGL on this computer."""

        print(f"  Vendor: {GL.glGetString(GL.GL_VENDOR).decode('utf-8')}")
        print(f"  Renderer: {GL.glGetString(GL.GL_RENDERER).decode('utf-8')}")
        print(f"  OpenGL version supported: {GL.glGetString(GL.GL_VERSION).decode('utf-8')}")
        print(f"  GLSL version supported: {GL.glGetString(GL.GL_SHADING_LANGUAGE_VERSION).decode('utf-8')}")
