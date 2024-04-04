from typing import Optional

from socceranalyzer.common.geometric.point import Point
from socceranalyzer.common.geometric.rectangle import Rectangle


class Field:
    """"
        A class to represent a soccer field.

        field(width: float, length: float, center: Point,penalty_area_left: Rectangle, penalty_area_right: Rectangle, small_penalty_area_left: Rectangle,  small_penalty_area_right: Rectangle,  goalpost_left: Rectangle, goalpost_right: Rectangle)

        Attributes
        ----------
            public through @properties:
                width: float
                    total width of the field
                length: float
                    total length of the field
                center: Point
                    center of the field
                penalty_area_left: SORectangle
                    defines the left penalty area in the field
                penalty_area_right: SORectangle
                    defines the right penalty area in the field
                small_penalty_area_left: SORectangle
                    defines the left small penalty area in the field
                small_penalty_area_right: SORectangle
                    defines the right small penalty area in the field
                goalpost_left: SORectangle 
                    defines the left goalpost in the field 
                goalpost_right: SORectangle 
                    defines the right goalpost in the field 
                
    """
    def __init__(self, width: float, length: float, center: Point, center_circle_diameter: float,
                penalty_area_left: Rectangle,
                penalty_area_right: Rectangle,
                small_penalty_area_left: Rectangle, 
                small_penalty_area_right: Rectangle, 
                goalpost_left: Rectangle,
                goalpost_right: Rectangle,
                penalty_mark_left: Optional[Point] = None,
                penalty_mark_right: Optional[Point] = None
                ):
        self.__width: float = width
        self.__length: float = length
        self.__center: Point = center
        self.__center_circle_diameter: float = center_circle_diameter
        self.__penalty_area_left: Rectangle = penalty_area_left
        self.__penalty_area_right: Rectangle = penalty_area_right
        self.__small_penalty_area_left: Rectangle = small_penalty_area_left
        self.__small_penalty_area_right: Rectangle = small_penalty_area_right
        self.__goalpost_left: Rectangle = goalpost_left
        self.__goalpost_right: Rectangle = goalpost_right
        self.__penalty_mark_left: Optional[Point] = penalty_mark_left
        self.__penalty_mark_right: Optional[Point] = penalty_mark_right
    
    @property
    def width(self):
        return self.__width
    
    @property
    def length(self):
        return self.__length
    
    @property
    def center(self):
        return self.__center

    @property
    def center_circle_diameter(self):
        return self.__center_circle_diameter

    @property
    def penalty_area_left(self):
        return self.__penalty_area_left
    
    @property
    def penalty_area_right(self):
        return self.__penalty_area_right

    @property
    def small_penalty_area_left(self):
        return self.__small_penalty_area_left
    
    @property
    def small_penalty_area_right(self):
        return self.__small_penalty_area_right
    
    @property
    def goalpost_left(self):
        return self.__goalpost_left
    
    @property
    def goalpost_right(self):
        return self.__goalpost_right

    @property
    def penalty_mark_left(self):
        return self.__penalty_mark_left

    @property
    def penalty_mark_right(self):
        return self.__penalty_mark_right


class Field2D(Field):
    def __init__(self):
        raise NotImplementedError
