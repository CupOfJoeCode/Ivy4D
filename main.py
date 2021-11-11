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

import mesh
import objparse
import vecs
import camera
import rotate
import light
import facenormal


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


scene = [DEFAULT_CUBE]
sceneSel = 0
LIGHT = light.Light()


GRID_SHADE = 0.  # Shade of black for the grid
GRID_POINTS = [(0, 0), (1, 0), (0, 0), (0, 1)]
blinkTimer = 0
prevCol = vecs.Vec3()

GIZMO_POINTS = [
    vecs.Vec3(1, 0, 0),
    vecs.Vec3(0, 1, 0),
    vecs.Vec3(0, 0, 1)
]

RECT_POINTS = [
    vecs.Vec3(-1, -1, -1),
    vecs.Vec3(1, -1, 0),
    vecs.Vec3(1, 1, 1),
]


def renderScene():
    global scene, sceneSel
    glBegin(GL_LINES)
    # Draws the grid
    for x in range(-8, 8):
        for y in range(-8, 8):
            for i in GRID_POINTS:
                glColor3f(GRID_SHADE, GRID_SHADE, GRID_SHADE)
                glVertex3f(x + i[0], 0, y + i[1])

    selectedMeshTransforms = scene[sceneSel].transform  # Mesh transforms

    # Draw gizmo in the middle of selected mesh
    for p in GIZMO_POINTS:
        pTrans = rotate.rotateVector(p,
                                     selectedMeshTransforms.rotate)
        pTrans = pTrans * selectedMeshTransforms.scale * vecs.toVec3(2.)
        pTrans = pTrans + selectedMeshTransforms.translate
        glColor3f(p.x, p.y, p.z)
        glVertex3f(selectedMeshTransforms.translate.x,
                   selectedMeshTransforms.translate.y, selectedMeshTransforms.translate.z)
        glColor3f(p.x, p.y, p.z)
        glVertex3f(pTrans.x, pTrans.y, pTrans.z)

    glEnd()

    glBegin(GL_TRIANGLES)  # Start drawing shapes

    for m in range(len(scene)):
        msh = scene[m]  # Currently rendering mesh
        currentCol = msh.color  # Mesh color

        for f in msh.faces:
            outF = [msh.verts[f[0]], msh.verts[f[1]], msh.verts[f[2]]]

            for i in range(len(outF)):
                transformVert = rotate.rotateVector(outF[i],
                                                    msh.transform.rotate)
                transformVert = transformVert * msh.transform.scale
                transformVert = transformVert + msh.transform.translate
                outF[i] = transformVert

            faceNormal = facenormal.getSurfaceNormal(msh.verts[f[0]], msh.verts[f[1]],
                                                     msh.verts[f[2]])

            averageNormal = (faceNormal.x + faceNormal.y + faceNormal.z) / 3.
            vertCol = currentCol + \
                (vecs.toVec3(averageNormal / 2) * LIGHT.color) + LIGHT.ambient

            for currentVert in outF:
                glColor3f(vertCol.x, vertCol.y, vertCol.z)
                glVertex3f(currentVert.x, currentVert.y, currentVert.z)

            if m == sceneSel:
                for currentVert in outF:
                    for v in RECT_POINTS:
                        glColor3f(0., 0., 0.)
                        glVertex3f(currentVert.x + v.x/10.,
                                   currentVert.y + v.y/10., currentVert.z + v.z/10.)

    glEnd()


gluPerspective(60, (windowSize[0] / windowSize[1]), 0.01, 100.0)
glEnable(GL_DEPTH_TEST)

mouseDown = False
rightDown = False

pmouseX, pmouseY = (0, 0)

ROTATE_SENSITIVY = 0.3
ZOOM_SENSITIVIY = 1.1
OFFSET_SENSITIVITY = 0.002

MOVE_SPEED = 0.04

cam = camera.Camera()

sceneSel = 0

waveOff = 0

keysPressed = {
    'left': False,
    'right': False,
    'up': False,
    'down': False,
    'z': False,
    'x': False
}

while True:
    # TODO: Add rotation and scaling
    for e in pg.event.get():
        if e.type == pg.QUIT:
            pg.quit()
            quit()
        if e.type == pg.KEYDOWN:
            if e.key == pg.K_w:
                cam.zoom *= ZOOM_SENSITIVIY
            elif e.key == pg.K_s:
                cam.zoom /= ZOOM_SENSITIVIY

            elif e.key == pg.K_LEFT:
                keysPressed['left'] = True
            elif e.key == pg.K_RIGHT:
                keysPressed['right'] = True
            elif e.key == pg.K_UP:
                keysPressed['up'] = True
            elif e.key == pg.K_DOWN:
                keysPressed['down'] = True
            elif e.key == pg.K_z:
                keysPressed['z'] = True
            elif e.key == pg.K_x:
                keysPressed['x'] = True
        if e.type == pg.KEYUP:
            if e.key == pg.K_LEFT:
                keysPressed['left'] = False
            elif e.key == pg.K_RIGHT:
                keysPressed['right'] = False
            elif e.key == pg.K_UP:
                keysPressed['up'] = False
            elif e.key == pg.K_DOWN:
                keysPressed['down'] = False
            elif e.key == pg.K_z:
                keysPressed['z'] = False
            elif e.key == pg.K_x:
                keysPressed['x'] = False
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

    if keysPressed['right']:
        scene[sceneSel].transform.translate += vecs.Vec3(MOVE_SPEED, 0., 0.)
    if keysPressed['left']:
        scene[sceneSel].transform.translate += vecs.Vec3(-MOVE_SPEED, 0., 0.)
    if keysPressed['up']:
        scene[sceneSel].transform.translate += vecs.Vec3(0., MOVE_SPEED, 0.)
    if keysPressed['down']:
        scene[sceneSel].transform.translate += vecs.Vec3(0., -MOVE_SPEED, 0.)
    if keysPressed['x']:
        scene[sceneSel].transform.translate += vecs.Vec3(0., 0., MOVE_SPEED)
    if keysPressed['z']:
        scene[sceneSel].transform.translate += vecs.Vec3(0., 0., -MOVE_SPEED)
