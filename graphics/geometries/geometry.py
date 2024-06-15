from graphics.core.openGL import Attribute

class Geometry:
    """
    Geometry objects store attribute data and their total number of vertices.
    This base class defines a dictionary for attributes and a count for the number of vertices.

    Attributes:
        attributes (dict): A dictionary of geometric attributes for this object.
        vertexCount (int): The total number of vertices for this object.
    """

    def  __init__(self):
        self._attributes = {}

    @property
    def attributes(self):
        return self._attributes

    @property
    def vertex_count(self):
        return self.count_vertices()

    def set_attribute(self, variable_name, data, data_type=None) -> None:
        """
        Set or add an attribute for this geometric object.

        Args:
            variableName (string): The name of the attribute variable to add or set.
            data (any): The data of type dataType to store in the attribute variable.
            dataType (string): The type of data for the attribute variable to add.
        """
        if variable_name in self._attributes.keys():
            self._attributes[variable_name].data = data
            self._attributes[variable_name].upload_data()
        elif data_type is not None:
            self._attributes[variable_name] = Attribute(data_type, data)
        else:
            raise ValueError("A new Geometry attribute must have a data type.")
    
    def count_vertices(self, variable_name=None) -> int:
        """
        Counts the number of vertices as the length of an attribute's data.
        For example, after adding an attribute of type 'vec3', its data will be a 3D vector and so 
        it will have 3 vertices.

        Args:
            variableName (string, optional): A specific attribute to use when counting vertices
        """
        if len(self._attributes) == 0:
            return 0
        
        if variable_name is not None:
            attrib = self._attributes.get(variable_name)
            if attrib is None:
                raise ValueError(variable_name, "No attribute with this name has been set")
            return len(attrib.data)
        else:
            return len(list(self._attributes.values())[0].data)

    def apply_matrix(self, matrix, variable_name="vertexPosition"):
        """ Transform the data in an attribute using the given matrix """
        if variable_name not in self._attributes.keys():
            raise ValueError(f"Unable to apply matrix to unknown attribute: {variable_name}")

        old_position_data = self._attributes[variable_name].data
        new_position_data = []

        for old_pos in old_position_data:
            # copy the data and add a homogeneous fourth coordinate
            new_pos = old_pos + (1,)

            # apply the matrix
            new_pos = matrix @ new_pos

            # remove the homogeneous coordinate and append to the new data
            new_pos = new_pos[:3]
            new_position_data.append(new_pos)

        self.set_attribute(variable_name, new_position_data)

    def merge(self, other_geometry):
        """
        Merge data from attributes of other geometries into this object.
        Both geometries must share attributes with the same names.
        """
        for variable_name, attribute in self._attributes.items():
            attribute.data += other_geometry.attributes[variable_name].data
            self.set_attribute(variable_name, attribute.data)

        self.count_vertices()
