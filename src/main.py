import pygame as pg
from pygame.locals import *
from PIL import Image
import numpy as np
from math import *
from copy import deepcopy

from OpenGL.GL import *
from OpenGL.GLU import *

from random import randint
from opensimplex import OpenSimplex

import mesh, objparse, vecs, camera, rotate

# Import all the default geometries
with open('shapes/sphere.obj', 'r') as fp:
    SPHERE_GEOMETRY = objparse.parseObj(fp.read())
with open('shapes/cube.obj', 'r') as fp:
    CUBE_GEOMETRY = objparse.parseObj(fp.read())
with open('shapes/plane.obj', 'r') as fp:
    PLANE_GEOMETRY = objparse.parseObj(fp.read())
with open('shapes/torus.obj', 'r') as fp:
    TORUS_GEOMETRY = objparse.parseObj(fp.read())
with open('shapes/plane16.obj', 'r') as fp:
    SUBDIV_PLANE_GEOMETRY = objparse.parseObj(fp.read())
noise = OpenSimplex()
# Regular window stuff
pg.init()
windowSize = (800, 600)
pg.display.set_caption('Ivy 4D')
d = pg.display.set_mode(windowSize, DOUBLEBUF | OPENGL)

# Makes the scene with a default cube (no clue where that idea is from)
DEFAULT_CUBE = deepcopy(CUBE_GEOMETRY)
DEFAULT_PLANE = deepcopy(SUBDIV_PLANE_GEOMETRY)

DEFAULT_PLANE.color = vecs.Vec3(0.2, 0.2, 0.7)
DEFAULT_PLANE.transform.scale = vecs.toVec3(4)
DEFAULT_PLANE.transform.rotate = vecs.Vec3(0.1, 0.2, 0)
for i in range(len(DEFAULT_PLANE.verts)):
    v = DEFAULT_PLANE.verts[i]
    DEFAULT_PLANE.verts[i].y = noise.noise2d(v.x, v.z)
scene = [DEFAULT_CUBE, DEFAULT_PLANE]


# Get surface normal for a triangle with the points p1,p2,p3
def getSurfaceNormal(p1, p2, p3):
    u = (p2).normalized() - (p1).normalized()
    v = (p3).normalized() - (p1).normalized()
    return vecs.Vec3((u.y * v.z) - (u.z * v.y), (u.z * v.x) - (u.x * v.z),
                     (u.x * v.y) - (u.y * v.x)).normalized()


GRID_SHADE = 0.  # Shade of black for the grid
GRID_POINTS = [(0, 0), (1, 0), (0, 0), (0, 1)]


def renderScene():
    glBegin(GL_LINES)
    # Draws the grid
    for x in range(-8, 8):
        for y in range(-8, 8):
            for i in GRID_POINTS:
                glColor3f(GRID_SHADE, GRID_SHADE, GRID_SHADE)
                glVertex3f(x + i[0], 0, y + i[1])
    glEnd()
    glBegin(GL_TRIANGLES)

    for msh in scene:
        currentCol = msh.color

        for f in msh.faces:
            outF = [msh.verts[f[0]], msh.verts[f[1]], msh.verts[f[2]]]

            for i in range(len(outF)):
                transformVert = rotate.rotateVector(outF[i],
                                                    msh.transform.rotate)
                transformVert = transformVert * msh.transform.scale
                transformVert = transformVert + msh.transform.translate
                outF[i] = transformVert

            faceNormal = getSurfaceNormal(msh.verts[f[0]], msh.verts[f[1]],
                                          msh.verts[f[2]])

            averageNormal = (faceNormal.x + faceNormal.y + faceNormal.z) / 3.
            vertCol = currentCol + vecs.toVec3(averageNormal / 2)

            for currentVert in outF:
                glColor3f(vertCol.x, vertCol.y, vertCol.z)
                glVertex3f(currentVert.x, currentVert.y, currentVert.z)

    glEnd()


gluPerspective(60, (windowSize[0] / windowSize[1]), 0.01, 100.0)
glEnable(GL_DEPTH_TEST)

mouseDown = False
rightDown = False

pmouseX, pmouseY = (0, 0)

ROTATE_SENSITIVY = 0.3
ZOOM_SENSITIVIY = 1.1
OFFSET_SENSITIVITY = 0.002

cam = camera.Camera()

while True:
    for e in pg.event.get():
        if e.type == pg.QUIT:
            pg.quit()
            quit()
        if e.type == pg.MOUSEBUTTONDOWN:
            if e.button == 1:
                mouseDown = True
            elif e.button == 3:
                rightDown = True
            elif e.button == 4:
                cam.zoom *= ZOOM_SENSITIVIY
            elif e.button == 5:
                cam.zoom /= ZOOM_SENSITIVIY
        if e.type == pg.MOUSEBUTTONUP:
            if e.button == 1:
                mouseDown = False
            elif e.button == 3:
                rightDown = False

    mouseX, mouseY = pg.mouse.get_pos()

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glClearColor(0.5, 0.5, 0.5, 1.)
    glPushMatrix()

    glTranslatef(cam.offset.x, cam.offset.y, -1)
    glScalef(cam.zoom, cam.zoom, cam.zoom)
    glRotatef(cam.rotation.x, 1, 0, 0)
    glRotatef(cam.rotation.y, 0, 1, 0)

    renderScene()
    glPopMatrix()
    dmouseX = mouseX - pmouseX
    dmouseY = mouseY - pmouseY
    if mouseDown:
        cam.rotation.x += dmouseY * ROTATE_SENSITIVY
        cam.rotation.y += dmouseX * ROTATE_SENSITIVY
    if rightDown:
        cam.offset.x += dmouseX * OFFSET_SENSITIVITY
        cam.offset.y -= dmouseY * OFFSET_SENSITIVITY
    pmouseX, pmouseY = (mouseX, mouseY)
    pg.display.flip()
    pg.time.wait(1)