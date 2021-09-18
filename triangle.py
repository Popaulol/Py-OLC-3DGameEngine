from vec3d import Vec3d, Vector_IntersectPlane


class Triangle:
    p: list[Vec3d, Vec3d, Vec3d]
    color: tuple[float, float, float]

    def __init__(
        self,
        p1: Vec3d = None,
        p2: Vec3d = None,
        p3: Vec3d = None,
        color: tuple[float, float, float] = (255, 255, 255),
    ):
        if p1 is None:
            p1 = Vec3d()
        if p2 is None:
            p2 = Vec3d()
        if p3 is None:
            p3 = Vec3d()
        self.p = [p1, p2, p3]
        self.color: tuple[float, float, float] = color


def Triangle_ClipAgainstPlane(plane_p: Vec3d, plane_n: Vec3d, in_tri: Triangle):
    def dist(p: Vec3d):
        # n = p.Normalise()
        return (
            plane_n.x * p.x
            + plane_n.y * p.y
            + plane_n.z * p.z
            - plane_n.DotProduct(plane_p)
        )

    plane_n = plane_n.Normalise()

    inside_points = [Vec3d() for _ in range(4)]
    nInsidePointCount = 0
    outside_points = [Vec3d() for _ in range(4)]
    nOutsidePointCount = 0

    d0 = dist(in_tri.p[0])
    d1 = dist(in_tri.p[1])
    d2 = dist(in_tri.p[2])

    if d0 >= 0:
        inside_points[nInsidePointCount] = in_tri.p[0]
        nInsidePointCount += 1
    else:
        outside_points[nOutsidePointCount] = in_tri.p[0]
        nOutsidePointCount += 1
    if d1 >= 0:
        inside_points[nInsidePointCount] = in_tri.p[1]
        nInsidePointCount += 1
    else:
        outside_points[nOutsidePointCount] = in_tri.p[1]
        nOutsidePointCount += 1
    if d2 >= 0:
        inside_points[nInsidePointCount] = in_tri.p[2]
        nInsidePointCount += 1
    else:
        outside_points[nOutsidePointCount] = in_tri.p[2]
        nOutsidePointCount += 1

    if nInsidePointCount == 0:
        return 0, None, None

    if nInsidePointCount == 3:
        return 1, in_tri, None

    if nInsidePointCount == 1 and nOutsidePointCount == 2:
        out_tri1 = Triangle()
        out_tri1.color = in_tri.color
        out_tri1.p[0] = inside_points[0]
        out_tri1.p[1] = Vector_IntersectPlane(
            plane_p, plane_n, inside_points[0], outside_points[0]
        )
        out_tri1.p[2] = Vector_IntersectPlane(
            plane_p, plane_n, inside_points[0], outside_points[1]
        )

        return 1, out_tri1, None

    if nInsidePointCount == 2 and nOutsidePointCount == 1:
        out_tri1 = Triangle()
        out_tri1.color = in_tri.color

        out_tri2 = Triangle()
        out_tri2.color = in_tri.color

        out_tri1.p[0] = inside_points[0]
        out_tri1.p[1] = inside_points[1]
        out_tri1.p[2] = Vector_IntersectPlane(
            plane_p, plane_n, inside_points[0], outside_points[0]
        )

        out_tri2.p[0] = inside_points[1]
        out_tri2.p[1] = out_tri1.p[2]
        out_tri2.p[2] = Vector_IntersectPlane(
            plane_p, plane_n, inside_points[1], outside_points[0]
        )

        return 2, out_tri1, out_tri2
