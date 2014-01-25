import math


identity_matrix = [[1, 0, 0],
                   [0, 1, 0],
                   [0, 0, 1]]

def mult(A, B):
    assert len(A[0]) == len(B), \
        'The number of columns in A does not match the number of rows in B.'

    def cols(l):
        return [list(col) for col in zip(*l)]

    return [[sum([a * b for a, b in zip(col, row)]) for col in cols(B)]
        for row in A]

def rotation_matrix(angle, axis):
    x, y, z = axis
    angle_r = math.radians(angle)
    c = math.cos(angle_r)
    s = math.sin(angle_r)
    C = 1 - c
    matrix = [[x**2*C + c,  x*y*C - z*s, x*z*C + y*s],
              [y*x*C + z*s, y**2*C + c,  y*z*C - x*s],
              [x*z*C - y*s, y*z*C + x*s, z**2*C+c   ]]
    return matrix

def reflection_matrix(n):
    x, y, z = n
    matrix = [[1 - 2*x**2, -2*x*y,     -2*x*z],
              [-2*x*y,     1 - 2*y**2, -2*y*z],
              [-2*x*z,     -2*y*z,     1 - 2*z**2]]
    return matrix

def mirror(A, v):
    return mult(A, reflection_matrix(v))

def rotate(A, angle, v):
    return mult(A, rotation_matrix(angle, v))


if __name__ == '__main__':
    pos = [1, 0, -1]
    print mirror([pos], [1, 0, 0])[0]
    print pos
    print mirror([pos], [0, 0, 1])[0]
    print mirror(mirror([pos], [1, 0, 0]), [0, 0, 1])[0]

