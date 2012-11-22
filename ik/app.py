from __future__ import division

import pygtk
pygtk.require('2.0')
import gtk

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import time
import threading

from scene import SceneArea, Scene
from iksolve import ik

def compile_display_list(func, *options):
    display_list = glGenLists(1)
    glNewList(display_list, GL_COMPILE)
    func(*options)
    glEndList()
    return display_list

class Manipulator(object):
    alpha1 = 0;
    a1     = 0;
    d1     = -30;

    alpha2 = -90;
    a2     = 27.5;
    d2     = 43;

    alpha3 = 0;
    a3     = 57.3;
    d3     = -18;

    alpha4 = 90;
    a4     = 106;
    d4     = 0;

    def __init__(self, theta1=0, theta2=0, theta3=0):
        self.initialized = True
        self.theta1 = theta1
        self.theta2 = theta2
        self.theta3 = theta3

    def display(self):
        glPushMatrix()
        glColor(1.0, .0, .0)

        self.draw_joint(self.alpha1, self.a1, self.a2, self.theta1, self.d1)
        self.draw_joint(self.alpha2, self.a2, self.a3, self.theta2, self.d2)
        self.draw_joint(self.alpha3, self.a3, self.a4, self.theta3, self.d3)
        self.draw_joint(self.alpha4, self.a4, 0,       0,           self.d4, True)

        glPopMatrix()

    def draw_joint(self, alpha, a1, a2, theta, d, end=False):
        glRotate(alpha, 1.0, .0, .0)
        glTranslate(a1, .0, .0)
        glRotate(theta, .0, .0, .1)
        glTranslate(.0, .0, d)

        if not end:
            glutSolidCone(9, 15, 30, 30)
        else:
            glutSolidSphere(3, 100, 100)

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

    @staticmethod
    def ik(x, y, z):
        return ik(x, y, z, Manipulator.a1, Manipulator.a2, Manipulator.a3,
                  Manipulator.a4, Manipulator.d1, Manipulator.d2, Manipulator.d3)

class Bot(object):
    def __init__(self):
        self.initialized = True

        self.x = 0
        self.y = 0
        self.z = 130
        self.dz = -1

        self.axesxl = 160.1
        self.axesyl = 108.1

        theta1, theta2, theta3 = Manipulator.ik(80, -80, -130)
        print theta1, theta2, theta3

        self.bl = Manipulator(theta1, theta2, theta3)
        self.fl = Manipulator(theta1, theta2, theta3)
        self.fr = Manipulator(theta1, theta2, theta3)
        self.br = Manipulator(theta1, theta2, theta3)

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

        glTranslate(self.x, self.y, self.z)

        x, y = self.axesxl / 2, self.axesyl / 2

        glPushMatrix()
        glTranslate(-x, -y, 0)
        glRotate(180, 0, 0, 1)
        glScale(1, -1, 1)
        glFrontFace(GL_CW)
        self.bl.display()
        glPopMatrix()

        glPushMatrix()
        glTranslate(x, -y, 0)
        glFrontFace(GL_CCW)
        self.fl.display()
        glPopMatrix()

        glPushMatrix()
        glTranslate(x, y, 0)
        glScale(1, -1, 1)
        glFrontFace(GL_CW)
        self.fr.display()
        glPopMatrix()

        glPushMatrix()
        glTranslate(-x, y, 0)
        glRotate(180, 0, 0, 1)
        glFrontFace(GL_CCW)
        self.br.display()
        glPopMatrix()

        glDisable(GL_LIGHT1)
        glDisable(GL_LIGHT0)
        glDisable(GL_LIGHTING)
        glPopMatrix()

    def update(self):
        self.z += self.dz
        if self.z < 100 or self.z > 170:
            self.dz = -self.dz
        theta1, theta2, theta3 = Manipulator.ik(80, -80, -self.z)

        self.br.theta1 = theta1
        self.br.theta2 = theta2
        self.br.theta3 = theta3

        self.fr.theta1 = theta1
        self.fr.theta2 = theta2
        self.fr.theta3 = theta3

        self.fl.theta1 = theta1
        self.fl.theta2 = theta2
        self.fl.theta3 = theta3

        self.bl.theta1 = theta1
        self.bl.theta2 = theta2
        self.bl.theta3 = theta3

class Ground(object):
    def __init__(self, lx, ly):
        self.lx = lx
        self.ly = ly

        self.initialized = True

    def display(self):
        glPushMatrix()
        glClearColor(0xaa/255, 0xf4/255, 0xf3/255, 0.0)
        glTranslate(-self.lx/2, -self.ly/2, 0)
        glColor(0x4d/255, 0x79/255, 0x42/255)
        glRectf(0.0, 0.0, float(self.lx), float(self.ly))
        glPopMatrix()


class App(object):

    def __init__(self):
        self.bot = Bot()
        self.ground = Ground(100000, 100000)

        self.scene = Scene()
        self.scene.add_actor(self.ground)
        self.scene.add_actor(self.bot)

        glarea = SceneArea(self.scene)

        self.window = gtk.Window()
        self.window.set_position(gtk.WIN_POS_CENTER)
        self.window.set_default_size(640, 480)
        self.window.add(glarea)

        self.window.connect('destroy', self.quit)

        gtk.gdk.threads_init()
        self.thread = threading.Thread(target=self.mainloop)
        self.thread.daemon = True
        self.thread.start()

    def show_window(self):
        self.window.show_all()

    def quit(self, event):
        gtk.main_quit()

    def mainloop(self):
        time.sleep(1)
        while True:
            self.bot.update()
            self.scene.invalidate()
            time.sleep(.01)


if __name__ == '__main__':
    app = App()
    app.show_window()
    gtk.main()

