import mesh
import vecs


# Reads in an obj file and returns a Mesh based on the geometry
def parseObj(inObj):
    lines = inObj.split('\n')
    for i in range(len(lines)):
        lines[i] = lines[i].split(' ')
    outVerts = []
    outFaces = []
    for line in lines:
        if line[0] == 'v':
            outVerts.append(
                vecs.Vec3(float(line[1]), float(line[2]), float(line[3])))
        elif line[0] == 'f':
            outFaces.append(
                [int(line[1]) - 1,
                 int(line[2]) - 1,
                 int(line[3]) - 1])

    return mesh.Mesh(outVerts, outFaces)


def dumpObj(inMesh):
    outTxt = 'o Mesh\n'

    for v in inMesh.verts:
        outTxt += 'v ' + str(v.x) + ' ' + str(v.y) + ' ' + str(v.z) + '\n'
    outTxt += 's off\n'
    for f in inMesh.faces:
        outTxt += 'f ' + str(f[0]+1) + ' ' + \
            str(f[1]+1) + ' ' + str(f[2]+1) + '\n'
    return outTxt
