from math import hypot, pow, acos

from typing import List


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __truediv__(self, n):
        return Point(self.x / n, self.y / n)


def sum_p(args: List[Point]):
    ans = Point(0, 0)
    for p in args:
        ans += p
    return ans


def avg_p(args: List[Point]):
    size = len(args)
    if size == 0:
        return Point(0, 0)
    return sum_p(args) / size


def dist_p(p1: Point, p2: Point):
    return hypot(p1.x - p2.x, p1.y - p2.y)


def square(n1):
    return pow(n1, 2)


def angle(opposite, adjacent1, adjacent2):
    res = (square(adjacent1) + square(adjacent2) - square(opposite)) / \
          (2 * adjacent1 * adjacent2)
    return acos(res)
