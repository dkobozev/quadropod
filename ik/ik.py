import bpy
from mathutils import Vector, Euler, Matrix
from math import radians, degrees, sin, cos, atan2, sqrt, pi

def delete_meshes():
    candidate_list = [item.name for item in bpy.data.objects if item.type == "MESH"]

    # select mesh objects and remove them
    for object_name in candidate_list:
        bpy.data.objects[object_name].select = True
    bpy.ops.object.delete()

    # remove the meshes, they have no users anymore
    for item in bpy.data.meshes:
        bpy.data.meshes.remove(item)

def create_joint(m, alpha, a1, a2, theta, d):
    rotx   = Matrix.Rotation(radians(alpha), 4, 'X')
    transx = Matrix.Translation(Vector((a1, 0, 0)))
    rotz   = Matrix.Rotation(radians(theta), 4, 'Z')
    transz = Matrix.Translation(Vector((0, 0, d)))
    m = m * rotx * transx * rotz * transz

    bpy.ops.mesh.primitive_cone_add(radius1=9, depth=15)
    j = bpy.context.scene.objects.active
    j.matrix_world = m

    if a2 != 0:
        # render link
        bpy.ops.mesh.primitive_cylinder_add(radius=2, depth=a2)
        link = bpy.context.scene.objects.active
        link_roty = Matrix.Rotation(radians(90), 4, 'Y')
        link_transx = Matrix.Translation(Vector((0, 0, a2/2)))
        link.matrix_world = m * link_roty * link_transx

    if d != 0:
        # render offset
        bpy.ops.mesh.primitive_cube_add()
        offset = bpy.context.scene.objects.active
        offset_transx = Matrix.Translation(Vector((0, 0, -d/2)))
        offset_s = Matrix.Scale(abs(d/2), 4, Vector((0, 0, 1)))
        offset.matrix_world = m * offset_transx * offset_s

    return m

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

class NoSolutionsError(Exception):
    pass

class IKError(Exception):
    pass

def convert_angle(a):
    """
    Return angle between -180 and 180 degrees.
    """
    if a >= pi:
        a = a % pi - pi
    elif a < -pi:
        a = pi - abs(a) % pi

    return round(degrees(a), 1)

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

def render_manipulator(theta1, theta2, theta3):
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

    #print ("Deleting all meshes...")
    delete_meshes()

    m = Matrix()
    m = create_joint(m, alpha1, a1, a2, theta1, d1)
    m = create_joint(m, alpha2, a2, a3, theta2, d2)
    m = create_joint(m, alpha3, a3, a4, theta3, d3)
    m = create_joint(m, alpha4, a4, 0, 0, d4)

    j = bpy.context.scene.objects.active

    print ()
    print ('location', j.location)
    print ('checking ik for', (theta1, theta2, theta3))

    x, y, z = j.location
    x, y, z = round(x, 4), round(y, 4), round(z, 4)

    theta1ik, theta2ik, theta3ik = ik(x, y, z, a1, a2, a3, a4, d1, d2, d3)

    if theta1 != theta1ik or theta2 != theta2ik or theta3 != theta3ik:
        print ('ik failure, expected', (theta1, theta2, theta3), 'got', (theta1ik, theta2ik, theta3ik))
        raise IKError('ik failure, expected', (theta1, theta2, theta3), 'got', (theta1ik, theta2ik, theta3ik))


theta1 = 0 # from 0 to -180
theta2 = 53 # from -90 to 90
theta3 = 60 # from 0 to 180


for theta1 in range(0, -181, -1):
    for theta2 in range(-90, 91):
        render_manipulator(theta1, theta2, theta3)

print ('done')
