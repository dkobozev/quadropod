from __future__ import division

import math
from vector import Vector
from geometry import circle_intersection, segment_angle


class Leg(object):
    """
    A robotic leg with 3 degrees of freedom (3dof).
    """
    def __init__(self, position):
        self.position = position

        #self.offsets    = [26.9, -23.6, -27]
        self.offsets    = [26.9, 23.6, -27]
        self.dimensions = [57.5, 105]

    def angles(self):
        """
        Calculate leg servo angles for current position.
        """
        x, y, z = self.position - self.offset_vector()

        alpha = segment_angle(0, 0, x, y)

        knee = self.knee_position((x, z))
        beta = segment_angle(0, 0, knee[0], knee[1])
        gamma = (2*math.pi + segment_angle(knee[0], knee[1], x, z) - beta) % (2*math.pi)

        return [math.degrees(a) for a in (alpha, beta, gamma)]

    def knee_position(self, dst):
        x, y, z = dst
        kx, kz = circle_intersection(0, 0, self.dimensions[0],
                                     x, z, self.dimensions[1])[0]
        return Vector(kx, y, kz)

    def translate(self, v):
        """
        Move leg.
        """
        self.position += v

    def offset_vector(self):
        x, y, z = self.position

        x_offset = self.offsets[0] * Vector(x, y).norm()
        y_offset = self.offsets[1] * Vector(0, 1).perpendicular(Vector(x, y)).norm()
        xy_offset = x_offset + y_offset

        offset = Vector(xy_offset[0], xy_offset[1], self.offsets[2])
        return offset


class LynxmotionQuad(object):

    def __init__(self):
        # hind right, front right, front left, hind left
        self.legs = [
            Leg(Vector(26, 154, -55)),
            Leg(Vector(26, 154, -55)),
            Leg(Vector(26, 154, -55)),
            Leg(Vector(26, 154, -55)),
        ]

    def translate(self, v):
        """
        Move body.

        Robot's own coordinate system has the y axis pointing forward and the x
        axis pointing to the right, same as the robot's front right leg's
        coordinate system.
        """
        self.legs[0].translate(Vector( v[0], -v[1], -v[2]))
        self.legs[1].translate(Vector( v[0],  v[1], -v[2]))
        self.legs[2].translate(Vector(-v[0],  v[1], -v[2]))
        self.legs[3].translate(Vector(-v[0], -v[1], -v[2]))

    def print_angles(self):
        for leg in self.legs:
            print '// x: %d, y: %d, z: %d' % tuple(leg.position)
            hip, knee, ankle = leg.angles()
            print "%d, %d, %d," % (round(ankle), round(knee), round(hip))

    def print_move(self, duration=20):
        print '{%d,' % duration
        self.print_angles()
        print '},'
        print


if __name__ == '__main__':
    bot = LynxmotionQuad()
    bot.print_move(10)
