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
    self.stance3()
    
    self.strafe_left()
      
  def stance(self):
    velocity = 10

    self.front_left0.setVelocity(velocity)
    self.front_left1.setVelocity(velocity)
    self.front_left2.setVelocity(velocity)
    
    self.front_right0.setVelocity(velocity)
    self.front_right1.setVelocity(velocity)
    self.front_right2.setVelocity(velocity)
    
    self.hind_right0.setVelocity(velocity)
    self.hind_right1.setVelocity(velocity)
    self.hind_right2.setVelocity(velocity)
    
    self.hind_left0.setVelocity(velocity)
    self.hind_left1.setVelocity(velocity)
    self.hind_left2.setVelocity(velocity)

    start = self.ik(50, -76, -100)
    #start = (0, 0, 0)
    self.set_angles('front_left', *start)
    self.set_angles('front_right', *start)
    self.set_angles('hind_right', *start)
    self.set_angles('hind_left', *start)
    self.wait(1)
    
    start = self.ik(50, -76, -120)
    self.set_angles('front_left', *start)
    self.set_angles('front_right', *start)
    self.set_angles('hind_right', *start)
    self.set_angles('hind_left', *start)
    self.wait(1)
    
  def stance3(self):
    velocity = 10

    self.front_left0.setVelocity(velocity)
    self.front_left1.setVelocity(velocity)
    self.front_left2.setVelocity(velocity)

    self.front_right0.setVelocity(velocity)
    self.front_right1.setVelocity(velocity)
    self.front_right2.setVelocity(velocity)

    self.hind_right0.setVelocity(velocity)
    self.hind_right1.setVelocity(velocity)
    self.hind_right2.setVelocity(velocity)

    self.hind_left0.setVelocity(velocity)
    self.hind_left1.setVelocity(velocity)
    self.hind_left2.setVelocity(velocity)

    start = self.ik(80, -90, -100)
    self.set_angles('front_left', *start)
    self.set_angles('front_right', *start)
    self.set_angles('hind_right', *start)
    self.set_angles('hind_left', *start)
    self.wait(1)

    start = self.ik(80, -90, -120)
    self.set_angles('front_left', *start)
    self.set_angles('front_right', *start)
    self.set_angles('hind_right', *start)
    self.set_angles('hind_left', *start)
    self.wait(1)

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
    
    shift_steps = 10
    shift_factor = 30 / shift_steps
        
    raise_steps = 10
    t_factor = 45 / raise_steps
    raise_h = 38
    raise_wait = 0.02

    print 'shift body left'
    for t in range(1, shift_steps + 1):
      dt = t*shift_factor
      self.set_angles('hind_right',  *self.ik(hrx+dt, hry-dt, hrz))
      self.set_angles('front_right', *self.ik(frx-dt, fry-dt, frz))
      self.set_angles('front_left',  *self.ik(flx-dt, fly+dt, flz))
      self.set_angles('hind_left',   *self.ik(hlx+dt, hly+dt, hlz))
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
    for t in range(1, raise_steps + 1):
      dt = t*t_factor
      dz = math.sin(math.pi/2 * t/raise_steps) * raise_h
      self.set_angles('hind_right', *self.ik(hrx-dt, hry, hrz+dz))
      self.wait(raise_wait)

    hrx -= 45
    hrz += raise_h

    print 'lower hr'
    for t in range(1, raise_steps + 1):
      dt = t*t_factor
      dz = (math.sin(math.pi/2 + math.pi/2 * t/raise_steps) - 1) * raise_h
      self.set_angles('hind_right', *self.ik(hrx-dt, hry, hrz+dz))
      self.wait(raise_wait)

    hrx -= 45
    hrz -= raise_h
    self.wait(0.02)

    print 'raise fr'
    for t in range(1, raise_steps + 1):
      dt = t*t_factor
      dz = math.sin(math.pi/2 * t/raise_steps) * raise_h
      self.set_angles('front_right', *self.ik(frx+dt, fry, frz+dz))
      self.wait(raise_wait)

    frx += 45
    frz += raise_h

    print 'lower fr'
    for t in range(1, raise_steps + 1):
      dt = t*t_factor
      dz = (math.sin(math.pi/2 + math.pi/2 * t/raise_steps) - 1) * raise_h
      self.set_angles('front_right', *self.ik(frx+dt, fry, frz+dz))
      self.wait(raise_wait)

    frx += 45
    frz -= raise_h
    self.wait(0.2)

    print 'shift body right'

    for t in range(1, shift_steps + 1):
      dt = t*shift_factor
      self.set_angles('hind_right',  *self.ik(hrx+dt, hry+dt*2, hrz))
      self.set_angles('front_right', *self.ik(frx-dt, fry+dt*2, frz))
      self.set_angles('front_left',  *self.ik(flx-dt, fly-dt*2, flz))
      self.set_angles('hind_left',   *self.ik(hlx+dt, hly-dt*2, hlz))
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

    for t in range(1, raise_steps + 1):
      dt =t*t_factor
      dz = math.sin(math.pi/2 * t/raise_steps) * raise_h
      self.set_angles('hind_left', *self.ik(hlx-dt, hly, hlz+dz))
      self.wait(raise_wait)

    hlx -= 45
    hlz += raise_h

    print 'lower hl'
    for t in range(1, raise_steps + 1):
        dt = t*t_factor
        dz = (math.sin(math.pi/2 + math.pi/2 * t/raise_steps) - 1) * raise_h
        self.set_angles('hind_left', *self.ik(hlx-dt, hly, hlz+dz))
        self.wait(raise_wait)

    hlx -= 45
    hlz -= raise_h
    self.wait(0.02)

    print 'raise fl'
    for t in range(1, raise_steps + 1):
      dt = t*t_factor
      dz = math.sin(math.pi/2 * t/raise_steps) * raise_h
      self.set_angles('front_left', *self.ik(flx+dt, fly, flz+dz))
      self.wait(raise_wait)

    flx += 45
    flz += raise_h

    print 'lower fl'
    for t in range(1, raise_steps + 1):
      dt = t*t_factor
      dz = (math.sin(math.pi/2 + math.pi/2 * t/raise_steps) - 1) * raise_h
      self.set_angles('front_left', *self.ik(flx+dt, fly, flz+dz))
      self.wait(raise_wait)

    flx += 45
    flz -= raise_h
    self.wait(0.02)

    print 'shift body back to center'
    for t in range(1, shift_steps + 1):
      dt = t*shift_factor
      self.set_angles('hind_right',  *self.ik(hrx+dt, hry-dt, hrz))
      self.set_angles('front_right', *self.ik(frx-dt, fry-dt, frz))
      self.set_angles('front_left',  *self.ik(flx-dt, fly+dt, flz))
      self.set_angles('hind_left',   *self.ik(hlx+dt, hly+dt, hlz))
      self.wait(0.02)

    hrx += 30
    hry -= 30
    frx -= 30
    fry -= 30
    flx -= 30
    fly += 30
    hlx += 30
    hly += 30
    
  def walk2(self):
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
    
    x_distance = 40
    raise_steps = 10
    t_factor = x_distance / raise_steps
    raise_h = 25
    raise_wait = 0.02
    
    shift_distance = x_distance / 2
    shift_steps = 10
    shift_factor = shift_distance / shift_steps
    
    print 'raise fr'
    for t in range(1, raise_steps + 1):
      dt = t*t_factor
      dz = math.sin(math.pi/2 * t/raise_steps) * raise_h
      self.set_angles('front_right', *self.ik(frx+dt, fry, frz+dz))
      self.wait(raise_wait)

    frx += x_distance
    frz += raise_h

    print 'lower fr'
    for t in range(1, raise_steps + 1):
      dt = t*t_factor
      dz = (math.sin(math.pi/2 + math.pi/2 * t/raise_steps) - 1) * raise_h
      self.set_angles('front_right', *self.ik(frx+dt, fry, frz+dz))
      self.wait(raise_wait)

    frx += x_distance
    frz -= raise_h
    
    self.wait(0.02)
    
    print 'raise hl'
    for t in range(1, raise_steps + 1):
      dt =t*t_factor
      dz = math.sin(math.pi/2 * t/raise_steps) * raise_h
      self.set_angles('hind_left', *self.ik(hlx-dt, hly, hlz+dz))
      self.wait(raise_wait)

    hlx -= x_distance
    hlz += raise_h

    print 'lower hl'
    for t in range(1, raise_steps + 1):
        dt = t*t_factor
        dz = (math.sin(math.pi/2 + math.pi/2 * t/raise_steps) - 1) * raise_h
        self.set_angles('hind_left', *self.ik(hlx-dt, hly, hlz+dz))
        self.wait(raise_wait)

    hlx -= x_distance
    hlz -= raise_h
    
    self.wait(0.02)

    print 'shift body forward'
    for t in range(1, shift_steps + 1):
      dt = t*shift_factor
      self.set_angles('hind_right',  *self.ik(hrx+dt, hry, hrz))
      self.set_angles('front_right', *self.ik(frx-dt, fry, frz))
      self.set_angles('front_left',  *self.ik(flx-dt, fly, flz))
      self.set_angles('hind_left',   *self.ik(hlx+dt, hly, hlz))
      self.wait(0.02)
      
    hrx += shift_distance
    frx -= shift_distance
    flx -= shift_distance
    hlx += shift_distance
    
    self.wait(0.02)
        
    print 'shift body forward'
    for t in range(1, shift_steps + 1):
      dt = t*shift_factor
      self.set_angles('hind_right',  *self.ik(hrx+dt, hry, hrz))
      self.set_angles('front_right', *self.ik(frx-dt, fry, frz))
      self.set_angles('front_left',  *self.ik(flx-dt, fly, flz))
      self.set_angles('hind_left',   *self.ik(hlx+dt, hly, hlz))
      self.wait(0.02)
      
    hrx += shift_distance
    frx -= shift_distance
    flx -= shift_distance
    hlx += shift_distance
    
    self.wait(0.02)
    
    sys.exit(0)
        
    print 'raise fl'
    for t in range(1, raise_steps + 1):
      dt = t*t_factor
      dz = math.sin(math.pi/2 * t/raise_steps) * raise_h
      self.set_angles('front_left', *self.ik(flx+dt, fly, flz+dz))
      self.wait(raise_wait)

    flx += x_distance
    flz += raise_h

    print 'lower fl'
    for t in range(1, raise_steps + 1):
      dt = t*t_factor
      dz = (math.sin(math.pi/2 + math.pi/2 * t/raise_steps) - 1) * raise_h
      self.set_angles('front_left', *self.ik(flx+dt, fly, flz+dz))
      self.wait(raise_wait)

    flx += x_distance
    flz -= raise_h
    self.wait(0.02)

    
    print 'shift body forward'

    for t in range(1, shift_steps + 1):
      dt = t*shift_factor
      self.set_angles('hind_right',  *self.ik(hrx+dt, hry, hrz))
      self.set_angles('front_right', *self.ik(frx-dt, fry, frz))
      self.set_angles('front_left',  *self.ik(flx-dt, fly, flz))
      self.set_angles('hind_left',   *self.ik(hlx+dt, hly, hlz))
      self.wait(0.02)
      
    hrx += shift_distance
    frx -= shift_distance
    flx -= shift_distance
    hlx += shift_distance
    
    self.wait(0.02)
            
    print 'shift body forward'

    for t in range(1, shift_steps + 1):
      dt = t*shift_factor
      self.set_angles('hind_right',  *self.ik(hrx+dt, hry, hrz))
      self.set_angles('front_right', *self.ik(frx-dt, fry, frz))
      self.set_angles('front_left',  *self.ik(flx-dt, fly, flz))
      self.set_angles('hind_left',   *self.ik(hlx+dt, hly, hlz))
      self.wait(0.02)
      
    hrx += shift_distance
    frx -= shift_distance
    flx -= shift_distance
    hlx += shift_distance
    
    self.wait(0.02)

    print 'raise hr'
    for t in range(1, raise_steps + 1):
      dt = t*t_factor
      dz = math.sin(math.pi/2 * t/raise_steps) * raise_h
      self.set_angles('hind_right', *self.ik(hrx-dt, hry, hrz+dz))
      self.wait(raise_wait)

    hrx -= x_distance
    hrz += raise_h

    print 'lower hr'
    for t in range(1, raise_steps + 1):
      dt = t*t_factor
      dz = (math.sin(math.pi/2 + math.pi/2 * t/raise_steps) - 1) * raise_h
      self.set_angles('hind_right', *self.ik(hrx-dt, hry, hrz+dz))
      self.wait(raise_wait)

    hrx -= x_distance
    hrz -= raise_h
    self.wait(0.02)
    
  def walk3(self):
    hrx = 80
    hry = -90
    hrz = -120

    frx = 80
    fry = -90
    frz = -120

    flx = 80
    fly = -90
    flz = -120

    hlx = 80
    hly = -90
    hlz = -120

    shift_dx = 13.75
    shift_dy = 15

    raise_d = 55
    raise_h = 38
    step_wait = 0.02

    print 'shift body left, raise hr'
    steps = 10
    for t in range(1, steps + 1):
      sdx = shift_dx * t/steps
      sdy = shift_dy * t/steps
      rdt = raise_d * t/steps
      rdz = raise_h * math.sin(math.pi/2 * t/steps)

      self.set_angles('hind_right',  *self.ik(hrx+sdx-rdt, hry-sdy, hrz+rdz))
      self.set_angles('front_right', *self.ik(frx-sdx,     fry-sdy, frz))
      self.set_angles('front_left',  *self.ik(flx-sdx,     fly+sdy, flz))
      self.set_angles('hind_left',   *self.ik(hlx+sdx,     hly+sdy, hlz))

      self.wait(step_wait)

    hrx += shift_dx
    hry -= shift_dy
    frx -= shift_dx
    fry -= shift_dy
    flx -= shift_dx
    fly += shift_dy
    hlx += shift_dx
    hly += shift_dy

    hrx -= raise_d
    hrz += raise_h

    print 'shift body left, lower hr'
    steps = 10
    for t in range(1, steps + 1):
      sdx = shift_dx * t/steps
      sdy = shift_dy * t/steps
      rdt = raise_d * t/steps
      rdz = raise_h * (math.sin(math.pi/2 + math.pi/2 * t/steps) - 1)

      self.set_angles('hind_right',  *self.ik(hrx+sdx-rdt, hry-sdy, hrz+rdz))
      self.set_angles('front_right', *self.ik(frx-sdx,     fry-sdy, frz))
      self.set_angles('front_left',  *self.ik(flx-sdx,     fly+sdy, flz))
      self.set_angles('hind_left',   *self.ik(hlx+sdx,     hly+sdy, hlz))

      self.wait(step_wait)

    hrx += shift_dx
    hry -= shift_dy
    frx -= shift_dx
    fry -= shift_dy
    flx -= shift_dx
    fly += shift_dy
    hlx += shift_dx
    hly += shift_dy

    hrx -= raise_d
    hrz -= raise_h

    print 'shift body right, raise fr'
    steps = 10
    for t in range(1, steps + 1):
      sdx = shift_dx * t/steps
      sdy = shift_dy * t/steps
      rdt = raise_d * t/steps
      rdz = raise_h * math.sin(math.pi/2 * t/steps)

      self.set_angles('hind_right',  *self.ik(hrx+sdx,     hry+sdy, hrz))
      self.set_angles('front_right', *self.ik(frx-sdx+rdt, fry+sdy, frz+rdz))
      self.set_angles('front_left',  *self.ik(flx-sdx,     fly-sdy, flz))
      self.set_angles('hind_left',   *self.ik(hlx+sdx,     hly-sdy, hlz))

      self.wait(step_wait)

    hrx += shift_dx
    hry += shift_dy
    frx -= shift_dx
    fry += shift_dy
    flx -= shift_dx
    fly -= shift_dy
    hlx += shift_dx
    hly -= shift_dy

    frx += raise_d
    frz += raise_h

    print 'shift body right, lower fr'
    steps = 10
    for t in range(1, steps + 1):
      sdx = shift_dx * t/steps
      sdy = shift_dy * t/steps
      rdt = raise_d * t/steps
      rdz = raise_h * (math.sin(math.pi/2 + math.pi/2 * t/steps) - 1)

      self.set_angles('hind_right',  *self.ik(hrx+sdx,     hry+sdy, hrz))
      self.set_angles('front_right', *self.ik(frx-sdx+rdt, fry+sdy, frz+rdz))
      self.set_angles('front_left',  *self.ik(flx-sdx,     fly-sdy, flz))
      self.set_angles('hind_left',   *self.ik(hlx+sdx,     hly-sdy, hlz))

      self.wait(step_wait)

    hrx += shift_dx
    hry += shift_dy
    frx -= shift_dx
    fry += shift_dy
    flx -= shift_dx
    fly -= shift_dy
    hlx += shift_dx
    hly -= shift_dy

    frx += raise_d
    frz -= raise_h

    print 'shift body right, raise hl'
    steps = 10
    for t in range(1, steps + 1):
      sdx = shift_dx * t/steps
      sdy = shift_dy * t/steps
      rdt = raise_d * t/steps
      rdz = raise_h * math.sin(math.pi/2 * t/steps)

      self.set_angles('hind_right',  *self.ik(hrx+sdx,     hry+sdy, hrz))
      self.set_angles('front_right', *self.ik(frx-sdx,     fry+sdy, frz))
      self.set_angles('front_left',  *self.ik(flx-sdx,     fly-sdy, flz))
      self.set_angles('hind_left',   *self.ik(hlx+sdx-rdt, hly-sdy, hlz+rdz))

      self.wait(step_wait)

    hrx += shift_dx
    hry += shift_dy
    frx -= shift_dx
    fry += shift_dy
    flx -= shift_dx
    fly -= shift_dy
    hlx += shift_dx
    hly -= shift_dy

    hlx -= raise_d
    hlz += raise_h

    print 'shift body right, lower hl'
    for t in range(1, steps + 1):
      sdx = shift_dx * t/steps
      sdy = shift_dy * t/steps
      rdt = raise_d * t/steps
      rdz = raise_h * (math.sin(math.pi/2 + math.pi/2 * t/steps) - 1)

      self.set_angles('hind_right',  *self.ik(hrx+sdx,     hry+sdy, hrz))
      self.set_angles('front_right', *self.ik(frx-sdx,     fry+sdy, frz))
      self.set_angles('front_left',  *self.ik(flx-sdx,     fly-sdy, flz))
      self.set_angles('hind_left',   *self.ik(hlx+sdx-rdt, hly-sdy, hlz+rdz))

      self.wait(step_wait)

    hrx += shift_dx
    hry += shift_dy
    frx -= shift_dx
    fry += shift_dy
    flx -= shift_dx
    fly -= shift_dy
    hlx += shift_dx
    hly -= shift_dy

    hlx -= raise_d
    hlz -= raise_h

    print 'shift body left, raise fl'
    steps = 10
    for t in range(1, steps + 1):
      sdx = shift_dx * t/steps
      sdy = shift_dy * t/steps
      rdt = raise_d * t/steps
      rdz = raise_h * math.sin(math.pi/2 * t/steps)

      self.set_angles('hind_right',  *self.ik(hrx+sdx,     hry-sdy, hrz))
      self.set_angles('front_right', *self.ik(frx-sdx,     fry-sdy, frz))
      self.set_angles('front_left',  *self.ik(flx-sdx+rdt, fly+sdy, flz+rdz))
      self.set_angles('hind_left',   *self.ik(hlx+sdx,     hly+sdy, hlz))

      self.wait(step_wait)

    hrx += shift_dx
    hry -= shift_dy
    frx -= shift_dx
    fry -= shift_dy
    flx -= shift_dx
    fly += shift_dy
    hlx += shift_dx
    hly += shift_dy

    flx += raise_d
    flz += raise_h

    print 'shift body left, lower fl'
    steps = 10
    for t in range(1, steps + 1):
      sdx = shift_dx * t/steps
      sdy = shift_dy * t/steps
      rdt = raise_d * t/steps
      rdz = raise_h * (math.sin(math.pi/2 + math.pi/2 * t/steps) - 1)

      self.set_angles('hind_right',  *self.ik(hrx+sdx,     hry-sdy, hrz))
      self.set_angles('front_right', *self.ik(frx-sdx,     fry-sdy, frz))
      self.set_angles('front_left',  *self.ik(flx-sdx+rdt, fly+sdy, flz+rdz))
      self.set_angles('hind_left',   *self.ik(hlx+sdx,     hly+sdy, hlz))

      self.wait(step_wait)

    hrx += shift_dx
    hry -= shift_dy
    frx -= shift_dx
    fry -= shift_dy
    flx -= shift_dx
    fly += shift_dy
    hlx += shift_dx
    hly += shift_dy

    flx += raise_d
    flz -= raise_h
    
    #print 'shift body forward'
    #steps = 10
    #shift_dx = 25
    #for t in range(1, steps + 1):
    #  sdx = shift_dx * t/steps
    #
    #  self.set_angles('hind_right',  *self.ik(hrx+sdx, hry, hrz))
    #  self.set_angles('front_right', *self.ik(frx-sdx, fry, frz))
    #  self.set_angles('front_left',  *self.ik(flx-sdx, fly, flz))
    #  self.set_angles('hind_left',   *self.ik(hlx+sdx, hly, hlz))
    #
    #  self.wait(step_wait)
    #
    #hrx += shift_dx
    #frx -= shift_dx
    #flx -= shift_dx
    #hlx += shift_dx

  def turn_left(self):
    hrx = 80
    hry = -90
    hrz = -120

    frx = 80
    fry = -90
    frz = -120

    flx = 80
    fly = -90
    flz = -120

    hlx = 80
    hly = -90
    hlz = -120

    angle = 30
    raise_h = 38
    step_wait = 0.04

    print 'turning left'
    steps = 10
    theta1, theta2, theta3 = self.ik(hrx, hry, hrz)
    for t in range(1, steps + 1):
       dt = t * angle/steps

       self.set_angles('hind_right',  theta1+dt, theta2, theta3)
       self.set_angles('front_right', theta1-dt, theta2, theta3)
       self.set_angles('front_left',  theta1+dt, theta2, theta3)
       self.set_angles('hind_left',   theta1-dt, theta2, theta3)

       self.wait(step_wait)

    self.wait(step_wait)

    print 'readjust hr'
    steps = 10
    for t in range(1, steps + 1):
       dt = t * angle/steps
       rdz = raise_h * math.sin(math.pi * t/steps)

       theta1, theta2, theta3 = self.ik(hrx, hry, hrz+rdz)
       self.set_angles('hind_right', theta1+angle-dt, theta2, theta3)

       self.wait(step_wait)

    self.wait(step_wait)

    print 'readjust fr'
    steps = 10
    for t in range(1, steps + 1):
       dt = t * angle/steps
       rdz = raise_h * math.sin(math.pi * t/steps)

       theta1, theta2, theta3 = self.ik(hrx, hry, hrz+rdz)
       self.set_angles('front_right', theta1-angle+dt, theta2, theta3)

       self.wait(step_wait)

    self.wait(step_wait)

    print 'readjust fl'
    steps = 10
    for t in range(1, steps + 1):
       dt = t * angle/steps
       rdz = raise_h * math.sin(math.pi * t/steps)

       theta1, theta2, theta3 = self.ik(hrx, hry, hrz+rdz)
       self.set_angles('front_left', theta1+angle-dt, theta2, theta3)

       self.wait(step_wait)

    self.wait(step_wait)

    print 'readjust hl'
    steps = 10
    for t in range(1, steps + 1):
       dt = t * angle/steps
       rdz = raise_h * math.sin(math.pi * t/steps)

       theta1, theta2, theta3 = self.ik(hrx, hry, hrz+rdz)
       self.set_angles('hind_left', theta1-angle+dt, theta2, theta3)

       self.wait(step_wait)

    self.wait(step_wait)

  def strafe_left(self):
    hrx = 80
    hry = -90
    hrz = -120

    frx = 80
    fry = -90
    frz = -120

    flx = 80
    fly = -90
    flz = -120

    hlx = 80
    hly = -90
    hlz = -120

    strafe_d = 40
    raise_h = 38
    step_wait = 0.02

    print 'shift body left'
    steps = 10
    for t in range(1, steps + 1):
      sdy = strafe_d * t/steps

      self.set_angles('hind_right',  *self.ik(hrx, hry-sdy, hrz))
      self.set_angles('front_right', *self.ik(frx, fry-sdy, frz))
      self.set_angles('front_left',  *self.ik(flx, fly+sdy, flz))
      self.set_angles('hind_left',   *self.ik(hlx, hly+sdy, hlz))

      self.wait(step_wait)

    hry -= strafe_d
    fry -= strafe_d
    fly += strafe_d
    hly += strafe_d

    self.wait(step_wait)

    print 'readjust hl'
    steps = 10
    for t in range(1, steps + 1):
      dy = t * strafe_d/steps
      rdz = raise_h * math.sin(math.pi * t/steps)

      self.set_angles('hind_left', *self.ik(hlx, hly-dy, hlz+rdz))

      self.wait(step_wait)

    hly -= strafe_d

    self.wait(step_wait)

    print 'readjust fl'
    steps = 10
    for t in range(1, steps + 1):
      dy = t * strafe_d/steps
      rdz = raise_h * math.sin(math.pi * t/steps)

      self.set_angles('front_left', *self.ik(flx, fly-dy, flz+rdz))

      self.wait(step_wait)

    fly -= strafe_d

    self.wait(step_wait)

    print 'readjust hr'
    steps = 10
    for t in range(1, steps + 1):
      dy = t * strafe_d/steps
      rdz = raise_h * math.sin(math.pi * t/steps)

      self.set_angles('hind_right', *self.ik(hrx, hry+dy, hrz+rdz))

      self.wait(step_wait)

    hry += strafe_d

    self.wait(step_wait)

    print 'readjust fr'
    steps = 10
    for t in range(1, steps + 1):
      dy = t * strafe_d/steps
      rdz = raise_h * math.sin(math.pi * t/steps)

      self.set_angles('front_right', *self.ik(frx, fry+dy, frz+rdz))

      self.wait(step_wait)

    fry += strafe_d

    self.wait(step_wait)


# The main program starts from here

# This is the main program of your controller.
# It creates an instance of your Robot subclass, launches its
# function(s) and destroys it at the end of the execution.
# Note that only one instance of Robot should be created in
# a controller program.
controller = Quadropod()
controller.run()
