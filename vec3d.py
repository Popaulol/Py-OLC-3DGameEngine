from math import sqrt
from numbers import Number


class Vec3d:
    def __init__(self, x: float = 0.0, y: float = 0.0, z: float = 0.0, w: float = 1.0):
        self.x: float = x
        self.y: float = y
        self.z: float = z
        self.w: float = w

    def coords2d(self):
        return self.x, self.y

    def coords3d(self):
        return self.x, self.y, self.z

    def __add__(self, other):
        if isinstance(other, Vec3d):
            return Vec3d(self.x + other.x, self.y + other.y, self.z + other.z)
        return NotImplemented

    def __sub__(self, other):
        if isinstance(other, Vec3d):
            return Vec3d(self.x - other.x, self.y - other.y, self.z - other.z)
        return NotImplemented

    def __mul__(self, other):
        if isinstance(other, Number):
            return Vec3d(self.x * other, self.y * other, self.z * other)
        return NotImplemented

    def __truediv__(self, other):
        return Vec3d(self.x / other, self.y / other, self.z / other)

    def DotProduct(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z

    def CrossProduct(self, other):
        v = Vec3d()
        v.x = self.y * other.z - self.z * other.y
        v.y = self.z * other.x - self.x * other.z
        v.z = self.x * other.y - self.y * other.x
        return v

    def length(self):
        return sqrt(self.DotProduct(self))

    def Normalise(self):
        length = self.length()
        if length == 0:
            return Vec3d(float("inf"), float("inf"), float("inf"))
        return Vec3d(self.x / length, self.y / length, self.z / length)

    def __repr__(self):
        return f"Vec3d({self.x}, {self.y}, {self.z})"


def Vector_IntersectPlane(plane_p: Vec3d, plane_n: Vec3d, lineStart: Vec3d, lineEnd: Vec3d) -> Vec3d:
    plane_n = plane_n.Normalise()
    plane_d = -(plane_n.DotProduct(plane_p))
    ad = lineStart.DotProduct(plane_n)
    bd = lineEnd.DotProduct(plane_n)
    t = (-plane_d - ad) / (bd - ad)
    lineStartToEnd = lineEnd - lineStart
    lineToIntersect = lineStartToEnd * t
    return lineStart + lineToIntersect
