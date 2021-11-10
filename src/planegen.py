import vecs
import mesh
import objparse
SIZE = 8
outMesh = mesh.Mesh()


def setPoint(inVec):
    if inVec in outMesh.verts:
        return outMesh.verts.index(inVec)

    outMesh.verts.append(inVec)
    return outMesh.verts.index(inVec)


for x in range(-SIZE, SIZE):
    for y in range(-SIZE, SIZE):
        p0 = vecs.Vec3(x, 0, y) / vecs.toVec3(SIZE)
        p1 = vecs.Vec3(x + 1, 0, y) / vecs.toVec3(SIZE)
        p2 = vecs.Vec3(x + 1, 0, y + 1) / vecs.toVec3(SIZE)
        p3 = vecs.Vec3(x, 0, y + 1) / vecs.toVec3(SIZE)

        outMesh.faces.append([
            setPoint(p0),
            setPoint(p1),
            setPoint(p2)
        ])
        outMesh.faces.append([
            setPoint(p0),
            setPoint(p2),
            setPoint(p3)
        ])
with open('shapes/plane16.obj', 'w') as fp:
    fp.write(objparse.dumpObj(outMesh))
