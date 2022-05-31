from socceranalyzer.common.geometric.point import Point
from socceranalyzer.common.geometric.rectangle import Rectangle

class Field:
    """"
        A class to represent a soccer field.

        field(width: float, length: float, center: Point,
                small_penalty_area: Rectangle, penalty_area: Rectangle)

        Attributes
        ----------
            private:
                width: float
                    total width of the field
                length: float
                    total length of the field
                center: Point
                    center of the field
                small_penalty_area: Rectangle
                    defines the small penalty area in the field
                penalty_area: Rectangle
                    defines the penalty area in the field
    """
    def __init__(self, width: float, length: float, center: Point,
                small_penalty_area_left: Rectangle, 
                small_penalty_area_right: Rectangle,
                penalty_area_left: Rectangle,
                penalty_area_right: Rectangle):
                
        self.__width = width
        self.__length = length
        self.__center = center
        self.__small_penalty_area_left = small_penalty_area_left
        self.__small_penalty_area_right = small_penalty_area_right
        self.__penalty_area_left = penalty_area_left
        self.__penalty_area_right = penalty_area_right



class Field2D(Field):
    def __init__(self):
        raise NotImplementedError
