from __future__ import division

import math


def segment_angle(x1, y1, x2, y2):
    """
    Find the angle between the x-axis and a line segment.
    """
    # use atan2 to find the correct quadrant
    return (math.atan2(y2 - y1, x2 - x1) + 2*math.pi) % (2*math.pi)

def circle_intersection(x0, y0, r0, x1, y1, r1):
    """
    Find intersection points between two circles.
    """
    # horizontal and vertical distances between circle centers P0 and P1
    dx, dy = (x1 - x0), (y1 - y0)

    # straight-line distance between P0 and P1
    d = math.sqrt(dx**2 + dy**2)

    if d > (r0 + r1):
        raise Exception('Circles are separate, no solutions.')
    elif d < abs(r0 - r1):
        raise Exception('Circles are nested, no solutions.')
    elif d == 0 and r0 == r1:
        raise Exception('Circles are coincident, infinite number of solutions.')

    # P2 is the point where the line through the circle intersection points
    # crosses the line between P0 and P1

    # find the distance from P0 to P2
    a = (r0**2 - r1**2 + d**2) / (2*d)

    # find the distance from P2 to either of the circle intersection points P3
    h = math.sqrt(r0**2 - a**2)

    # calculate the coordinates of P2
    x2 = x0 + a * dx / d
    y2 = y0 + a * dy / d

    # calculate the coordinates of intersection points
    offset_x = h * dy / d
    offset_y = h * dx / d

    x3a = x2 - offset_x
    y3a = y2 + offset_y
    x3b = x2 + offset_x
    y3b = y2 - offset_y

    return ((x3a, y3a), (x3b, y3b))
