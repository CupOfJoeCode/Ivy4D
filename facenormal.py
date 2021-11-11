import vecs

# Get surface normal for a triangle with the points p1,p2,p3


def getSurfaceNormal(p1, p2, p3):
    u = (p2).normalized() - (p1).normalized()
    v = (p3).normalized() - (p1).normalized()
    return vecs.Vec3((u.y * v.z) - (u.z * v.y), (u.z * v.x) - (u.x * v.z),
                     (u.x * v.y) - (u.y * v.x)).normalized()
