from SimPyLC import World
from elevator import Elevator, Plotter
from controller import MainController



#aantal_liften = int(input("Hoeveel liften?")) # bijv 5 liften? tik dit in als 0 1 2 3 4
#lijst = []
#
#
#print("voer alleen integers in.")
#print()
#lijst_van_lift_objecten=[]
#for x in range(0, aantal_liften):
#    floors=int(input("hoeveel vloeren heeft lift {} ?".format(x)))
#    print()
#    floorheight=int(input("hoogste verdieping die lift {} kan gaan ?".format(x)))
#    print()
#    expressLift=bool(input("is lift {} een express lift? voer 0 of 1 in. ".format(x)))
#    print()
#    lijst_van_lift_objecten.append(Elevator(x,floors,floorheight,expressLift))

#m = ClassWrapper(MainController, lijst_van_lift_objecten)

slist = [Elevator(1, 10, 10, False), Elevator(1, 10, 10, False), Elevator(1, 10, 10, False)]
e1 = Elevator(1, 10, 10, False)  # Elevator(number, floors, floorheight, express lift?)
e2 = Elevator(2, 4, 10, False)  # Elevator(number, floors, floorheight, express lift?)
e3 = Elevator(3, 4, 10, False)  # Elevator(number, floors, floorheight, express lift?)

m = MainController(e1, e2, e3)
World(e1, e2, e3, m)
#m = MainController(*slist)
#World(slist[0], slist[1], slist[2], m)

#m = MainController(lijst_van_lift_objecten)
#ClassWrapper(World, lijst_van_lift_objecten)
#World(*lijst_van_lift_objecten, m)
