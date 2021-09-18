from triangle import Triangle
from vec3d import Vec3d


class Mesh:
    tris: list[Triangle]

    def __init__(self, tris: list[Triangle] = None):
        if tris is not None:
            self.tris: list[Triangle] = tris
        else:
            self.tris = []

    def LoadFromObjectFile(self, filename: str):
        verts = []
        with open(filename, "r") as f:
            while True:
                line = f.readline()
                if not line:
                    break

                if line[0] == "v":
                    x, y, z = line[2:].split(" ")
                    verts.append(Vec3d(float(x), float(y), float(z)))
                elif line[0] == "f":
                    p1, p2, p3 = line[2:].split(" ")
                    self.tris.append(
                        Triangle(
                            verts[int(p1) - 1],
                            verts[int(p2) - 1],
                            verts[int(p3) - 1],
                            (0, 0, 0),
                        )
                    )
