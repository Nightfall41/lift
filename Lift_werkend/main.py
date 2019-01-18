from SimPyLC import *
from elevator import Elevator, Plotter
from controller import MainController

aantal_liften = int(input("Hoeveel liften?"))
print()

elevatorsClass=[]
elevators=[]
for x in range(0, aantal_liften):
    elevator = {}

    #floors = int(input("hoeveel vloeren heeft lift {} ?".format(x)))
    floors = 3
    elevator['floors'] = floors

    #floorsMax = int(input("hoogste verdieping die lift {} kan gaan ?".format(x)))
    floorsMax = 3
    elevator['floorsMax'] = floorsMax

    #express = bool(input("is lift {} een express lift? voer 0 of 1 in. ".format(x)))
    express = 1
    elevator['express'] = express

    #e = Elevator(x, floors, floorsMax, express)
    elevatorsClass.append(Elevator(x, floors, floorsMax, express))
    elevator['elevator'] = elevatorsClass[-1]

    elevators.append(elevator)

m = MainController(elevators)
g = Generator(elevators)

MainController.__setattr__('sweep', g.sweep)

World(*elevatorsClass, m)
