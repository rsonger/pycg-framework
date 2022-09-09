# From chapter 3.3
from math import sin, cos, tan, pi
import numpy

class Matrix:
    """Provides four-dimensional matrices for geometric transformations."""

    # the 4D identity matrix
    __identity = numpy.array((
        (1, 0, 0, 0),
        (0, 1, 0, 0),
        (0, 0, 1, 0),
        (0, 0, 0, 1)
    )).astype(float)

    @classmethod
    def get_identity(cls):
        """Create a copy of the 4D identity matrix"""
        return cls.__identity.copy()

    @staticmethod
    def make_translation(x, y, z):
        """Return a 4D matrix for the translation vector <x,y,z>."""
        return numpy.array((
            (1, 0, 0, x),
            (0, 1, 0, y),
            (0, 0, 1, z),
            (0, 0, 0, 1)
        )).astype(float)

    @staticmethod
    def make_rotation_x(angle):
        """Return a 4D matrix for rotating around the x-axis by the given angle in radians."""
        c = cos(angle)
        s = sin(angle)
        return numpy.array((
            (1, 0,  0, 0),
            (0, c, -s, 0),
            (0, s,  c, 0),
            (0, 0,  0, 1)
        )).astype(float)

    @staticmethod
    def make_rotation_y(angle):
        """Return a 4D matrix for rotating around the y-axis by the given angle in radians."""
        c = cos(angle)
        s = sin(angle)
        return numpy.array((
            ( c, 0, s, 0),
            ( 0, 1, 0, 0),
            (-s, 0, c, 0),
            ( 0, 0, 0, 1)
        )).astype(float)

    @staticmethod
    def make_rotation_z(angle):
        """Return a 4D matrix for rotating around the z-axis by the given angle in radians."""
        c = cos(angle)
        s = sin(angle)
        return numpy.array((
            (c, -s, 0, 0),
            (s,  c, 0, 0),
            (0,  0, 1, 0),
            (0,  0, 0, 1)
        )).astype(float)

    @staticmethod
    def make_scale(r, s, t):
        """Return a 4D matrix for scaling by the given magnitudes."""
        return numpy.array((
            (r, 0, 0, 0),
            (0, s, 0, 0),
            (0, 0, t, 0),
            (0, 0, 0, 1)
        )).astype(float)

    @staticmethod
    def make_perspective(angle_of_view=60, aspect_ratio=1, near=0.1, far=1000):
        """Return a 4D matrix for a projection with the given perspective."""
        a = angle_of_view * pi / 180.0
        d = 1.0 / tan(a/2)
        r = aspect_ratio
        b = (near + far) / (near - far)
        c = 2 * near * far / (near - far)
        return numpy.array((
            (d/r, 0,  0, 0),
            (0,   d,  0, 0),
            (0,   0,  b, c),
            (0,   0, -1, 0)
        )).astype(float)