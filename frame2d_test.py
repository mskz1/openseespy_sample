import matplotlib.pyplot as plt
from frame2d import Model
from frame2d import Node, Element
from pytest import approx
import pytest


def test_node():
    n1 = Node(x=0, y=0)
    n2 = Node(x=1000, y=0)
    n3 = Node()
    n3.x = 400.
    n3.y = -200
    n3.tag = 5
    assert n1.x == 0
    assert n2.x == 1000
    assert n2.y == 0
    assert n3.x == 400
    assert n3.y == -200
    assert n3.tag == 5


def test_element():
    e1 = Element()
    e1.tag = 1
    e1.node1 = 1
    e1.node2 = 2
    assert e1.tag == 1
    assert e1.node1 == 1





@pytest.mark.skip
def test_plot_node():
    nodes = [Node(1, 0, 0), Node(2, 1000, 0), Node(3, 2000, 1000)]
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)

    for n in nodes:
        n.plot(ax, disp_tag=True)

    plt.axis('equal')
    plt.show()


@pytest.mark.skip
def test_plot_element():
    n1 = Node(1, 0, 0)
    n2 = Node(2, 1000, 0)
    n3 = Node(3, 2000, 1000)
    nodes = [n1, n2, n3]
    e1 = Element(1, 1, 2)
    e2 = Element(2, 2, 3)
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)

    e1.plot(ax, n1, n2, disp_tag=True)
    e2.plot(ax, n2, n3, disp_tag=True)

    plt.axis('equal')
    plt.show()

# @pytest.mark.skip
def test_plot_support_fig():
    n1 = Node(1, 0, 0)
    n2 = Node(2, 1000, 0)
    n3 = Node(3, 8000, 1000)
    # view_range = 8000  # 支点マークのサイズを決める
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)

    # pin support
    n1.plot(ax,True)
    n1.plot_support_pin(ax)
    n2.plot(ax)
    n2.plot_support_fixed(ax)
    n3.plot(ax)
    n3.plot_support_roller(ax)
    plt.axis('equal')

    plt.show()
