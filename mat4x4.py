from vec3d import Vec3d

from math import cos, sin, tan, pi


class Mat4x4:
    m: list

    def __init__(self, m: list[list[int]] = None):
        if m is None:
            m = [[0.0 for _ in range(4)] for _ in range(4)]
        self.m = m

    def __mul__(self, other):
        if isinstance(other, Vec3d):
            v = Vec3d()
            v.x = other.x * self.m[0][0] + other.y * self.m[1][0] + other.z * self.m[2][0] + other.w * self.m[3][0]
            v.y = other.x * self.m[0][1] + other.y * self.m[1][1] + other.z * self.m[2][1] + other.w * self.m[3][1]
            v.z = other.x * self.m[0][2] + other.y * self.m[1][2] + other.z * self.m[2][2] + other.w * self.m[3][2]
            v.w = other.x * self.m[0][3] + other.y * self.m[1][3] + other.z * self.m[2][3] + other.w * self.m[3][3]
            return v
        elif isinstance(other, Mat4x4):
            matrix = Mat4x4()
            for c in range(4):
                for r in range(4):
                    matrix.m[r][c] = self.m[r][0] * other.m[0][c] + self.m[r][1] * other.m[1][c] + self.m[r][2] * \
                                     other.m[2][c] + self.m[r][3] * other.m[3][c]
            return matrix
        return NotImplemented

    def QuikInverse(self):
        matrix = Mat4x4()
        matrix.m[0][0] = self.m[0][0]
        matrix.m[0][1] = self.m[1][0]
        matrix.m[0][2] = self.m[2][0]
        matrix.m[0][3] = 0.0

        matrix.m[1][0] = self.m[0][1]
        matrix.m[1][1] = self.m[1][1]
        matrix.m[1][2] = self.m[2][1]
        matrix.m[1][3] = 0.0

        matrix.m[2][0] = self.m[0][2]
        matrix.m[2][1] = self.m[1][2]
        matrix.m[2][2] = self.m[2][2]
        matrix.m[2][3] = 0.0

        matrix.m[3][0] = -(self.m[3][0] * matrix.m[0][0] + self.m[3][1] * matrix.m[1][0] + self.m[3][2] * matrix.m[2][0]);
        matrix.m[3][1] = -(self.m[3][0] * matrix.m[0][1] + self.m[3][1] * matrix.m[1][1] + self.m[3][2] * matrix.m[2][1]);
        matrix.m[3][2] = -(self.m[3][0] * matrix.m[0][2] + self.m[3][1] * matrix.m[1][2] + self.m[3][2] * matrix.m[2][2]);
        matrix.m[3][3] = 1.0

        return matrix


def Matrix_MakeIdentity() -> Mat4x4:
    matrix = Mat4x4()
    matrix.m[0][0] = 1.0
    matrix.m[1][1] = 1.0
    matrix.m[2][2] = 1.0
    matrix.m[3][3] = 1.0
    return matrix


def Matrix_MakeRotationX(fAngleRad: float) -> Mat4x4:
    matrix = Mat4x4()
    matrix.m[0][0] = 1.0
    matrix.m[1][1] = cos(fAngleRad)
    matrix.m[1][2] = sin(fAngleRad)
    matrix.m[2][1] = -sin(fAngleRad)
    matrix.m[2][2] = cos(fAngleRad)
    matrix.m[3][3] = 1.0
    return matrix


def Matrix_MakeRotationY(fAngleRad: float) -> Mat4x4:
    matrix = Mat4x4()
    matrix.m[0][0] = cos(fAngleRad)
    matrix.m[0][2] = sin(fAngleRad)
    matrix.m[2][0] = -sin(fAngleRad)
    matrix.m[1][1] = 1.0
    matrix.m[2][2] = cos(fAngleRad)
    matrix.m[3][3] = 1.0
    return matrix


def Matrix_MakeRotationZ(fAngleRad: float) -> Mat4x4:
    matrix = Mat4x4()
    matrix.m[0][0] = cos(fAngleRad)
    matrix.m[0][1] = sin(fAngleRad)
    matrix.m[1][0] = -sin(fAngleRad)
    matrix.m[1][1] = cos(fAngleRad)
    matrix.m[2][2] = 1.0
    matrix.m[3][3] = 1.0
    return matrix


def Matrix_MakeTranslation(x: float, y: float, z: float) -> Mat4x4:
    matrix = Mat4x4()
    matrix.m[0][0] = 1.0
    matrix.m[1][1] = 1.0
    matrix.m[2][2] = 1.0
    matrix.m[3][3] = 1.0
    matrix.m[3][0] = x
    matrix.m[3][1] = y
    matrix.m[3][2] = z
    return matrix


def Matrix_MakeProjection(fFovDegrees: float, fAspectRatio: float, fNear: float, fFar: float) -> Mat4x4:
    fFovRad = 1.0 / tan(fFovDegrees * 0.5 / 180.0 * pi)
    matrix = Mat4x4()
    matrix.m[0][0] = fAspectRatio * fFovRad
    matrix.m[1][1] = fFovRad
    matrix.m[2][2] = fFar / (fFar - fNear)
    matrix.m[3][2] = (-fFar * fNear) / (fFar - fNear)
    matrix.m[2][3] = 1.0
    matrix.m[3][3] = 0.0
    return matrix


def Matrix_PointAt(pos: Vec3d, target: Vec3d, up: Vec3d) -> Mat4x4:
    # Calculate new forward direction
    newForward = target - pos
    newForward = newForward.Normalise()

    # Calculate new Up direction
    a = newForward * up.DotProduct(newForward)
    newUp = up - a
    newUp = newUp.Normalise()
    newRight = newUp.CrossProduct(newForward)

    matrix = Mat4x4()
    matrix.m[0][0] = newRight.x
    matrix.m[0][1] = newRight.y
    matrix.m[0][2] = newRight.z
    matrix.m[0][3] = 0.0

    matrix.m[1][0] = newUp.x
    matrix.m[1][1] = newUp.y
    matrix.m[1][2] = newUp.z
    matrix.m[1][3] = 0.0

    matrix.m[2][0] = newForward.x
    matrix.m[2][1] = newForward.y
    matrix.m[2][2] = newForward.z
    matrix.m[2][3] = 0.0

    matrix.m[3][0] = pos.x
    matrix.m[3][1] = pos.y
    matrix.m[3][2] = pos.z
    matrix.m[3][3] = 1.0
    return matrix

