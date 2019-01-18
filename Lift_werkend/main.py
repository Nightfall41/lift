from SimPyLC import *
from elevator import Elevator, Plotter
from controller import MainController


e1 = Elevator(1, 10, 10, False)  # Elevator(number, floors, floorheight, express lift?)
e2 = Elevator(2, 4, 10, False)  # Elevator(number, floors, floorheight, express lift?)
e3 = Elevator(3, 4, 10, False)  # Elevator(number, floors, floorheight, express lift?)
e4 = Elevator(4, 5, 10, False)
p1 = Plotter(1, e1)
p2 = Plotter(2, e2)
p3 = Plotter(3, e3)
m = MainController(e1, e2, e3)
World(e1, e2, e3, e4, p1, p2, p3, m)
