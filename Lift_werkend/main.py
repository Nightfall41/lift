from SimPyLC import *
from elevator import Elevator, Plotter
from controller import MainController

aantal_liften = int(input("Hoeveel liften?"))
print()

elevators=[]
for x in range(0, aantal_liften):
    floors=int(input("hoeveel vloeren heeft lift {} ?".format(x)))
    print()
    floorheight=int(input("hoogste verdieping die lift {} kan gaan ?".format(x)))
    print()
    expressLift=bool(input("is lift {} een express lift? voer 0 of 1 in. ".format(x)))
    print()
    elevators.append(Elevator(x,floors,floorheight,expressLift))

m = MainController(elevators)
World(*elevators, m)
