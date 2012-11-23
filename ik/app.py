from __future__ import division

import pygtk
pygtk.require('2.0')
import gtk

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import time
import threading
import math

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

    def __init__(self, px, py, pz):
        self.initialized = True
        self.set_position(px, py, pz)

    def set_position(self, x=None, y=None, z=None):
        if x is None and y is None and z is None:
            raise Exception('x, y or z parameters are required')

        if x is not None:
            self.x = x
        if y is not None:
            self.y = y
        if z is not None:
            self.z = z

        self.theta1, self.theta2, self.theta3 = self.ik(self.x, self.y, self.z)

    def set_position_rel(self, x=0, y=0, z=0):
        self.x, self.y, self.z = self.x + x, self.y + y, self.z + z
        self.theta1, self.theta2, self.theta3 = self.ik(self.x, self.y, self.z)

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

def loopseq(s):
    i = 0
    while 1:
        if i >= len(s):
            i = 0
        yield s[i]
        i += 1

class Bot(object):
    def __init__(self):
        self.initialized = True

        self.axesxl = 160.1
        self.axesyl = 108.1

        self.x = 0
        self.y = 0
        self.z = 130

        self.dz = -0.5

        self.legseq = loopseq([2, 0, 1, 3])

        self.legs = [
            Manipulator(0, -110, -130),
            Manipulator(0, -110, -130),
            Manipulator(0, -110, -130),
            Manipulator(0, -110, -130),
        ]
        self.legsigns = [1, -1, -1, 1]

        self.leg_param = 0
        self.leg_dp = 0.005

        self.leg_paramx = 0
        self.leg_paramz = 0
        self.current_leg = next(self.legseq)
        self.step_count = 0

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
        self.legs[0].display()
        glPopMatrix()

        glPushMatrix()
        glTranslate(x, -y, 0)
        glFrontFace(GL_CCW)
        self.legs[1].display()
        glPopMatrix()

        glPushMatrix()
        glTranslate(x, y, 0)
        glScale(1, -1, 1)
        glFrontFace(GL_CW)
        self.legs[2].display()
        glPopMatrix()

        glPushMatrix()
        glTranslate(-x, y, 0)
        glRotate(180, 0, 0, 1)
        glFrontFace(GL_CCW)
        self.legs[3].display()
        glPopMatrix()

        glDisable(GL_LIGHT1)
        glDisable(GL_LIGHT0)
        glDisable(GL_LIGHTING)
        glPopMatrix()

    def update(self):
        self.raise_leg()
        pass

    def raise_leg(self):
        if self.leg_param > 1:
            self.leg_param = 0
            self.current_leg = next(self.legseq)
            self.leg_paramx = 0
            self.leg_paramz = 0
            self.step_count += 1

        if self.step_count < 4:
            body_x = 30
            self.x += body_x * self.leg_dp
            self.legs[0].set_position_rel(x=body_x * self.leg_dp)
            self.legs[1].set_position_rel(x=-body_x * self.leg_dp)
            self.legs[2].set_position_rel(x=-body_x * self.leg_dp)
            self.legs[3].set_position_rel(x=body_x * self.leg_dp)

            x = round(self.leg_param * 100, 2)
            z = round(math.sin(math.pi * self.leg_param) * 10, 2)
            self.legs[self.current_leg].set_position_rel(x=(x - self.leg_paramx) * -self.legsigns[self.current_leg],
                                                         z=z - self.leg_paramz)
            self.leg_paramx = x
            self.leg_paramz = z

            self.leg_param += self.leg_dp

    def bounce(self, zmin, zmax):
        self.z += self.dz
        if self.z < zmin or self.z >= zmax:
            self.dz = -self.dz

        for leg in self.legs:
            leg.set_position(z=-self.z)


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

