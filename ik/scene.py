from __future__ import division

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import pygtk
pygtk.require('2.0')
import gtk
from gtk.gtkgl.apputils import GLArea, GLScene, GLSceneButton, GLSceneButtonMotion

from views import ViewOrtho, ViewPerspective

class SceneArea(GLArea):
    """
    Extend GLScene to provide mouse wheel support.
    """
    def __init__(self, *args, **kwargs):
        super(SceneArea, self).__init__(*args, **kwargs)

        self.connect('scroll-event', self.glscene.wheel_scroll)
        self.add_events(gtk.gdk.SCROLL_MASK)


class Scene(GLScene, GLSceneButton, GLSceneButtonMotion):
    PAN_SPEED    = 25
    ROTATE_SPEED = 25

    def __init__(self):
        super(Scene, self).__init__(gtk.gdkgl.MODE_RGB |
                                    gtk.gdkgl.MODE_DEPTH |
                                    gtk.gdkgl.MODE_DOUBLE)
        self.model    = None
        self.actors   = []
        self.cursor_x = 0
        self.cursor_y = 0

        self.view_ortho = ViewOrtho()
        self.view_perspective = ViewPerspective()
        self.current_view = self.view_perspective

        self.initialized = False

    def add_actor(self, actor):
        self.actors.append(actor)

    def clear(self):
        self.actors = []

    def is_initialized(self):
        return self.glarea.window is not None

    # ------------------------------------------------------------------------
    # DRAWING
    # ------------------------------------------------------------------------

    def init(self):
        glClearColor(0.0, 0.0, 0.0, 0.0) # set clear color to black
        glClearDepth(1.0)                # set depth value to 1
        glDepthFunc(GL_LEQUAL)

        glEnable(GL_COLOR_MATERIAL)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_CULL_FACE)
        # simulate translucency by blending colors
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        self.init_actors()
        self.initialized = True

    def init_actors(self):
        for actor in self.actors:
            if not actor.initialized:
                actor.init()

    def display(self, w, h):
        # clear the color and depth buffers from any leftover junk
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # discard back-facing polygons
        glCullFace(GL_BACK)

        # fix normals after scaling to prevent problems with lighting
        # see: http://www.opengl.org/resources/faq/technical/lights.htm#ligh0090
        glEnable(GL_RESCALE_NORMAL)

        self.view_ortho.begin(w, h)
        self.draw_axes()
        self.view_ortho.end()

        self.current_view.begin(w, h)
        self.current_view.display_transform()
        for actor in self.actors:
            actor.display()
        self.current_view.end()

    def reshape(self, w, h):
        glViewport(0, 0, w, h)

    def draw_axes(self, length=50.0):
        glPushMatrix()
        self.current_view.ui_transform(length)

        axes = [
            (length, 0.0, 0.0),
            (0.0, length, 0.0),
            (0.0, 0.0, length),
        ]
        colors = [
            (1.0, 0.0, 0.0),
            (0.0, 1.0, 0.0),
            (0, 0x8a/255, 1.0),
        ]
        labels = ['x', 'y', 'z']

        glBegin(GL_LINES)

        for axis, color in zip(axes, colors):
            glColor(*color)
            glVertex(0.0, 0.0, 0.0)
            glVertex(*axis)

        glEnd()

        # draw axis labels
        glutInit()

        for label, axis, color in zip(labels, axes, colors):
            glColor(*color)
            # add padding to labels
            glRasterPos(axis[0] + 2, axis[1] + 2, axis[2] + 2)
            glutBitmapCharacter(GLUT_BITMAP_8_BY_13, ord(label));

        glPopMatrix()

    # ------------------------------------------------------------------------
    # VIEWING MANIPULATIONS
    # ------------------------------------------------------------------------

    def button_press(self, width, height, event):
        self.cursor_x = event.x
        self.cursor_y = event.y

    def button_release(self, width, height, event):
        pass

    def button_motion(self, width, height, event):
        delta_x = event.x - self.cursor_x
        delta_y = event.y - self.cursor_y

        if event.state & gtk.gdk.BUTTON1_MASK: # left mouse button
            self.current_view.rotate(delta_x * self.ROTATE_SPEED / 100,
                                     delta_y * self.ROTATE_SPEED / 100)
        elif event.state & gtk.gdk.BUTTON2_MASK: # middle mouse button
            if hasattr(self.current_view, 'offset'):
                self.current_view.offset(delta_x * self.PAN_SPEED / 100,
                                         delta_y * self.PAN_SPEED / 100)
        elif event.state & gtk.gdk.BUTTON3_MASK: # right mouse button
            self.current_view.pan(delta_x * self.PAN_SPEED / 100,
                                  delta_y * self.PAN_SPEED / 100)

        self.cursor_x = event.x
        self.cursor_y = event.y

        self.invalidate()

    def wheel_scroll(self, widget, event):
        delta_y = 30.0
        if event.direction == gtk.gdk.SCROLL_DOWN:
            delta_y = -delta_y

        self.current_view.zoom(0, delta_y)
        self.invalidate()

    def reset_view(self, both=False):
        if both:
            self.view_ortho.reset_state()
            self.view_perspective.reset_state()
        else:
            self.current_view.reset_state()

    def rotate_view(self, azimuth, elevation):
        self.current_view.azimuth = azimuth
        self.current_view.elevation = elevation
        self.invalidate()
