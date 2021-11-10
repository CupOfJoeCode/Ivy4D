import vecs


# Stores position, rotation, and scale vectors
class Transform:
    def __init__(self,
                 translate=vecs.Vec3(),
                 scale=vecs.Vec3(1., 1., 1.),
                 rotate=vecs.Vec3()):
        self.translate = translate
        self.scale = scale
        self.rotate = rotate


class Mesh:
    def __init__(self, inVerts=[], inFaces=[]):
        self.verts = inVerts
        self.faces = inFaces
        self.color = vecs.Vec3(1., 0., 0.)
        self.transform = Transform()

    def subdivide(self, iter=1):
        outFaces = []
        for k in range(iter):
            for f in range(len(self.faces)):
                face = self.faces[f]
                vert0 = self.verts[face[0]]
                vert1 = self.verts[face[1]]
                vert2 = self.verts[face[2]]

                vind0 = face[0]
                vind1 = face[1]
                vind2 = face[2]

                mvert0 = (vert0 + vert1) / vecs.toVec3(2.)
                mvert1 = (vert1 + vert2) / vecs.toVec3(2.)
                mvert2 = (vert2 + vert0) / vecs.toVec3(2.)

                mind0 = len(self.verts)
                self.verts.append(mvert0)
                mind1 = len(self.verts)
                self.verts.append(mvert1)
                mind2 = len(self.verts)
                self.verts.append(mvert2)

                outFaces.append([vind0, mind0, mind2])
                outFaces.append([mind0, vind1, mind1])
                outFaces.append([mind2, mind1, vind2])
                outFaces.append([mind0, mind1, mind2])
            self.faces = outFaces
