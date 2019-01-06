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
    # e1.set_theta()
    # assert e1.theta == 0.
    e2 = Element(2, 2, 3)
    e2.pinned1 = True
    e2.pinned2 = True
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)

    e1.plot(ax, n1, n2, disp_tag=True)
    e2.plot(ax, n2, n3, disp_tag=True)

    plt.axis('equal')
    plt.show()


@pytest.mark.skip
def test_plot_support_fig():
    n1 = Node(1, 0, 0)
    n2 = Node(2, 1000, 0)
    n3 = Node(3, 3000, 1000)
    n4 = Node(4, 6000, 2000)
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)

    n1.plot(ax, True)
    n1.plot_support_pin(ax)
    n2.plot(ax, True)
    n2.plot_support_fixed(ax)
    n3.plot(ax, True)
    n3.plot_support_roller(ax)
    n4.plot(ax, True)
    n4.plot_support_roller(ax, direc='Y')
    plt.axis('equal')
    plt.xlim((-1000, 10000))
    plt.ylim((-2000, 8000))
    plt.show()


# @pytest.mark.skip
def test_model():
    mdl = Model()
    mdl.add_node(1, 0, 0)
    mdl.add_node(2, 1000, 0)
    mdl.add_node(3, 2000, 1000)
    mdl.add_node(4, 3000, 1000)

    mdl.add_element(1, 1, 2)
    mdl.add_element(2, 2, 3, pinned1=True)
    mdl.add_element(3, 3, 4, pinned1=True, pinned2=True)
    # print(mdl.get_node_by_tag(1).x,mdl.get_node_by_tag(1).y)

    mdl.add_support(1, "110")
    mdl.add_support(2, "100")
    mdl.add_support(3, '010')
    mdl.add_support(4, '111')

    mdl.set_element_theta()
    # mdl._show_element_theta()
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)

    mdl.plot_model(ax)
    plt.axis('equal')
    # plt.xlim((-1000, 10000))
    # plt.ylim((-2000, 8000))
    plt.show()
