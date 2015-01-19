# File:          wheeled_robot.py
# Date:          
# Description:   
# Author:        
# Modifications: 

# You may need to import some classes of the controller module. Ex:
#  from controller import Robot, LED, DistanceSensor
#
# or to import the entire module. Ex:
#  from controller import *
from __future__ import division

from controller import *
import math
from math import radians
from iksolve import ik
import time
import sys

TIME_STEP = 16

# Here is the main class of your controller.
# This class defines how to initialize and how to run your controller.
# Note that this class derives Robot and so inherits all its functions
class Quadropod (Robot):
  alpha1 = 0
  a1     = 0
  d1     = -30

  alpha2 = -90
  a2     = 27.5
  d2     = 43

  alpha3 = 0
  a3     = 57.3
  d3     = -18

  alpha4 = 90
  a4     = 106
  d4     = 0
  
  def __init__(self):
    super(Quadropod, self).__init__()
    
    self.front_left0 = self.getMotor('front_left0')
    self.front_left1 = self.getMotor('front_left1')
    self.front_left2 = self.getMotor('front_left2')
    
    self.front_right0 = self.getMotor('front_right0')
    self.front_right1 = self.getMotor('front_right1')
    self.front_right2 = self.getMotor('front_right2')
    
    self.hind_right0 = self.getMotor('hind_right0')
    self.hind_right1 = self.getMotor('hind_right1')
    self.hind_right2 = self.getMotor('hind_right2')
    
    self.hind_left0 = self.getMotor('hind_left0')
    self.hind_left1 = self.getMotor('hind_left1')
    self.hind_left2 = self.getMotor('hind_left2')
    
    self.front_left0_sensor = self.getPositionSensor('front_left0_sensor')
    self.front_left1_sensor = self.getPositionSensor('front_left1_sensor')
    self.front_left2_sensor = self.getPositionSensor('front_left2_sensor')
    
    self.front_right0_sensor = self.getPositionSensor('front_right0_sensor')
    self.front_right1_sensor = self.getPositionSensor('front_right1_sensor')
    self.front_right2_sensor = self.getPositionSensor('front_right2_sensor')
    
    self.hind_right0_sensor = self.getPositionSensor('hind_right0_sensor')
    self.hind_right1_sensor = self.getPositionSensor('hind_right1_sensor')
    self.hind_right2_sensor = self.getPositionSensor('hind_right2_sensor')
    
    self.hind_left0_sensor = self.getPositionSensor('hind_left0_sensor')
    self.hind_left1_sensor = self.getPositionSensor('hind_left1_sensor')
    self.hind_left2_sensor = self.getPositionSensor('hind_left2_sensor')
  
  def ik(self, x, y, z):
    return ik(x, y, z, self.a1, self.a2, self.a3, self.a4,
              self.d1, self.d2, self.d3)
              
  def set_angles(self, name, theta1, theta2, theta3):
    if name == 'front_left' or name == 'hind_right':
      sign = -1
    else:
      sign = 1

    self.set_position(name + '0', radians(theta1 * sign))
    self.set_position(name + '1', radians(theta2))
    self.set_position(name + '2', radians(theta3 - 67.5))
    
  def set_position(self, name, position):
    #delta = 0.001
    getattr(self, name).setPosition(position)
    #sensor = getattr(self, name + '_sensor')
    #sensor.enable(TIME_STEP)
    
    while 0:
      self.tick()
      effective = sensor.getValue()
      if abs(position - effective) <= delta:
        break
        
    #sensor.disable()
    
  def tick(self):
    if self.step(TIME_STEP) == -1:
      sys.exit(0)
      
  def wait(self, sec):
    start = self.getTime()
    while start + sec > self.getTime():
      self.tick()
      
  def run(self):
    print 'hello!'
    self.stance()

    while True:
      self.walk()
      
  def stance(self):
    self.front_left0.setVelocity(2)
    self.front_left1.setVelocity(2)
    self.front_left2.setVelocity(2)
    
    self.front_right0.setVelocity(2)
    self.front_right1.setVelocity(2)
    self.front_right2.setVelocity(2)
    
    self.hind_right0.setVelocity(2)
    self.hind_right1.setVelocity(2)
    self.hind_right2.setVelocity(2)
    
    self.hind_left0.setVelocity(2)
    self.hind_left1.setVelocity(2)
    self.hind_left2.setVelocity(2)

    start = self.ik(50, -76, -100)
    #start = (0, 0, 0)
    self.set_angles('front_left', *start)
    self.set_angles('front_right', *start)
    self.set_angles('hind_right', *start)
    self.set_angles('hind_left', *start)
    self.wait(3)
    
    start = self.ik(50, -76, -120)
    self.set_angles('front_left', *start)
    self.set_angles('front_right', *start)
    self.set_angles('hind_right', *start)
    self.set_angles('hind_left', *start)
    self.wait(3)
  
  def walk(self):
    hrx = 50
    hry = -76
    hrz = -120

    frx = 50
    fry = -76
    frz = -120

    flx = 50
    fly = -76
    flz = -120

    hlx = 50
    hly = -76
    hlz = -120

    print 'shift body left'
    
    for t in range(1, 16):
      dt = t*2
      self.set_angles('hind_right', *self.ik(hrx+dt, hry-dt, hrz))
      self.set_angles('front_right', *self.ik(frx-dt, fry-dt, frz))
      self.set_angles('front_left', *self.ik(flx-dt, fly+dt, flz))
      self.set_angles('hind_left', *self.ik(hlx+dt, hly+dt, hlz))
      self.wait(0.02)

    hrx += 30
    hry -= 30
    frx -= 30
    fry -= 30
    flx -= 30
    fly += 30
    hlx += 30
    hly += 30
   
    print 'raise hr'

    raise_h = 38
    for t in range(1, 46):
      dt = t
      dz = math.sin(math.pi/2 * t/45) * raise_h
      self.set_angles('hind_right', *self.ik(hrx-dt, hry, hrz+dz))
      self.wait(0.02)

    hrx -= 45
    hrz += raise_h

    print 'lower hr'
    for t in range(1, 46):
      dt = t
      dz = (math.sin(math.pi/2 + math.pi/2 * t/45) - 1) * raise_h
      self.set_angles('hind_right', *self.ik(hrx-dt, hry, hrz+dz))
      self.wait(0.02)

    hrx -= 45
    hrz -= raise_h

    print 'raise fr'
    for t in range(1, 46):
      dt = t
      dz = math.sin(math.pi/2 * t/45) * raise_h
      self.set_angles('front_right', *self.ik(frx+dt, fry, frz+dz))
      self.wait(0.02)

    frx += 45
    frz += raise_h

    print 'lower fr'
    for t in range(1, 46):
      dt = t
      dz = (math.sin(math.pi/2 + math.pi/2 * t/45) - 1) * raise_h
      self.set_angles('front_right', *self.ik(frx+dt, fry, frz+dz))
      self.wait(0.02)

    frx += 45
    frz -= raise_h
   
    self.wait(0.2)

    print 'shift body right'

    for t in range(1, 16):
      dt = t*2
      self.set_angles('hind_right', *self.ik(hrx+dt, hry+dt*2, hrz))
      self.set_angles('front_right', *self.ik(frx-dt, fry+dt*2, frz))
      self.set_angles('front_left', *self.ik(flx-dt, fly-dt*2, flz))
      self.set_angles('hind_left', *self.ik(hlx+dt, hly-dt*2, hlz))
      self.wait(0.02)

    hrx += 30
    hry += 60
    frx -= 30
    fry += 60
    flx -= 30
    fly -= 60
    hlx += 30
    hly -= 60
    
    self.wait(0.2)

    print 'raise hl'

    for t in range(1, 46):
      dt =t
      dz = math.sin(math.pi/2 * t/45) * raise_h
      self.set_angles('hind_left', *self.ik(hlx-dt, hly, hlz+dz))
      self.wait(0.02)

    hlx -= 45
    hlz += raise_h

    print 'lower hl'
    for t in range(1, 46):
        dt = t
        dz = (math.sin(math.pi/2 + math.pi/2 * t/45) - 1) * raise_h
        self.set_angles('hind_left', *self.ik(hlx-dt, hly, hlz+dz))
        self.wait(0.02)

    hlx -= 45
    hlz -= raise_h

    print 'raise fl'
    for t in range(1, 46):
      dt = t
      dz = math.sin(math.pi/2 * t/45) * raise_h
      self.set_angles('front_left', *self.ik(flx+dt, fly, flz+dz))
      self.wait(0.02)

    flx += 45
    flz += raise_h

    print 'lower fl'
    for t in range(1, 46):
      dt = t
      dz = (math.sin(math.pi/2 + math.pi/2 * t/45) - 1) * raise_h
      self.set_angles('front_left', *self.ik(flx+dt, fly, flz+dz))
      self.wait(0.02)

    flx += 45
    flz -= raise_h

    print 'shift body back to center'
    for t in range(1, 16):
      dt = t*2
      self.set_angles('hind_right', *self.ik(hrx+dt, hry-dt, hrz))
      self.set_angles('front_right', *self.ik(frx-dt, fry-dt, frz))
      self.set_angles('front_left', *self.ik(flx-dt, fly+dt, flz))
      self.set_angles('hind_left', *self.ik(hlx+dt, hly+dt, hlz))
      self.wait(0.02)

    hrx += 30
    hry -= 30
    frx -= 30
    fry -= 30
    flx -= 30
    fly += 30
    hlx += 30
    hly += 30


# The main program starts from here

# This is the main program of your controller.
# It creates an instance of your Robot subclass, launches its
# function(s) and destroys it at the end of the execution.
# Note that only one instance of Robot should be created in
# a controller program.
controller = Quadropod()
controller.run()
