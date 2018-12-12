from frame2d import Model
from frame2d import Node

def test_node():
    n1 = Node(0,0)
    n2 = Node(1000,0)
    assert n1.x == 0
    assert n2.x == 1000
    assert n2.y == 0



