from OpenGL.GL import *
from OpenGL.GLU import *
from PyQt5 import QtCore
from PyQt5.QtWidgets import QOpenGLWidget

from src.ui.utils import set_minimum_expanding_size_policy

from src.data_processing.quaternion import Quaternion


class GlRocket(QOpenGLWidget):
    def __init__(self, parent):
        super().__init__(parent)
        set_minimum_expanding_size_policy(self)
        self.setMinimumSize(QtCore.QSize(200, 400))
        self.setObjectName("GlRocket")
        self.fin_vertices = [(0.3, 0, 1), (0.3, 0, 0), (0.7, 0, 0.1), (0.7, 0, 0.5)]
        self._rocket_orientation = (0, 0, 0, 0)

    def draw_rocket(self):
        cm = 2  # Centre de masse. Unités à partir du bas
        glTranslatef(0, 0, -cm)
        self.draw_tube()
        self.draw_fins()
        glTranslatef(0, 0, 5.5)
        self.draw_cone()
        glTranslatef(0, 0, -5.5 + cm)

    @staticmethod
    def draw_tube():
        glColor3b(120, 120, 120)
        cyl = gluNewQuadric()
        gluQuadricNormals(cyl, GLU_SMOOTH)
        gluCylinder(cyl, 0.3, 0.3, 5.5, 50, 5)  # (obj, base radius, top radius, length, res, res)

    def draw_fins(self):
        glColor3b(115, 0, 0)
        for i in range(3):
            self.draw_fin()
            glRotatef(120, 0, 0, 1)

    def draw_fin(self):
        glBegin(GL_QUADS)
        glTexCoord2f(0, 0)
        glVertex3f(self.fin_vertices[0][0], self.fin_vertices[0][1], self.fin_vertices[0][2])
        glTexCoord2f(0, 1)
        glVertex3f(self.fin_vertices[1][0], self.fin_vertices[1][1], self.fin_vertices[1][2])
        glTexCoord2f(1, 1)
        glVertex3f(self.fin_vertices[2][0], self.fin_vertices[2][1], self.fin_vertices[2][2])
        glTexCoord2f(1, 0)
        glVertex3f(self.fin_vertices[3][0], self.fin_vertices[3][1], self.fin_vertices[3][2])
        glEnd()

    @staticmethod
    def draw_cone():
        glColor3b(115, 0, 0)
        con = gluNewQuadric()
        gluQuadricNormals(con, GLU_SMOOTH)
        gluCylinder(con, 0.3, 0, 1.5, 50, 5)

    def set_rocket_rotation(self, rot: Quaternion):
        self._rocket_orientation = (rot.w, rot.x, rot.y, rot.z)
        self.update()

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()
        glRotatef(self._rocket_orientation[0], self._rocket_orientation[1], self._rocket_orientation[2],
                  self._rocket_orientation[3])
        self.draw_rocket()
        glPopMatrix()
        glFlush()

    def initializeGL(self):
        glMatrixMode(GL_PROJECTION)
        gluPerspective(45.0, 0.5, 0.1, 50.0)
        glTranslatef(0, -1, -11)  # Point d'observation
        glRotatef(270, 1, 0, 0)

        glClearDepth(1.0)
        glDepthFunc(GL_LEQUAL)
        glEnable(GL_DEPTH_TEST)
        glShadeModel(GL_SMOOTH)
