import socceranalyzer


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
    def __init__(self, width, length, center, small_penalty_area, penalty_area):
        self.__width: float = width
        self.__length: float = length
        self.__center: socceranalyzer.Point = center
        self.__small_penalty_area: socceranalyzer.Rectangle = small_penalty_area
        self.__penalty_area: socceranalyzer.Rectangle = penalty_area


class Field2D(Field):
    def __init__(self):
        raise NotImplementedError
