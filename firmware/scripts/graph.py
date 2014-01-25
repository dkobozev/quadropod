from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np

from matplotlib.patches import FancyArrowPatch
from mpl_toolkits.mplot3d import proj3d

from kinematics import Leg
from vector import Vector


class Arrow3D(FancyArrowPatch):
    def __init__(self, xs, ys, zs, *args, **kwargs):
        FancyArrowPatch.__init__(self, (0,0), (0,0), *args, **kwargs)
        self._verts3d = xs, ys, zs

    def draw(self, renderer):
        xs3d, ys3d, zs3d = self._verts3d
        xs, ys, zs = proj3d.proj_transform(xs3d, ys3d, zs3d, renderer.M)
        self.set_positions((xs[0],ys[0]),(xs[1],ys[1]))
        FancyArrowPatch.draw(self, renderer)

def plot_vector(a, b):
    a = Arrow3D(*zip(a, b), mutation_scale=20, lw=1, arrowstyle="-|>", color="r")
    ax.add_artist(a)


if __name__ == '__main__':
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    ax.set_aspect("equal")

    leg = Leg(Vector(26, 154, -55))
    knee = leg.knee_position(leg.position)

    plot_vector([0, 0, 0], knee)
    plot_vector(knee, leg.position)

    plt.show()
