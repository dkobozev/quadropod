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

Resources
---------
* http://en.wikipedia.org/wiki/Forward_kinematics
* http://en.wikipedia.org/wiki/Inverse_kinematics
* http://en.wikipedia.org/wiki/Denavit%E2%80%93Hartenberg_parameters
* Industrial Robotics: Theory, Modelling and Control (specifically, chapter on
  forward and inverse kinematics)
  http://www.intechopen.com/books/industrial_robotics_theory_modelling_and_control
* http://robotics.usc.edu/~aatrash/cs545/Lecture8.pdf
