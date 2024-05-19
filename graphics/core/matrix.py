# From chapter 3.3
from math import sin, cos, tan, pi

import numpy as np
import numpy.typing as npt

class Matrix:
    """ Provides four-dimensional matrices for various geometric transformations """

    # the 4D identity matrix
    __identity = np.array((
        (1, 0, 0, 0),
        (0, 1, 0, 0),
        (0, 0, 1, 0),
        (0, 0, 0, 1)
    )).astype(float)

    @classmethod
    def identity(cls) -> npt.NDArray[np.float64]:
        """ A copy of the 4D identity matrix """
        return cls.__identity.copy()

    @staticmethod
    def translation(x, y, z) -> npt.NDArray[np.float64]:
        """ 4D matrix for the translating along vector <x, y, z> """
        return np.array((
            (1, 0, 0, x),
            (0, 1, 0, y),
            (0, 0, 1, z),
            (0, 0, 0, 1)
        )).astype(float)

    @staticmethod
    def rotation_x(angle) -> npt.NDArray[np.float64]:
        """ 4D matrix for rotating around the x-axis by the given angle in radians """
        c = cos(angle)
        s = sin(angle)
        return np.array((
            (1, 0,  0, 0),
            (0, c, -s, 0),
            (0, s,  c, 0),
            (0, 0,  0, 1)
        )).astype(float)

    @staticmethod
    def rotation_y(angle) -> npt.NDArray[np.float64]:
        """ 4D matrix for rotating around the y-axis by the given angle in radians """
        c = cos(angle)
        s = sin(angle)
        return np.array((
            ( c, 0, s, 0),
            ( 0, 1, 0, 0),
            (-s, 0, c, 0),
            ( 0, 0, 0, 1)
        )).astype(float)

    @staticmethod
    def rotation_z(angle) -> npt.NDArray[np.float64]:
        """ 4D matrix for rotating around the z-axis by the given angle in radians """
        c = cos(angle)
        s = sin(angle)
        return np.array((
            (c, -s, 0, 0),
            (s,  c, 0, 0),
            (0,  0, 1, 0),
            (0,  0, 0, 1)
        )).astype(float)

    @staticmethod
    def scale(r, s, t) -> npt.NDArray[np.float64]:
        """ 4D matrix for scaling dimensions x, y, and z by magnitudes r, s, and t respectively """
        return np.array((
            (r, 0, 0, 0),
            (0, s, 0, 0),
            (0, 0, t, 0),
            (0, 0, 0, 1)
        )).astype(float)

    @staticmethod
    def perspective(
            angle_of_view=60,
            aspect_ratio=1,
            near=0.1,
            far=1000
    ) -> npt.NDArray[np.float64]:
        """ 4D matrix for a projection transformation to the given perspective """
        a = angle_of_view * pi / 180.0
        d = 1.0 / tan(a/2)
        r = aspect_ratio
        b = (near + far) / (near - far)
        c = 2 * near * far / (near - far)
        return np.array((
            (d/r, 0,  0, 0),
            (0,   d,  0, 0),
            (0,   0,  b, c),
            (0,   0, -1, 0)
        )).astype(float)