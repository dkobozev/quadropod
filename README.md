quadropod
=========

An Arduino-based four-legged robot.

Hardware
--------

All parts were ordered from Lynxmotion (SKU in parentheses).

* Lynxmotion Tibias 4.25" (ASBT-02)
* Lynxmotion Aluminum "C" Servo Brackets with Ball Bearings (ASB-09)
* Lynxmotion Aluminum Multi-Purpose Servo Brackets (ASB-04)
* Hitec HS-485HB servos with Metal Servo Horns (SCD-01)
* Quadrapod Body Kit - Mini (QBK-01)
* Aluminum "L" Connector Brackets (ASB-06)
* BotBoarduino (BBU-01)
* 6.0 Volt Ni-MH 2800mAh Battery Pack (BAT-05)
* Wiring Harness (WH-01)

Firmware
--------

Robot firmware is written in C for the Arduino-based BotBoarduino board and
uses a custom Makefile to link, compile and upload the firmware. All robot
movements were first simulated in software, then translated into C from Python.

Software
--------

Inverse kinematics simulation in 3D, using Python, PyGTK and PyOpenGL.
Simulator dependencies:

* Python 2.6+ (http://www.python.org/)
* PyGTK 2.24 (http://www.pygtk.org/index.html)
* PyOpenGL (http://pyopengl.sourceforge.net/)
* Python bindings for GtkGLExt (https://projects.gnome.org/gtkglext/download.html#pygtkglext)
* NumPy (http://www.numpy.org/)

Description
----------

The goal of this project was construct an Arduino-based robot capable of
walking on 4 legs. The biggest problem that had I had to solve to make the robot
walk was figuring out the inverse kinematics for the legs. From the point of
view of the code, the most straightforward way to specify a position of the
robot leg (specifically, the tip of the leg or the end effector) in space is to
use 3-dimensional coordinates. To convert from 3-dimensional coordinates to
angles for each joint, which can be passed to the servos powering the joints,
inverse kinematics equations have to be calculated.

The existing literature on the subject that I managed to uncover is terse and
math heavy, so the following description is based on my limited understanding
of the subject. Back in 1955, Jacques Denavit and Richard Hartenberg introduced
the standard convention to specify robot manipulator dimensions and degrees of
freedom. Denavit-Hartenberg parameters (DH parameters for short) for a given
manipulator are used to calculate a transformation matrix that provides
forward kinematics. What this means is that by inputting joint angles into the
matrix you can calculate the coordinates of the end effector. Practically
speaking, I had to carefully measure the robot leg, write down the measurements
as DH parameters and then use the parameters to calculate the matrix.

The inverse kinematics solutions were found algebraically from the forward
kinematics DH matrix. This part was the hardest part of the project for me, so
the best I can do here is provide a list of resources that I used to find the
solutions:

Industrial Robotics: Theory, Modelling and Control (specifically, chapter on
forward and inverse kinematics)
http://www.intechopen.com/books/industrial_robotics_theory_modelling_and_control

http://robotics.usc.edu/~aatrash/cs545/Lecture8.pdf
