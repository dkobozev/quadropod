from math import radians, degrees, sin, cos, atan2, sqrt, pi

def fk(a1, a2, a3, a4, theta1, theta2, theta3, d1, d2, d3):
    theta1 = radians(theta1)
    theta2 = radians(theta2)
    theta3 = radians(theta3)

    c1  = cos(theta1)
    c2  = cos(theta2)
    c23 = cos(theta2 + theta3)

    s1  = sin(theta1)
    s2  = sin(theta2)
    s23 = sin(theta2 + theta3)

    x = a4*c1*c23 + a3*c1*c2 - d3*s1 + a2*c1 - d2*s1
    y = a4*s1*c23 + a3*s1*c2 + d3*c1 + a2*s1 + d2*c1
    z = -a4*s23 - a3*s2 + d1;

    return x, y, z

class IKError(Exception):
    pass

def convert_angle(a):
    """
    Return angle between -180 and 180 degrees.
    """
    a = round(degrees(a))

    if a >= 180:
        a = a % 180 - 180
    elif a < -180:
        a = 180 - abs(a) % 180

    if a == -180:
        a = 180

    return a

def ik_theta1(x, y, d2, d3):
    d = d2 + d3
    m = atan2(-x, y)
    n = atan2(sqrt(x*x + y*y - d*d), d)

    a1 = m + n
    a2 = m - n

    return convert_angle(a1), convert_angle(a2)

def ik_theta3(x, y, z, theta1, a2, a3, a4, d1):
    th1 = radians(theta1)
    m = -4*a2*x*cos(th1) - 4*a2*y*sin(th1) + x*x*cos(2*th1) + 2*x*y*sin(2*th1) - y*y*cos(2*th1) + 2*(z - d1)**2 + 2*a2*a2 + x*x + y*y;
    n = (m/2 - a3*a3 - a4*a4) / (2*a3*a4);
    n2 = round(n*n, 4)

    if n2 > 1:
        #print ('No solution for angle %f' % theta1)
        return ()

    o = sqrt(1 - n2)

    a1 = atan2(o, n)
    a2 = atan2(-o, n)

    return convert_angle(a1), convert_angle(a2)

def ik_theta2(x, y, z, theta1, theta3, a2, a4, d1):
    theta1 = radians(theta1)
    theta3 = radians(theta3)
    m = a2 - (x*cos(theta1) + y*sin(theta1))
    n = -z + d1
    o = a4*sin(theta3)
    p = m*m + n*n - o*o

    if p < 0:
        # no solutions
        return ()

    q = atan2(m, n)
    r = atan2(sqrt(p), o)

    a1 = q + r
    a2 = q - r

    return convert_angle(a1), convert_angle(a2)

def ik(x, y, z, a1, a2, a3, a4, d1, d2, d3):
    solutions = [(theta1, theta2, theta3) for theta1 in ik_theta1(x, y, d2, d3)
                                          for theta3 in ik_theta3(x, y, z, theta1, a2, a3, a4, d1)
                                          for theta2 in ik_theta2(x, y, z, theta1, theta3, a2, a4, d1)]
    #print ('all solutions:', solutions)

    # check the solutions by running them through forward kinematics and
    # comparing obtained coordinates
    valid = []
    for theta1, theta2, theta3 in solutions:
        px, py, pz = fk(a1, a2, a3, a4, theta1, theta2, theta3, d1, d2, d3)
        px, py, pz = round(px, 4), round(py, 4), round(pz, 4)
        #print ('fk', (px, py, pz))
        if abs(px - x) < 0.001 and abs(py - y) < 0.001 and abs(pz - z) < 0.001:
            valid.append((theta1, theta2, theta3))

    print ('valid solutions', valid)

    if len(valid) >= 1:
        return valid[0]
    else:
        return (0, 0, 0)

def verify_ik():
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

    theta1 = 180

    #for theta1 in range(0, -181, -1):
    for theta2 in range(-90, 91):
        for theta3 in range(0, 181):
            x, y, z = fk(a1, a2, a3, a4, theta1, theta2, theta3, d1, d2, d3)
            theta1ik, theta2ik, theta3ik = ik(x, y, z, a1, a2, a3, a4, d1, d2, d3)

            if theta1 != theta1ik or theta2 != theta2ik or theta3 != theta3ik:
                raise IKError('ik failure, expected (%s, %s, %s), got (%s, %s, %s)' % (
                    theta1, theta2, theta3, theta1ik, theta2ik, theta3ik))

if __name__ == '__main__':
    verify_ik()
