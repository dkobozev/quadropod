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
        self.param_stack = []
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

    def push_params(self):
        self.param_stack.append((self.x, self.y, self.z, ))

    def pop_params(self):
        try:
            x, y, z = self.param_stack.pop()
            self.set_position(x, y, z)
            return True
        except IndexError:
            return False

    def __str__(self):
        return "Manipulator(%s, %s, %s) => [%s, %s, %s]" % (self.x, self.y, self.z,
                self.theta1, self.theta2, self.theta3)

    def __repr__(self):
        return "Manipulator(%s, %s, %s)" % (self.x, self.y, self.z)

def loopseq(s):
    i = 0
    while 1:
        if i >= len(s):
            i = 0
        yield s[i]
        i += 1

class Bot(object):
    T_MAX = 100
    T_INC = 1

    def __init__(self):
        """
        good parameters:

        * z = 160, lx = 30, ly = 80, dbody = 30
        * z = 160, lx = 30, ly = 60, dbody = 30
        * z = 120, lx = 60, ly = 80, dbody = ?

        """
        self.initialized = True

        self.axesxl = 160.1
        self.axesyl = 108.1

        self.x = 0
        self.y = 0
        self.z = 120

        self.dz = -0.5 # bounce only

        lx = 50
        ly = 76
        self.legs = [
            Manipulator(lx, -ly, -self.z),
            Manipulator(lx, -ly, -self.z),
            Manipulator(lx, -ly, -self.z),
            Manipulator(lx, -ly, -self.z),
        ]
        self.legsigns = [1, -1, -1, 1]

        self.param_stack = []
        self.move_count = 0
        self.t = 0

        # init moves
        self.moves = []

        self.moves.append((self.create_move_xy, (30, 30)))
        self.moves.append((self.create_raise_leg, (0, 45, 30)))
        self.moves.append((self.create_lower_leg, (0, 45, 30)))
        self.moves.append((self.create_raise_leg, (1, 45, 30)))
        self.moves.append((self.create_lower_leg, (1, 45, 30)))
        self.moves.append((self.create_move_xy, (30, -60)))
        self.moves.append((self.create_raise_leg, (3, 45, 30)))
        self.moves.append((self.create_lower_leg, (3, 45, 30)))
        self.moves.append((self.create_raise_leg, (2, 45, 30)))
        self.moves.append((self.create_lower_leg, (2, 45, 30)))
        self.moves.append((self.create_move_xy, (30, 30)))

        self.moves.append((self.create_move_xy, (30, 30)))
        self.moves.append((self.create_raise_leg, (0, 45, 30)))
        self.moves.append((self.create_lower_leg, (0, 45, 30)))
        self.moves.append((self.create_raise_leg, (1, 45, 30)))
        self.moves.append((self.create_lower_leg, (1, 45, 30)))
        self.moves.append((self.create_move_xy, (30, -60)))
        self.moves.append((self.create_raise_leg, (3, 45, 30)))
        self.moves.append((self.create_lower_leg, (3, 45, 30)))
        self.moves.append((self.create_raise_leg, (2, 45, 30)))
        self.moves.append((self.create_lower_leg, (2, 45, 30)))
        self.moves.append((self.create_move_xy, (30, 30)))

        self.moves.append((self.create_move_xy, (30, 30)))
        self.moves.append((self.create_raise_leg, (0, 45, 30)))
        self.moves.append((self.create_lower_leg, (0, 45, 30)))
        self.moves.append((self.create_raise_leg, (1, 45, 30)))
        self.moves.append((self.create_lower_leg, (1, 45, 30)))
        self.moves.append((self.create_move_xy, (30, -60)))
        self.moves.append((self.create_raise_leg, (3, 45, 30)))
        self.moves.append((self.create_lower_leg, (3, 45, 30)))
        self.moves.append((self.create_raise_leg, (2, 45, 30)))
        self.moves.append((self.create_lower_leg, (2, 45, 30)))
        self.moves.append((self.create_move_xy, (30, 30)))

        self.moves.append((self.create_move_xy, (30, 30)))
        self.moves.append((self.create_raise_leg, (0, 45, 30)))
        self.moves.append((self.create_lower_leg, (0, 45, 30)))
        self.moves.append((self.create_raise_leg, (1, 45, 30)))
        self.moves.append((self.create_lower_leg, (1, 45, 30)))
        self.moves.append((self.create_move_xy, (30, -60)))
        self.moves.append((self.create_raise_leg, (3, 45, 30)))
        self.moves.append((self.create_lower_leg, (3, 45, 30)))
        self.moves.append((self.create_raise_leg, (2, 45, 30)))
        self.moves.append((self.create_lower_leg, (2, 45, 30)))
        self.moves.append((self.create_move_xy, (30, 30)))
        #self.moves.append((self.create_move_xy, (-30, -40)))
        #self.moves.append((self.create_raise_leg, (2, 20, 30)))
        #self.moves.append((self.create_lower_leg, (2, 20, 30)))

        #self.moves.append((self.create_move_xy, (30, 0)))
        #self.moves.append((self.create_raise_leg, (2, 30, 20)))

        # prepare the first move
        try:
            self.next_move(reset=True)
        except StopIteration:
            self.move = None

    def create_move_xy(self, dx, dy):
        botx = self.x
        boty = self.y
        leg0x = self.legs[0].x
        leg1x = self.legs[1].x
        leg2x = self.legs[2].x
        leg3x = self.legs[3].x

        leg0y = self.legs[0].y
        leg1y = self.legs[1].y
        leg2y = self.legs[2].y
        leg3y = self.legs[3].y
        def move(t):
            self.x = botx + dx*t
            self.y = boty + dy*t
            self.legs[0].set_position(x=leg0x + dx*t, y=leg0y - dy*t)
            self.legs[1].set_position(x=leg1x - dx*t, y=leg1y - dy*t)
            self.legs[2].set_position(x=leg2x - dx*t, y=leg2y + dy*t)
            self.legs[3].set_position(x=leg3x + dx*t, y=leg3y + dy*t)
        return move

    def create_raise_leg(self, idx, d, h):
        legx = self.legs[idx].x
        legz = self.legs[idx].z
        def move(t):
            x = round(t * d, 2)
            z = round(math.sin(math.pi/2 * t) * h, 2)
            self.legs[idx].set_position(x=legx + x * -self.legsigns[idx],
                                        z=legz + z)
        return move

    def create_lower_leg(self, idx, d, h):
        legx = self.legs[idx].x
        legz = self.legs[idx].z
        def move(t):
            x = round(t * d, 2)
            z = round((math.sin(math.pi/2 + math.pi/2 * t) - 1) * h, 2)
            self.legs[idx].set_position(x=legx + x * -self.legsigns[idx],
                                        z=legz + z)
        return move

    def create_move_w_raise(self, dx, dy, leg_idx, leg_d, leg_h):
        body = self.create_move_xy(dx, dy)
        leg = self.create_raise_leg(leg_idx, leg_d, leg_h)
        def move(t):
            body(t)
            leg(t)
        return move

    def bounce(self, zmin, zmax):
        self.z += self.dz
        if self.z < zmin or self.z >= zmax:
            self.dz = -self.dz

        for leg in self.legs:
            leg.set_position(z=-self.z)

    def push_params(self):
        self.param_stack.append((self.x, self.y, self.z, ))
        for leg in self.legs:
            leg.push_params()

    def pop_params(self):
        try:
            self.x, self.y, self.z = self.param_stack.pop()
            success = True
        except IndexError:
            success = False
        for leg in self.legs:
            leg.pop_params()
        return success

    def prev_move(self):
        self.pop_params()
        self.push_params()
        current_move = self.move_count
        if current_move > 0:
            self.t = self.T_MAX
            self.next_move(reset=True)
            self.update(animate=False)
            while self.move_count < current_move - 1:
                self.next_move()
                self.update(False)
            self.t = 0

    def next_move(self, reset=False):
        if reset:
            self.move_count = 0
            self.move_generator = iter(range(len(self.moves)))
        move, params = self.moves[next(self.move_generator)]
        self.move = move(*params)
        if not reset:
            self.move_count += 1

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

        glColor(0.0, 0.0, 1.0, 1.0)
        glRotate(180, 0, 1, 0)
        gluCylinder(gluNewQuadric(), 2, 2, self.z, 30, 30)
        glRotate(180, 0, 1, 0)

        # robot body approximation
        glColor(1.0, 0.0, 0.0, 1)
        glutSolidSphere(3, 100, 100)
        glColor(0.0, 0.0, 0.0, 0.5)
        glBegin(GL_POLYGON)
        glVertex(- self.axesxl/2, - self.axesyl/2, 0)
        glVertex(+ self.axesxl/2, - self.axesyl/2, 0)
        glVertex(+ self.axesxl/2, + self.axesyl/2, 0)
        glVertex(- self.axesxl/2, + self.axesyl/2, 0)
        glEnd()

        # legs
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

        # draw drop shadow
        shadow_v = []
        if round(abs(self.legs[0].z), 2) == round(self.z):
            shadow_v.append((-x - self.legs[0].x, -y + self.legs[0].y, self.legs[0].z + 1))
        if round(abs(self.legs[1].z), 2) == round(self.z):
            shadow_v.append((x + self.legs[1].x, -y + self.legs[1].y, self.legs[1].z + 1))
        if round(abs(self.legs[2].z), 2) == round(self.z):
            shadow_v.append((x + self.legs[2].x, y - self.legs[2].y, self.legs[2].z + 1))
        if round(abs(self.legs[3].z), 2) == round(self.z):
            shadow_v.append((-x - self.legs[3].x, y - self.legs[3].y, self.legs[3].z + 1))

        glColor(1.0, 0.0, 0.0, 0.5)
        glBegin(GL_POLYGON)
        for vx, vy, vz in shadow_v:
            glVertex(vx, vy, vz)
        glEnd()

        # draw the centroid of a triangle formed by three legs touching the ground
        if len(shadow_v) == 3:
            cx = 0.33 * (shadow_v[0][0] + shadow_v[1][0] + shadow_v[2][0])
            cy = 0.33 * (shadow_v[0][1] + shadow_v[1][1] + shadow_v[2][1])
            cz = shadow_v[0][2]
            glTranslate(cx, cy, cz)
            glutSolidSphere(3, 100, 100)

        glDisable(GL_LIGHT1)
        glDisable(GL_LIGHT0)
        glDisable(GL_LIGHTING)
        glPopMatrix()

    def update(self, animate=True):
        if self.t > self.T_MAX:
            self.t = 0
            for leg in self.legs:
                print (leg)
            self.next_move()

        if self.move is not None:
            self.move(self.t / self.T_MAX)

        if animate:
            self.t += self.T_INC


class Ground(object):
    def __init__(self, lx, ly):
        self.lx = lx
        self.ly = ly

        self.initialized = False

    def init(self):
        self.display_list = compile_display_list(self.draw)
        self.initialized = True

    def draw(self):
        glPushMatrix()

        # use polygon offset to push the rectangle back and draw lines on top
        # see: # http://www.opengl.org/archives/resources/faq/technical/polygonoffset.htm
        glEnable(GL_POLYGON_OFFSET_FILL)
        glPolygonOffset(1.0, 1.0)

        glClearColor(0xaa/255, 0xf4/255, 0xf3/255, 0.0)
        glTranslate(-self.lx/2, -self.ly/2, 0)
        glColor(0x4d/255, 0x79/255, 0x42/255)
        glRectf(0.0, 0.0, float(self.lx), float(self.ly))

        glDisable(GL_POLYGON_OFFSET_FILL)

        glBegin(GL_LINES)
        for p in range(0, self.lx, 10):
            if p % 50 == 0:
                glColor(1.0, 1.0, 1.0, 0.5)
            else:
                glColor(0.6, 0.6, 0.6, 0.5)
            glVertex(p, 0, 0.01)
            glVertex(p, self.ly, 0.01)

        for p in range(0, self.ly, 10):
            if p % 50 == 0:
                glColor(1.0, 1.0, 1.0, 0.5)
            else:
                glColor(0.6, 0.6, 0.6, 0.5)
            glVertex(0, p, 0.01)
            glVertex(self.lx, p, 0.01)
        glEnd()

        glPopMatrix()

    def display(self):
        glCallList(self.display_list)


class App(object):

    def __init__(self):
        self.bot = Bot()
        self.bot.push_params()

        self.ground = Ground(5000, 5000)

        self.scene = Scene()
        self.scene.add_actor(self.ground)
        self.scene.add_actor(self.bot)

        glarea = SceneArea(self.scene)

        self.btn_play = gtk.Button('Pause')
        self.btn_rewind = gtk.Button('Rewind')
        self.btn_prev_move = gtk.Button('Prev move')
        self.btn_next_move = gtk.Button('Next move')
        self.btn_top = gtk.Button('Top')
        self.btn_quit = gtk.Button('Quit')

        self.chk_loop = gtk.CheckButton('Loop')
        self.chk_loop.set_active(False)

        self.chk_ortho = gtk.CheckButton('Ortho')
        self.chk_ortho.set_active(False)

        self.entry_move = gtk.Entry()
        self.entry_move.set_text(str(self.bot.move_count))

        control_box = gtk.HBox()
        control_box.set_border_width(5)
        control_box.pack_start(self.btn_play)
        control_box.pack_start(self.btn_rewind)
        control_box.pack_start(self.btn_prev_move)
        control_box.pack_start(self.btn_next_move)
        control_box.pack_start(self.btn_top)
        control_box.pack_start(self.btn_quit)

        control_box2 = gtk.HBox()
        control_box2.set_border_width(5)
        control_box2.pack_start(self.chk_loop)
        control_box2.pack_start(self.chk_ortho)
        control_box2.pack_start(self.entry_move)

        vbox = gtk.VBox()
        vbox.pack_start(glarea)
        vbox.pack_start(control_box, expand=False, fill=False)
        vbox.pack_start(control_box2, expand=False, fill=False)

        self.window = gtk.Window()
        self.window.set_position(gtk.WIN_POS_CENTER)
        self.window.set_default_size(640, 480)
        self.window.add(vbox)

        self.window.connect('destroy', self.quit)
        self.btn_play.connect('clicked', self.play)
        self.btn_rewind.connect('clicked', self.rewind)
        self.btn_prev_move.connect('clicked', self.prev_move)
        self.btn_next_move.connect('clicked', self.next_move)
        self.btn_top.connect('clicked', self.view_top)
        self.btn_quit.connect('clicked', self.quit)

        self.chk_loop.connect('toggled', self.toggle_loop)
        self.chk_ortho.connect('toggled', self.toggle_ortho)

        self.play = True
        self.loop = False
        self.ortho = False

        gtk.gdk.threads_init()
        self.thread = threading.Thread(target=self.mainloop)
        self.thread.daemon = True
        self.thread.start()

    def show_window(self):
        self.window.show_all()

    def quit(self, event):
        gtk.main_quit()

    def play(self, event):
        self.play = not self.play
        self.update_play_button()

    def update_play_button(self):
        if self.play:
            self.btn_play.set_label('Pause')
        else:
            self.btn_play.set_label('Play')

    def rewind(self, event):
        self.play = False
        self.update_play_button()
        self.reset_bot()
        self.entry_move.set_text(str(self.bot.move_count))

    def prev_move(self, event):
        self.bot.prev_move()
        self.entry_move.set_text(str(self.bot.move_count))

    def next_move(self, event):
        # finish the current move
        self.bot.t = Bot.T_MAX
        self.bot.update(animate=False)
        try:
            self.bot.next_move()
        except StopIteration:
            pass
        self.bot.t = 0
        self.entry_move.set_text(str(self.bot.move_count))

    def toggle_loop(self, widget):
        self.loop = widget.get_active()

    def toggle_ortho(self, widget):
        self.ortho = widget.get_active()
        if self.ortho:
            self.scene.set_ortho()
        else:
            self.scene.set_perspective()

    def reset_bot(self):
        while self.bot.pop_params():
            pass # empty the stack
        self.bot.push_params()
        self.bot.t = 0
        self.bot.next_move(reset=True)

    def view_top(self, event):
        self.scene.rotate_view(90, -90)

    def mainloop(self):
        time.sleep(1)
        while True:
            try:
                move = self.bot.move_count
                self.bot.update(self.play)
                if self.bot.move_count != move:
                    self.entry_move.set_text(str(self.bot.move_count))
            except StopIteration:
                self.play = self.loop
                self.update_play_button()
                self.bot.t = Bot.T_MAX
                #self.reset_bot()

            self.scene.invalidate()
            time.sleep(.01)


if __name__ == '__main__':
    app = App()
    app.show_window()
    gtk.main()

