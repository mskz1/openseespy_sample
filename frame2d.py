import matplotlib.pyplot as plt
import matplotlib.lines as ml
import matplotlib.patches as mp
import numpy as np
from matplotlib.path import Path
from matplotlib.patches import PathPatch


class Model:
    pass


class Node:
    def __init__(self, tag=0, x=0, y=0, loaded=False, supported=False):
        self._tag = tag
        self._x = x
        self._y = y
        self._loaded = loaded
        self._supported = supported

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, x):
        self._x = x

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, y):
        self._y = y

    @property
    def tag(self):
        return self._tag

    @tag.setter
    def tag(self, tag):
        self._tag = tag

    def plot(self, ax, disp_tag=False):
        ct_style = dict(color='k', linestyle='solid', linewidth=2., fill=True)
        text_style = dict(textcoords='offset points', color='k', size='x-small')

        ax.add_patch(mp.Circle((self._x, self._y), radius=1, **ct_style))
        if disp_tag:
            ax.annotate(str(self._tag), (self._x, self._y), xytext=(3, 3), **text_style)

    def plot_support_pin(self, ax):
        size = 50
        ox = self._x
        oy = self._y
        vertices = []
        codes = []
        codes = [Path.MOVETO] + [Path.LINETO] * 2 + [Path.CLOSEPOLY]
        vertices = [(ox, oy), (ox + size / 2, oy - size * 1.73 / 2), (ox - size / 2, oy - size * 1.73 / 2), (0, 0)]

        vertices = np.array(vertices, float)
        path = Path(vertices, codes)
        pathpatch = PathPatch(path, facecolor='None', edgecolor='k')
        ax.add_patch(pathpatch)

    def plot_support_roller(self, ax):
        size = 50
        ox = self._x
        oy = self._y
        vertices = []
        codes = []
        codes = [Path.MOVETO] + [Path.LINETO] * 2 + [Path.CLOSEPOLY]
        vertices = [(ox, oy), (ox + size / 2, oy - size * 1.73 / 2), (ox - size / 2, oy - size * 1.73 / 2), (0, 0)]

        codes += [Path.MOVETO] + [Path.LINETO] * 1 + [Path.CLOSEPOLY]
        vertices += [(ox + size / 2, oy - size * 1.73 / 2 - size / 4), (ox - size / 2, oy - size * 1.73 / 2 - size / 4),
                     (0, 0)]
        vertices = np.array(vertices, float)
        path = Path(vertices, codes)
        pathpatch = PathPatch(path, facecolor='None', edgecolor='k')
        ax.add_patch(pathpatch)


class Element:
    def __init__(self, tag=0, node1=0, node2=0):
        self._tag = tag
        self._node1 = node1
        self._node2 = node2

    @property
    def node1(self):
        return self._node1

    @node1.setter
    def node1(self, node1):
        self._node1 = node1

    @property
    def node2(self):
        return self._node2

    @node2.setter
    def node2(self, node2):
        self._node2 = node2

    @property
    def tag(self):
        return self._tag

    @tag.setter
    def tag(self, tag):
        self._tag = tag

    def plot(self, ax, node1, node2, disp_tag=False):
        line_style = dict(color='b', linestyle='solid', linewidth=2., marker='.')
        text_style = dict(textcoords='offset points', color='b', size='x-small')

        ax.add_line(ml.Line2D((node1.x, node2.x), (node1.y, node2.y), **line_style))
        if disp_tag:
            ax.annotate(str(self._tag), ((node1.x + node2.x) / 2, (node1.y + node2.y) / 2), xytext=(3, 3), **text_style)
