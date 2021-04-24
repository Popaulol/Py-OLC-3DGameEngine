import custom_fast_turtle
from triangle import Triangle, Triangle_ClipAgainstPlane
from vec3d import Vec3d
from Mesh import Mesh
from mat4x4 import Mat4x4, Matrix_MakeProjection, Matrix_MakeRotationX, Matrix_MakeRotationZ, Matrix_MakeTranslation, \
    Matrix_MakeIdentity, Matrix_MakeRotationY, Matrix_PointAt

from input_handler import curr_held
from pynput.keyboard import Key
import time


class PyOlcEngine3D:
    meshCube: Mesh = Mesh()
    matProj: Mat4x4 = Mat4x4()  # Matrix that converts from view space to screen space
    vCamera: Vec3d = Vec3d()  # Location of camera in world space
    vLookDir: Vec3d = Vec3d()  # Direction vector along the direction camera points
    fYaw: float = 0.0  # FPS Camera rotation in XZ plane
    fTheta: float = 0.0  # Spins World transform

    def __init__(self):
        pass

    def on_create(self, filename):
        self.meshCube.LoadFromObjectFile(filename)
        self.matProj = Matrix_MakeProjection(90.0, float(custom_fast_turtle.ScreenHeight()) / float(
            custom_fast_turtle.ScreenWidth()), 0.1, 1000.0)
        return True

    def on_update(self, ElapsedTime):

        if Key.up in curr_held:
            self.vCamera.y += 8.0 * ElapsedTime
        if Key.down in curr_held:
            self.vCamera.y -= 8.0 * ElapsedTime

        if Key.left in curr_held:
            self.vCamera.x -= 8.0 * ElapsedTime
        if Key.right in curr_held:
            self.vCamera.x += 8.0 * ElapsedTime

        vForward = self.vLookDir * (8 * ElapsedTime)

        for letter in curr_held:
            try:
                if letter.char == "w":
                    self.vCamera = self.vCamera + vForward

                if letter.char == "s":
                    self.vCamera = self.vCamera - vForward

                if letter.char == "a":
                    self.fYaw -= 2.0 * ElapsedTime

                if letter.char == "d":
                    self.fYaw += 2.0 * ElapsedTime
            except AttributeError:
                pass

        # self.fTheta += 1.0 * ElapsedTime
        matRotX = Matrix_MakeRotationX(self.fTheta)
        matRotZ = Matrix_MakeRotationZ(self.fTheta * 0.5)

        matTrans = Matrix_MakeTranslation(0.0, 0.0, 5.0)

        matWorld = Matrix_MakeIdentity()
        matWorld = matRotZ * matRotX
        matWorld = matWorld * matTrans

        vUp = Vec3d(0, 1, 0)
        vTarget = Vec3d(0, 0, 1)
        matCameraRot = Matrix_MakeRotationY(self.fYaw)
        self.vLookDir = matCameraRot * vTarget

        vTarget = self.vCamera + self.vLookDir

        matCamera = Matrix_PointAt(self.vCamera, vTarget, vUp)

        matView = matCamera.QuikInverse()

        vecTrianglesToRaster = []

        for i, tri in enumerate(self.meshCube.tris):
            triProjected, triTransformed, triViewed = Triangle(), Triangle(), Triangle()

            triTransformed.p[0] = matWorld * tri.p[0]
            triTransformed.p[1] = matWorld * tri.p[1]
            triTransformed.p[2] = matWorld * tri.p[2]

            line1 = triTransformed.p[1] - triTransformed.p[0]
            line2 = triTransformed.p[2] - triTransformed.p[0]

            normal = line1.CrossProduct(line2)

            normal = normal.Normalise()
            vCameraRay = triTransformed.p[0] - self.vCamera

            if normal.DotProduct(vCameraRay) < 0.0:
                light_direction = Vec3d(0.0, 1.0, -1.0)
                light_direction = light_direction.Normalise()
                dp = max(0.1, light_direction.DotProduct(normal))

                triTransformed.color = (dp, dp, dp)

                triViewed.p[0] = matView * triTransformed.p[0]
                triViewed.p[1] = matView * triTransformed.p[1]
                triViewed.p[2] = matView * triTransformed.p[2]
                triViewed.color = triTransformed.color

                clipped = [None, None]
                nClippedTriangles, clipped[0], clipped[1] = Triangle_ClipAgainstPlane(Vec3d(0.0, 0.0, 0.1),
                                                                                      Vec3d(0.0, 0.0, 1.0),
                                                                                      triViewed)
                for n in range(nClippedTriangles):
                    triProjected.p[0] = self.matProj * clipped[n].p[0]
                    triProjected.p[1] = self.matProj * clipped[n].p[1]
                    triProjected.p[2] = self.matProj * clipped[n].p[2]
                    triProjected.color = clipped[n].color

                    triProjected.p[0] = triProjected.p[0] / triProjected.p[0].w
                    triProjected.p[1] = triProjected.p[1] / triProjected.p[1].w
                    triProjected.p[2] = triProjected.p[2] / triProjected.p[2].w

                    triProjected.p[0].x *= -1.0
                    triProjected.p[1].x *= -1.0
                    triProjected.p[2].x *= -1.0
                    # triProjected.p[0].y *= -1.0
                    # triProjected.p[1].y *= -1.0
                    # triProjected.p[2].y *= -1.0

                    vOffsetView = Vec3d(1, 1, 0)
                    triProjected.p[0] = triProjected.p[0] + vOffsetView
                    triProjected.p[1] = triProjected.p[1] + vOffsetView
                    triProjected.p[2] = triProjected.p[2] + vOffsetView
                    triProjected.p[0].x *= 0.5 * float(custom_fast_turtle.ScreenWidth())
                    triProjected.p[0].y *= 0.5 * float(custom_fast_turtle.ScreenHeight())
                    triProjected.p[1].x *= 0.5 * float(custom_fast_turtle.ScreenWidth())
                    triProjected.p[1].y *= 0.5 * float(custom_fast_turtle.ScreenHeight())
                    triProjected.p[2].x *= 0.5 * float(custom_fast_turtle.ScreenWidth())
                    triProjected.p[2].y *= 0.5 * float(custom_fast_turtle.ScreenHeight())

                    vecTrianglesToRaster.append(triProjected)

        vecTrianglesToRaster.sort(key=lambda t1: (t1.p[0].z + t1.p[1].z + t1.p[2].z) / 3.0, reverse=True)

        custom_fast_turtle.clear()

        for triToRaster in vecTrianglesToRaster:
            clipped = [Triangle(), Triangle()]
            listTriangles = []

            listTriangles.append(triToRaster)

            nNewTriangles = 1
            for p in range(4):
                nTrisToAdd = 0
                while nNewTriangles > 0:
                    test = listTriangles.pop(0)
                    nNewTriangles -= 1

                    if p == 0:
                        nTrisToAdd, clipped[0], clipped[1] = Triangle_ClipAgainstPlane(Vec3d(0.0, 0.0, 0.0),
                                                                                       Vec3d(0.0, 1.0, 0.0),
                                                                                       test)
                    elif p == 1:
                        nTrisToAdd, clipped[0], clipped[1] = Triangle_ClipAgainstPlane(
                            Vec3d(0.0, float(custom_fast_turtle.ScreenHeight() - 1), 0.0),
                            Vec3d(0.0, -1.0, 0.0),
                            test)
                    elif p == 2:
                        nTrisToAdd, clipped[0], clipped[1] = Triangle_ClipAgainstPlane(Vec3d(0.0, 0.0, 0.0),
                                                                                       Vec3d(1.0, 0.0, 0.0),
                                                                                       test)
                    elif p == 3:
                        nTrisToAdd, clipped[0], clipped[1] = Triangle_ClipAgainstPlane(
                            Vec3d(float(custom_fast_turtle.ScreenWidth() - 1), 0.0, 0.0),
                            Vec3d(-1.0, 0.0, 0.0),
                            test)
                    for w in range(nTrisToAdd):
                        listTriangles.append(clipped[w])

                nNewTriangles = len(listTriangles)

            for t in listTriangles:
                custom_fast_turtle.draw_triangle(t)
        return True


if __name__ == '__main__':
    win = PyOlcEngine3D()
    win.on_create("axis.obj")
    timed = 0
    while True:
        start_time = time.time()
        win.on_update(timed)
        custom_fast_turtle.update()
        timed = time.time() - start_time
        print(f"Frame Rendered in {timed}, Camera: {win.vCamera}, Theta: {win.fTheta}")
