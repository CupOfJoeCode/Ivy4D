from math import *
import vecs


# Idk the math behind this i just copied it from somewhere
# It takes one point as a Vec3 and rotates it around the origin
def rotateVector(vec, vec2):
    xRot = vec2.x
    yRot = vec2.y
    zRot = vec2.z

    cosa = cos(zRot)
    sina = sin(zRot)

    cosb = cos(yRot)
    sinb = sin(yRot)

    cosc = cos(xRot)
    sinc = sin(xRot)

    Axx = cosa * cosb
    Axy = cosa * sinb * sinc - sina * cosc
    Axz = cosa * sinb * cosc + sina * sinc

    Ayx = sina * cosb
    Ayy = sina * sinb * sinc + cosa * cosc
    Ayz = sina * sinb * cosc - cosa * sinc

    Azx = -sinb
    Azy = cosb * sinc
    Azz = cosb * cosc

    px = vec.x
    py = vec.y
    pz = vec.z

    pointx = Axx * px + Axy * py + Axz * pz
    pointy = Ayx * px + Ayy * py + Ayz * pz
    pointz = Azx * px + Azy * py + Azz * pz
    return vecs.Vec3(pointx, pointy, pointz)
