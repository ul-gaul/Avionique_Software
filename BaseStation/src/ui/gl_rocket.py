from OpenGL.GL import *
from OpenGL.GLU import *
from PyQt5 import QtCore
from PyQt5.QtWidgets import QOpenGLWidget, QSizePolicy


class GlRocket(QOpenGLWidget):
    def __init__(self, parent):
        super().__init__(parent)
        size_policy = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(size_policy)
        self.setMinimumSize(QtCore.QSize(200, 400))
        self.setObjectName("GlRocket")
        self.vertices = [(0.3, 0, 1), (0.3, 0, 0), (0.7, 0, 0.1), (0.7, 0, 0.5)]
        self.face = (0, 1, 2, 3)

    def draw_rocket(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        cm = 2  # Centre de masse. Unités à partir du bas
        glTranslatef(0, 0, -cm)
        self.draw_base()
        self.draw_fins()
        glTranslatef(0, 0, 5.5)
        self.draw_cone()
        glTranslatef(0, 0, -3.5)
        self.draw_tube()
        glTranslatef(0, 0, cm - 2)

    @staticmethod
    def draw_base():
        glColor3b(120, 120, 120)
        cyl = gluNewQuadric()
        gluQuadricNormals(cyl, GLU_SMOOTH)
        gluCylinder(cyl, 0.3, 0.3, 2.5, 50, 5)  # (obj, base radius, top radius, length, res, res)

    @staticmethod
    def draw_tube():
        glColor3b(120, 120, 120)
        cyl = gluNewQuadric()
        gluQuadricNormals(cyl, GLU_SMOOTH)
        gluCylinder(cyl, 0.3, 0.3, 3.5, 50, 5)

    def draw_fins(self):
        for i in range(3):
            self.draw_fin()
            glRotatef(120, 0, 0, 1)

    def draw_fin(self):
        glColor3b(115, 0, 0)
        glBegin(GL_QUADS)
        glTexCoord2f(0, 0)
        glVertex3f(self.vertices[self.face[0]][0], self.vertices[self.face[0]][1], self.vertices[self.face[0]][2])
        glTexCoord2f(0, 1)
        glVertex3f(self.vertices[self.face[1]][0], self.vertices[self.face[1]][1], self.vertices[self.face[1]][2])
        glTexCoord2f(1, 1)
        glVertex3f(self.vertices[self.face[2]][0], self.vertices[self.face[2]][1], self.vertices[self.face[2]][2])
        glTexCoord2f(1, 0)
        glVertex3f(self.vertices[self.face[3]][0], self.vertices[self.face[3]][1], self.vertices[self.face[3]][2])
        glEnd()

    @staticmethod
    def draw_cone():
        glColor3b(115, 0, 0)
        con = gluNewQuadric()
        gluQuadricNormals(con, GLU_SMOOTH)
        gluCylinder(con, 0.3, 0, 1.5, 50, 5)

    def rotate_rocket(self, w, x, y, z):
        glRotatef(w, x, y, z)
        self.paintGL()

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        self.draw_rocket()

        # glLoadIdentity()
        #
        # glTranslatef(-2.5, 0.5, -6.0)
        # glColor3f(1.0, 1.5, 0.0)
        # glPolygonMode(GL_FRONT, GL_FILL)
        #
        # glBegin(GL_TRIANGLES)
        # glVertex3f(2.0, -1.2, 0.0)
        # glVertex3f(2.6, 0.0, 0.0)
        # glVertex3f(2.9, -1.2, 0.0)
        # glEnd()

        glFlush()

    def initializeGL(self):
        gluPerspective(45.0, 0.5, 0.1, 50.0)
        glTranslatef(0, -1, -11)  # Point d'observation
        glRotatef(270, 1, 0, 0)

        glClearDepth(1.0)
        glDepthFunc(GL_LEQUAL)
        glEnable(GL_DEPTH_TEST)
        glShadeModel(GL_SMOOTH)

        glRotatef(0, 0, 1, 0)
