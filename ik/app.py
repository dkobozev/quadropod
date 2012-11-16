from __future__ import division

import pygtk
pygtk.require('2.0')
import gtk

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from scene import SceneArea, Scene


class Manipulator(object):
    def __init__(self):
        self.initialized = True
        self.alpha1 = 0;
        self.a1     = 0;
        self.d1     = -30;

        self.alpha2 = -90;
        self.a2     = 27.5;
        self.d2     = 43;

        self.alpha3 = 0;
        self.a3     = 57.3;
        self.d3     = -18;

        self.alpha4 = 90;
        self.a4     = 106;
        self.d4     = 0;

        self.theta1 = 0
        self.theta2 = -30
        self.theta3 = 60

    def display(self):
        glPushMatrix()

        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glEnable(GL_LIGHT1)
        glEnable(GL_NORMALIZE)
        glShadeModel(GL_SMOOTH)

        # material properties (white plastic)
        glMaterial(GL_FRONT, GL_AMBIENT, (0.0, 0.0, 0.0, 1.0))
        glMaterial(GL_FRONT, GL_DIFFUSE, (0.55, 0.55, 0.55, 1.0))
        glMaterial(GL_FRONT, GL_SPECULAR, (0.7, 0.7, 0.7, 1.0))
        glMaterial(GL_FRONT, GL_SHININESS, 32.0)

        # lights properties
        glLight(GL_LIGHT0, GL_AMBIENT, (0.3, 0.3, 0.3, 1.0))
        glLight(GL_LIGHT0, GL_DIFFUSE, (0.3, 0.3, 0.3, 1.0))
        glLight(GL_LIGHT1, GL_DIFFUSE, (0.3, 0.3, 0.3, 1.0))

        # lights position
        glLightfv(GL_LIGHT0, GL_POSITION, (20, 20, 20))
        glLightfv(GL_LIGHT1, GL_POSITION, (-20.0, -20.0, 20.0))

        glColor(1.0, .0, .0)

        self.draw_joint(self.alpha1, self.a1, self.a2, self.theta1, self.d1)
        self.draw_joint(self.alpha2, self.a2, self.a3, self.theta2, self.d2)
        self.draw_joint(self.alpha3, self.a3, self.a4, self.theta3, self.d3)
        self.draw_joint(self.alpha4, self.a4, 0,       0,           self.d4)

        glDisable(GL_LIGHT1)
        glDisable(GL_LIGHT0)
        glDisable(GL_LIGHTING)
        glPopMatrix()

    def draw_joint(self, alpha, a1, a2, theta, d):
        glRotate(alpha, 1.0, .0, .0)
        glTranslate(a1, .0, .0)
        glRotate(theta, .0, .0, .1)
        glTranslate(.0, .0, d)

        glutSolidCone(9, 15, 30, 30)

        if a2 != 0:
            glPushMatrix()
            glRotate(90, 0, 1, 0)
            glColor(1.0, 1.0, 1.0)
            gluCylinder(gluNewQuadric(), 1, 1, a2, 30, 30)
            glPopMatrix()

        if d != 0:
            glPushMatrix()
            glColor(0xfa/255, 0xdd/255, 0x5a/255)
            glScale(1.5, 1.5, -d)
            glTranslate(0, 0, .5)
            glutSolidCube(1.0)
            glPopMatrix()

        glColor(1.0, .0, .0)


class App(object):

    def __init__(self):
        manipulator = Manipulator()

        self.scene = Scene()
        self.scene.add_actor(manipulator)

        glarea = SceneArea(self.scene)

        self.window = gtk.Window()
        self.window.set_position(gtk.WIN_POS_CENTER)
        self.window.set_default_size(640, 480)
        self.window.add(glarea)

        self.window.connect('destroy', self.quit)

    def show_window(self):
        self.window.show_all()

    def quit(self, event):
        gtk.main_quit()

if __name__ == '__main__':
    app = App()
    app.show_window()
    gtk.main()

