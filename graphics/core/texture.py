import pygame
import OpenGL.GL as GL

class Texture:

    def __init__(self, filename=None, properties={}):

        # pygame object for storying pixel data
        self.surface = None

        # texture reference from the GPU
        self.texture_ref = GL.glGenTextures(1)

        self.properties = {
            "magFilter": GL.GL_LINEAR,
            "minFilter": GL.GL_LINEAR_MIPMAP_LINEAR,
            "wrap": GL.GL_REPEAT
        }

        self.set_properties(properties)

        if filename is not None:
            self.load_image(filename)
            self.upload_data()

    def load_image(self, filename):
        self.surface = pygame.image.load(filename)

    def set_properties(self, properties):
        for name, data in properties.items():
            if name in self.properties.keys():
                self.properties[name] = data
            else:
                raise ValueError(f"Texture has no property with name {name}.")
    
    def upload_data(self):

        width = self.surface.get_width()
        height = self.surface.get_height()

        pixel_data = pygame.image.tostring(self.surface, "RGBA", 1)

        GL.glBindTexture(GL.GL_TEXTURE_2D, self.texture_ref)

        GL.glTexImage2D(GL.GL_TEXTURE_2D, 0, GL.GL_RGBA, width, height, 0, 
                        GL.GL_RGBA, GL.GL_UNSIGNED_BYTE, pixel_data)

        GL.glGenerateMipmap(GL.GL_TEXTURE_2D)

        GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MAG_FILTER,
                           self.properties["magFilter"])
        GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MIN_FILTER,
                           self.properties["minFilter"])
        GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_WRAP_S,
                           self.properties["wrap"])
        GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_WRAP_T,
                           self.properties["wrap"])

        GL.glTexParameterfv(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_BORDER_COLOR, 
                            [1,1,1,1])
            