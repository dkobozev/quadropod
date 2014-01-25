from __future__ import division

import math


class Vector(object):
    def __init__(self, *args):
        self.elements = args

    def __iter__(self):
        return iter(self.elements)

    def __getitem__(self, index):
        return self.elements[index]

    def __len__(self):
        return len(self.elements)

    def __repr__(self):
        return 'Vector(' + ', '.join([str(e) for e in self]) + ')'

    def __eq__(self, v):
        return all([a == b for a, b in zip(self, v)])

    def __neg__(self):
        """
        Negate the vector.
        """
        return Vector(*[-e for e in self])

    def __abs__(self):
        """
        Calculate vector magnitude (length).
        """
        return math.sqrt(sum([e*e for e in self]))

    length = __abs__
    magnitude = __abs__

    def __mul__(self, k):
        """
        Multiply the vector by a scalar.
        """
        return Vector(*[e * k for e in self])

    def __rmul__(self, k):
        return self.__mul__(k)

    def __div__(self, k):
        """
        Divide the vector by a scalar.
        """
        return Vector(*[e / k for e in self])

    def norm(self):
        """
        Normalize the vector.
        """
        magnitude = abs(self)
        return Vector(*[e / magnitude for e in self])

    def __add__(self, v):
        """
        Add two vectors.
        """
        return Vector(*[a + b for a, b in zip(self, v)])

    def __sub__(self, v):
        """
        Subtract two vectors.
        """
        return Vector(*[a - b for a, b in zip(self, v)])

    def dot(self, v):
        """
        Calculate the dot product of two vectors.
        """
        return sum([a * b for a, b in zip(self, v)])

    def cross(self, v):
        if len(self) != 3 or len(v) != 3:
            raise VectorException(
                "Cannot calculate the cross product for vectors of size %d and %d" % (
                    len(self), len(v)))

        x1, y1, z1 = self
        x2, y2, z2 = v

        return Vector(*[y1 * z2 - z1 * y2,
                        z1 * x2 - x1 * z2,
                        x1 * y2 - y1 * x2])

    def parallel(self, v):
        """
        Calculate vector's projection, parallel to v.
        """
        return v * (self.dot(v) / abs(v)**2)

    def perpendicular(self, v):
        """
        Calculate vector's projection, perpendicular to v.
        """
        return self - self.parallel(v)


if __name__ == '__main__':
    v1 = Vector(128, 125)
    print abs(v1)
