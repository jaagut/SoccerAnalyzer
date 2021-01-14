from .basic import Point
from .measures import distance

class Block:
    def __init__(self, width=0, height=0, center_x=0, center_y=0):
        self.width = width
        self.height = height
        self.center = [center_x, center_y]

    def center(self):
        center = [self.width/2, self.height/2]

        return center

    def is_inside(self, position):
        pass

class Radial:
    def __init__(self, ray, center):
        self.ray = ray
        self.area = 3.14 * self.ray * self.ray
        self.center = center

    def describe(self):
        print('Ray: {}\nArea: {}'.format(self.ray,self.area))

    def is_inside(self, point):
        position = Point(self.center[0], self.center[1])
        dist = distance(point, position)

        if dist > self.ray:
            return False
        else:
            return True

