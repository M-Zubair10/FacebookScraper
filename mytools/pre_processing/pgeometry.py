import numpy as np
import random
import cv2


class Rectangle:
    def __init__(self, rect):
        """
        Rectangle object
        :param rect: [x, y, w, h]
        """
        self.rect = rect
        self.xyxy = self.rect[:2] + [self.rect[0] + self.rect[2], self.rect[1] + self.rect[3]]
        self.xywh = self.rect

    def center(self):
        """Get center of rect object"""
        return int((self.rect[0] + self.rect[2]) / 2), int((self.rect[1] + self.rect[3] / 2))

    def expand(self, k_dist, output='self'):
        """
        Expand rectangle::

        :param rect: x1, y1, x2, y2
        :param k_dist: expanding distance or border
        :return: new rectangle
        """

        x1, y1, x2, y2 = self.rect
        x1 -= k_dist
        y1 -= k_dist
        x2 += k_dist + k_dist
        y2 += k_dist + k_dist

        if output == 'self':
            self.rect = [x1, y1, x2, y2]
        else:
            return [x1, y1, x2, y2]

    def shrink(self, k_dist, output='self'):
        """Same as expand with -ve k_distance"""
        return self.expand(-k_dist, output)

    def rangeXY(self):
        """
        Get coordinates
        :param rect: input rectangle
        :return: x, y
        """

        X, Y = set(range(self.rect[0], self.rect[0] + self.rect[2])), set(range(self.rect[1], self.rect[1] + self.rect[3]))
        return X, Y

    def is_overlap(self, rect):
        """
        Is self.rect overlaps rect
        :param rect: new rectangle
        :return: bool
        """

        x1_1, y1_1, x2_1, y2_1 = self.rect
        x1_2, y1_2, x2_2, y2_2 = rect
        return (x1_1 < x2_2) and (x2_1 > x1_2) and (y1_1 < y2_2) and (y2_1 > y1_2)

    def draw(self, img, color=None, thickness=1):
        """
        Draw rectangle on given image
        :param img: cv2.imread() -> img
        :param color: random if None
        :param thickness: rect thickness
        :return: None
        """

        if color is None:
            color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        cv2.rectangle(img, self.rect[:2], (self.rect[0] + self.rect[2], self.rect[1] + self.rect[3]), color, thickness)

    @staticmethod
    def show(rects, img=np.zeros([1000, 800, 3]), i=1, thickness=1, position=(), _format='xywh'):
        """
        See rect changes
        :param rects: [rect1, rect2, ...]
        :param i: show image after i rect plot
        :param position: move output window there
        :param format: boxes format [xywh or xyxy]
        :return: None
        """
        _img = img.copy()
        for r, rect in enumerate(rects):
            color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            if _format == 'xywh':
                x1, y1, x2, y2 = rect[0], rect[1], rect[0] + rect[2], rect[1] + rect[3]
            elif _format == 'xyxy':
                x1, y1, x2, y2 = rect
            cv2.rectangle(_img, (x1, y1), (x2, y2), color, thickness)
            if r % i - 1 == 0 or i == 1:
                cv2.imshow("View", _img)
                if position:
                    cv2.moveWindow("View", *position)
                cv2.waitKey(0)
                cv2.destroyAllWindows()


class Polygon:
    def __init__(self, points):
        self.points = points

    def to_rect(self):
        x_min, x_max = self.points[0][0], self.points[0][0]
        y_min, y_max = self.points[0][1], self.points[0][1]
        for vertex in self.points[1:]:
            x, y = vertex
            x_min = min(x_min, x)
            x_max = max(x_max, x)
            y_min = min(y_min, y)
            y_max = max(y_max, y)
        return (x_min, y_min, x_max, y_max)

