from numpy.linalg import inv
import OpenGL.GL as GL

from core.matrix import Matrix
from geometry import Geometry
from material import Material

class Object3D:
    """The Object3D class represents a node in the scene graph tree structure. 
    
    It stores a list of references to child objects and a parent object with 
    add and remove functions to update parent and child references when needed.
    In addition, each object stores transform data as a core.Matrix object and 
    can calculate its world transformation with the getWorldMatrix() method.

    Attributes:
        parent (Object3D): The parent object of this object in the scene graph.
    """
    def __init__(self):
        self._transform = Matrix.get_identity()
        self._parent = None
        self._children = []

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, node):
        """Sets or removes the parent of this node.

        Args:
            node (Object3D): The node to be the parent of this node, or None

        Raises:
            Exception: The provided node is not an instance of Object3D
            Exception: This node already has a parent and the provided node is not None
        """
        if not isinstance(node, Object3D):
            raise Exception("Parent node must be an instance of Object3D.")
        if self._parent is not None and node is not None:
            raise Exception("Cannot add a child of another node.")
        self._parent = node

    @property
    def world_matrix(self):
        """Calculate the transformation of this object relative to the root of the scene graph (a.k.a., the world).

        Returns:
            NDArray: A matrix representing this object's world transformation.
        """
        if self._parent is None:
            return self._transform
        else:
            # recursion!
            return self._parent.world_matrix @ self._transform

    @property
    def descendant_list(self):
        """Get a single list containing all descendants of this Object3D (a.k.a., node).

        Returns:
            List: All descendants of this node including itself.
        """
        descendants = [self]
        for c in self._children:
            # more recursion!
            descendants += c.descendant_list
        return descendants

    @property
    def position(self):
        """Get coordinates representing the local position of this object (relative to its parent).

        Returns:
            list: The object's coordinates as [x,y,z].
        """
        return [self._transform.item((0,3)), # numpy.ndarray.item 
                self._transform.item((1,3)), # returns the scalar value at the given index
                self._transform.item((2,3))]

    @position.setter
    def position(self, coords):
        """Change this object's position in local space (meaning relative to its parent).

        Args:
            position (list): This object's new position as [x,y,z] coordinates.
        """
        if not type(coords) in (list,tuple) or len(coords) != 3:
            raise Exception("Object3D position must be in the form (x,y,z).")

        self._transform.itemset((0,3), coords[0]) # numpy.ndarray.itemset
        self._transform.itemset((1,3), coords[1]) # inserts the scalar value into the array at the given index     
        self._transform.itemset((2,3), coords[2])

    @property
    def world_position(self):
        """Get coordinates representing the position of this object with respect to the root of the scene graph (a.k.a., the world).

        Returns:
            list: This object's coordinates as [x,y,z].
        """
        world_transform = self.world_matrix
        return [world_transform.item((0,3)),
                world_transform.item((1,3)),
                world_transform.item((2,3))]

    def add(self, child):
        """Adds an object as the child to this object in the scene graph.

        Args:
            child (Object3D): The child node to add to this object.

        Raises:
            Exception: The object to add is already a child of another object.
        """
        child.parent = self
        self._children.append(child)

    def remove(self, child):
        """Remove a child object from this object.

        Args:
            child (Object3D): The object to remove from this object's list of children.
        """
        self._children.remove(child)
        child.parent = None

    def apply_matrix(self, matrix, local_coords=True):
        """Apply a geometric transformation to this object.

        Args:
            matrix (NDArray): The transformation matrix to apply.
            localCoord (bool, optional): Whether the transformation is local or not. Defaults to True.
        """
        if local_coords:
            self._transform = self._transform @ matrix
        else:
            self._transform = matrix @ self._transform

    def translate(self, x, y, z, local_coords=True):
        """Calculate and apply a translation to this object.

        Args:
            x (float): The number of units to translate along the x-axis.
            y (float): The number of units to translate along the y-axis.
            z (float): The number of units to translate along the z-axis.
            localCoord (bool, optional): Whether the transformation is local or not. Defaults to True.
        """
        m = Matrix.make_translation(x,y,z)
        self.apply_matrix(m, local_coords)
    
    def rotate_x(self, angle, local_coords=True):
        """Calculate and apply a rotation around the x-axis of this object.

        Args:
            angle (float): The number of radians to rotate around the x-axis.
            localCoord (bool, optional): Whether the tranformation is local or not. Defaults to True.
        """
        m = Matrix.make_rotation_x(angle)
        self.apply_matrix(m, local_coords)
    
    def rotate_y(self, angle, local_coords=True):
        """Calculate and apply a rotation around the y-axis of this object.

        Args:
            angle (float): The number of radians to rotate around the y-axis.
            localCoord (bool, optional): Whether the tranformation is local or not. Defaults to True.
        """
        m = Matrix.make_rotation_y(angle)
        self.apply_matrix(m, local_coords)
    
    def rotate_z(self, angle, local_coords=True):
        """Calculate and apply a rotation around the z-axis of this object.

        Args:
            angle (float): The number of radians to rotate around the z-axis.
            localCoord (bool, optional): Whether the tranformation is local or not. Defaults to True.
        """
        m = Matrix.make_rotation_z(angle)
        self.apply_matrix(m, local_coords)
    
    def scale_uniform(self, s, local_coords=True):
        """Calculate and apply a scaling tranformation to this object.

        Args:
            s (float): The magnitude by which to scale.
            localCoord (bool, optional): Whether the transformation is local or not. Defaults to True.
        """
        m = Matrix.make_scale(s, s, s)
        self.apply_matrix(m, local_coords)


class Scene(Object3D):
    """Represents the root node of the scene graph tree structure.
    
    This class is entirely semantic and provides no additional functionality.
    """
    def __init__(self):
        super().__init__()

    @Object3D.parent.setter
    def parent(self, node):
        if node is not None:
            raise Exception("The root node cannot have a parent.")


class Group(Object3D):
    """Represents an interior node of the scene graph.
    
    Many other nodes can be attached to this one in order to more easily transform them.
    This class is entirely semantic and provides no additional functionality.
    """
    def __init__(self) -> None:
        super().__init__()


class Camera(Object3D):
    """Represents the virtual camera used to view the scene.
    
    As with any 3D object, the camera has a position and orientation which is stored in its transform matrix.
    Since camera transformations make world objects appear to transform in the opposite direction,
    this class also stores a view matrix as the inverse of the camera's transform matrix.
    The camera defines the position and orientation of the viewer, so it also stores the projection matrix.

    Attributes:
        projection_matrix (NDArray): The projection matrix for the scene.
        view_matrix (NDArray): The transformation matrix for the camera.
    """
    def __init__(self, angle_of_view=60, aspect_ratio=1, near=0.1, far=1000):
        super().__init__()
        self._projection_matrix = Matrix.make_perspective(
            angle_of_view, aspect_ratio, near, far
        )
        self._view_matrix = Matrix.get_identity()

    @property
    def projection_matrix(self):
        return self._projection_matrix

    @property
    def view_matrix(self):
        return self._view_matrix

    def update_view_matrix(self):
        self._view_matrix = inv(self.world_matrix)


class Mesh(Object3D):
    """Represents a visible object in the scene.

    Mesh contains data geometric data related to the object vertices and material data about its appearance.
    It also creates and stores a vertex array object (VAO) reference, and associates variables between
    vertex buffers and shader varriables.

    Attributes:
        geometry (geometry.Geometry): Data representing this object's geometric attributes and vertices.
        material (material.Material): Data representing the general appearance of this object.
    """
    def __init__(self, geometry, material):
        super().__init__()

        if not isinstance(geometry, Geometry):
            raise Exception(f"Expecting an instance of Geometry but got {type(geometry)} instead.")
        self._geometry = geometry
        
        if not isinstance(material, Material):
            raise Exception(f"Expecting an instance of Material but got {type(material)} instead.")
        self._material = material

        self._visible = True

        # Set up associations between attributes in the geometry 
        # and the shader program in material.
        self._vao_ref = GL.glGenVertexArrays(1)
        GL.glBindVertexArray(self._vao_ref)

        for variable, attribute in geometry.attributes.items():
            attribute.associate_variable(material.program_ref, variable)

        # unbind this vertex array object
        GL.glBindVertexArray(0)

    @property
    def visible(self):
        return self._visible
    
    @visible.setter
    def visible(self, value):
        self._visible = bool(value)

    def render(self, view_matrix, projection_matrix):
        GL.glUseProgram(self._material.program_ref)
            
        GL.glBindVertexArray(self._vao_ref)

        # update matrix uniforms
        self._material.set_uniform("modelMatrix", self.world_matrix)
        self._material.set_uniform("viewMatrix", view_matrix)
        self._material.set_uniform("projectionMatrix", projection_matrix)

        # update the stored data and settings before drawing
        self._material.upload_data()
        self._material.update_render_settings()
        GL.glDrawArrays(self._material.get_setting("drawStyle"), 0, 
                     self._geometry.vertex_count)

        GL.glBindVertexArray(0)