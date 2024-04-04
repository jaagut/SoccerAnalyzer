class Point:
    '''
    A class to create a point somewhere in the field.
    ...
    Attributes
    ----------
    x: float
        x coordinates of the point in the field
    y: float
        y coordinates of the point in the field
    z: float
        z coordinates of the point in the field
    '''

    def __init__(self, x=0.0, y=0.0, z=0.0):
        '''
        Constructs all the necessary attributes for the point object.
        Parameters
        ----------
        x: float
            x coordinates of the point in the field
        y: float
            y coordinates of the point in the field
        z: float
            z coordinates of the point in the field
        '''
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        return f"{self.x=}, {self.y=}, {self.z=}"
