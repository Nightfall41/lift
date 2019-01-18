from SimPyLC import *


class MainController(Module):
    def __init__(self, elevators):
        self.elevator1 = elevators[0]
        self.elevator2 = elevators[1]
        self.elevator3 = elevators[2]
        Module.__init__(self)
        self.page('Main Controller')
        self.group('Run', True)
        self.runner = Runner()

        self.group('Elevator 1')
        self.empty1 = Register()
        self.available1 = Marker()
        self.setDes1 = Register()
        self.error1 = Register()
        self.errorm1 = Register()
        self.go1 = Marker()

        self.group('Elevator 2')
        self.empty2 = Register()
        self.available2 = Marker()
        self.setDes2 = Register()
        self.error2 = Register()
        self.errorm2 = Register()
        self.go2 = Marker()

        self.group('Elevator 3')
        self.empty3 = Register()
        self.available3 = Marker()
        self.setDes3 = Register()
        self.error3 = Register()
        self.errorm3 = Register()
        self.go3 = Marker()

        self.group('Building Floors', True)
        self.group('Floor Level 3')
        self.down3 = Marker(False)
        self.people3 = Register()
        self.floorclosed31 = Marker(True)
        self.floorclosed32 = Marker(True)
        self.floorclosed33 = Marker(True)

        self.group('Floor Level 2')
        self.up2 = Marker(False)
        self.down2 = Marker(False)
        self.people2 = Register()
        self.floorclosed21 = Marker(True)
        self.floorclosed22 = Marker(True)
        self.floorclosed23 = Marker(True)

        self.group('Floor Level 1')
        self.up1 = Marker(False)
        self.down1 = Marker(False)
        self.people1 = Register()
        self.floorclosed11 = Marker(True)
        self.floorclosed12 = Marker(True)
        self.floorclosed13 = Marker(True)

        self.group('Floor Level 0')
        self.lvl1 = Marker(False)
        self.lvl2 = Marker(False)
        self.lvl3 = Marker(False)
        self.closed1 = Marker(True)
        self.closed2 = Marker(True)
        self.closed3 = Marker(True)
        self.people0 = Register()

        self.group('Debug')
        self.chosen = Register()
        self.movement_done = Marker(True)

    def sweep(self):
        # updaters
        self.update1()
        self.update2()
        #self.update3()
        #self.algorithm()
        #self.testen()
        #self.switch_destination()
        #self.test_movement()
        self.test_people()
        #self.people0.set(0)
        #self.test_chosenfunc()


    def testen(self):
        #if self.people0 == 1  and self.movement_done:
         if self.people0 > 0 and self.movement_done:
            #self.test_function()
            #self.chosen.set(0)
            self.switch_destination(2)
         else: 
            self.setDes1.set(0)
            self.chosen.set(1)
               # if self.available1 == 0 and self.elevator1.get_level() == 0:
                    #destination == 1
                #self.chosen.set(0)
                #self.setDes1.set(1)
                    #elif self.available1 and self.elevator1.get_level() == 0 and self.chosen == 0:
                     #   self.chosen.set(1)
                      #  destination == 0

    def switch_destination(self, argument1):
        destination = {
            1: self.setDes1.set(0),
            2: self.setDes1.set(1),
            3: self.setDes1.set(2),
            4: self.setDes1.set(3)
        }
        return destination.get(argument1)

    def test_function(self):
        self.setDes1.set(1)
        self.elevator1.add_people(self.people0)
        self.people0.set(0)
        print("the end")
    
    def test_chosenfunc(self):
        if self.movement_done and self.chosen == 1:
            self.setDes1.set(1) 
            self.people0.set(5) 
            #self.elevator1.add_people(self.people0)
            print("Kom ik wel hier ?")
            sleep(3)
        elif self.chosen == 0: 
            self.people0.set(0) 
            self.setDes1.set(0)
             
        

    def test_people(self):
        if self.people0 > 0 and self.movement_done:
            self.setDes1.set(1)
            self.chosen.set(1)
        elif self.chosen == 1 and self.setDes1 == 1:
            self.setDes1.set(0)
                    #self.elevator1.add_people(self.people0)
            #if self.chosen == 1:
                #self.movement_done.mark(False)

            print("kom ik hier ?")
            #removepeople = self.people0 * -1
            #self.elevator1.add_people(removepeople)
            #self.people0.set(0)
            #self.chosen.set(0)
            #sleep(3)
        #elif self.chosen == 1 and not self.movement_done:
         #   self.chosen.set(0)
          #  self.people0.set(0)
            #removepeople = self.people0 * -1
            #self.elevator1.add_people(removepeople)
           ## self.elevator1.People = 0

    def test_movement(self):
        if self.people0 > 0 and self.movement_done:
            if self.lvl1: # lift 1 gaat van beganegrond naar verdieping 1
                self.setDes1.set(1)
                self.closed1.mark(False)
                self.elevator1.add_people(self.people0)
                print("People set to elevator1")
                self.people1.set(self.people0)
                print("People set to floor 1")
                self.people0.set(1)
                print("Kom ik hier doorheen")
                self.closed1.mark(True)  
                sleep(3)
                self.go1.mark(True)
                self.lvl1.mark(False)
                self.movement_done.mark(False)
            elif self.lvl2: # lift 1 gaat van verdieping 1 naar beganegrond
                self.setDes1.set(0)
                self.elevator1.add_people(self.people1)
                sleep(3)
                self.go1.mark(True)
                self.lvl2.mark(False)
                self.movement_done.mark(False)

    def test_movement1(self):
        if self.people0 > 0 and self.movement_done:
            if self.lvl1: # lift 1 gaat van beganegrond naar verdieping 1
                self.setDes1.set(1)

    def algorithm(self):
        # algoritme aantal mensen van begane grond naar verdieping 1, 2 of 3
        if self.people0 > 0 and self.movement_done:
            if self.lvl1:
                if self.available1 == 0 and self.elevator1.get_level() == 0 and not self.closed1 and self.chosen == 1:  # Lege lift op 0 en deur open, lift gaat naar bestemming
                    self.setDes1.set(1)
                    self.elevator1.add_people(self.people0)
                    self.people0.set(0)
                    self.closed1.mark(True)
                    sleep(3)
                    self.go1.mark(True)
                    self.lvl1.mark(False)
                    self.movement_done.mark(False)
                elif self.available1 and self.elevator1.get_level() == 0 and self.closed1 and self.chosen == 1:  # Lege lift op 0 en deur dicht, deur gaat open
                    self.closed1.mark(False)
                    sleep(1)
                elif self.available1 and self.elevator1.get_level() == 0 and self.chosen == 0:  # Lege lift op andere verdieping wordt opgeroepen
                    self.chosen.set(1)

                elif self.available2 and self.elevator2.get_level() == 0 and not self.closed2 and self.chosen == 2:
                    self.setDes2.set(1)
                    self.elevator2.add_people(self.people0)
                    self.people0.set(0)
                    self.closed2.mark(True)
                    sleep(3)
                    self.go2.mark(True)
                    self.lvl1.mark(False)
                    self.movement_done.mark(False)
                elif self.available2 and self.elevator2.get_level() == 0 and self.closed2 and self.chosen == 2:
                    self.closed2.mark(False)
                    sleep(1)
                elif self.available2 and self.elevator2.get_level() == 0 and self.chosen == 0:
                    self.chosen.set(2)

                elif self.available3 and self.elevator3.get_level() == 0 and not self.closed3 and self.chosen == 3:  # Lege lift op 0 en deur open, lift gaat naar bestemming
                    self.setDes3.set(1)
                    self.elevator3.add_people(self.people0)
                    self.people0.set(0)
                    self.closed3.mark(True)
                    sleep(3)
                    self.go3.mark(True)
                    self.lvl1.mark(False)
                    self.movement_done.mark(False)
                elif self.available3 and self.elevator3.get_level() == 0 and self.closed3 and self.chosen == 3:  # Lege lift op 0 en deur dicht, deur gaat open
                    self.closed3.mark(False)
                    sleep(1)
                elif self.available3 and self.elevator3.get_level() == 0 and self.chosen == 0:  # Lege lift op andere verdieping wordt opgeroepen
                    self.chosen.set(3)

            elif self.lvl2:
                if self.available1 and self.elevator1.get_level() == 0 and not self.closed1 and self.chosen == 1:  # Lege lift op 0 en deur open, lift gaat naar bestemming
                    self.setDes1.set(2)
                    self.elevator1.add_people(self.people0)
                    self.people0.set(0)
                    self.closed1.mark(True)
                    sleep(3)
                    self.go1.mark(True)
                    self.lvl2.mark(False)
                    self.movement_done.mark(False)
                elif self.available1 and self.elevator1.get_level() == 0 and self.closed1 and self.chosen == 1:  # Lege lift op 0 en deur dicht, deur gaat open
                    self.closed1.mark(False)
                    sleep(1)
                elif self.available1 and self.elevator1.get_level() == 0 and self.chosen == 0:  # Lege lift op andere verdieping wordt opgeroepen
                    self.chosen.set(1)

                elif self.available2 and self.elevator2.get_level() == 0 and not self.closed2 and self.chosen == 2:
                    self.setDes2.set(2)
                    self.elevator2.add_people(self.people0)
                    self.people0.set(0)
                    self.closed2.mark(True)
                    sleep(3)
                    self.go2.mark(True)
                    self.lvl2.mark(False)
                    self.movement_done.mark(False)
                elif self.available2 and self.elevator2.get_level() == 0 and self.closed2 and self.chosen == 2:
                    self.closed2.mark(False)
                    sleep(1)
                elif self.available2 and self.elevator2.get_level() == 0 and self.chosen == 0:
                    self.chosen.set(2)

                elif self.available3 and self.elevator3.get_level() == 0 and not self.closed3 and self.chosen == 3:  # Lege lift op 0 en deur open, lift gaat naar bestemming
                    self.setDes3.set(2)
                    self.elevator3.add_people(self.people0)
                    self.people0.set(0)
                    self.closed3.mark(True)
                    sleep(3)
                    self.go3.mark(True)
                    self.lvl2.mark(False)
                    self.movement_done.mark(False)
                elif self.available3 and self.elevator3.get_level() == 0 and self.closed3 and self.chosen == 3:  # Lege lift op 0 en deur dicht, deur gaat open
                    self.closed3.mark(False)
                    sleep(1)
                elif self.available3 and self.elevator3.get_level() == 0 and self.chosen == 0:  # Lege lift op andere verdieping wordt opgeroepen
                    self.chosen.set(3)

            elif self.lvl3:
                if self.available1 and self.elevator1.get_level() == 0 and not self.closed1 and self.chosen == 1:  # Lege lift op 0 en deur open, lift gaat naar bestemming
                    self.setDes1.set(3)
                    self.elevator1.add_people(self.people0)
                    self.people0.set(0)
                    self.closed1.mark(True)
                    sleep(3)
                    self.go1.mark(True)
                    self.lvl3.mark(False)
                    self.movement_done.mark(False)
                elif self.available1 and self.elevator1.get_level() == 0 and self.closed1 and self.chosen == 1:  # Lege lift op 0 en deur dicht, deur gaat open
                    self.closed1.mark(False)
                    sleep(1)
                elif self.available1 and self.elevator1.get_level() == 0 and self.chosen == 0:  # Lege lift op andere verdieping wordt opgeroepen
                    self.chosen.set(1)

                elif self.available2 and self.elevator2.get_level() == 0 and not self.closed2 and self.chosen == 2:
                    self.setDes2.set(3)
                    self.elevator2.add_people(self.people0)
                    self.people0.set(0)
                    self.closed2.mark(True)
                    sleep(3)
                    self.go2.mark(True)
                    self.lvl3.mark(False)
                    self.movement_done.mark(False)
                elif self.available2 and self.elevator2.get_level() == 0 and self.closed2 and self.chosen == 2:
                    self.closed2.mark(False)
                    sleep(1)
                elif self.available2 and self.elevator2.get_level() == 0 and self.chosen == 0:
                    self.chosen.set(2)

                elif self.available3 and self.elevator3.get_level() == 0 and not self.closed3 and self.chosen == 3:  # Lege lift op 0 en deur open, lift gaat naar bestemming
                    self.setDes3.set(3)
                    self.elevator3.add_people(self.people0)
                    self.people0.set(0)
                    self.closed3.mark(True)
                    sleep(3)
                    self.go3.mark(True)
                    self.lvl3.mark(False)
                    self.movement_done.mark(False)
                elif self.available3 and self.elevator3.get_level() == 0 and self.closed3 and self.chosen == 3:  # Lege lift op 0 en deur dicht, deur gaat open
                    self.closed3.mark(False)
                    sleep(1)
                elif self.available3 and self.elevator3.get_level() == 0 and self.chosen == 0:  # Lege lift op andere verdieping wordt opgeroepen
                    self.chosen.set(3)

            elif self.lvl1 or self.lvl2 or self.lvl3:
                if self.available1 and self.elevator1.get_level() == 1 and self.chosen == 0:
                    self.setDes1.set(0)
                    self.go1.mark(True)
                    self.chosen.set(1)
                elif self.available2 and self.elevator2.get_level() == 1 and self.chosen == 0:
                    self.setDes2.set(0)
                    self.go2.mark(True)
                    self.chosen.set(2)
                elif self.available3 and self.elevator3.get_level() == 1 and self.chosen == 0:
                    self.setDes3.set(0)
                    self.go3.mark(True)
                    self.chosen.set(3)

                if self.available1 and self.elevator1.get_level() == 2 and self.chosen == 0:
                    self.setDes1.set(0)
                    self.go1.mark(True)
                    self.chosen.set(1)
                elif self.available2 and self.elevator2.get_level() == 2 and self.chosen == 0:
                    self.setDes2.set(0)
                    self.go2.mark(True)
                    self.chosen.set(2)
                elif self.available3 and self.elevator3.get_level() == 2 and self.chosen == 0:
                    self.setDes3.set(0)
                    self.go3.mark(True)
                    self.chosen.set(3)

                if self.available1 and self.elevator1.get_level() == 3 and self.chosen == 0:
                    self.setDes1.set(0)
                    self.go1.mark(True)
                    self.chosen.set(1)
                elif self.available2 and self.elevator2.get_level() == 3 and self.chosen == 0:
                    self.setDes2.set(0)
                    self.go2.mark(True)
                    self.chosen.set(2)
                elif self.available3 and self.elevator3.get_level() == 3 and self.chosen == 0:
                    self.setDes3.set(0)
                    self.go3.mark(True)
                    self.chosen.set(3)
        # Door control
        elif not self.movement_done():
            if self.chosen == 1 and self.available1:
                if self.elevator1.get_level() == 1:
                    self.floorclosed11.mark(False)
                    sleep(1)
                    self.floorclosed11.mark(True)
                    self.movement_done.mark(True)
                    self.chosen.set(0)
                elif self.elevator1.get_level() == 2:
                    self.floorclosed21.mark(False)
                    sleep(1)
                    self.floorclosed21.mark(True)
                    self.movement_done.mark(True)
                    self.chosen.set(0)
                elif self.elevator1.get_level() == 3:
                    self.floorclosed31.mark(False)
                    sleep(1)
                    self.floorclosed31.mark(True)
                    self.movement_done.mark(True)
                    self.chosen.set(0)
            elif self.chosen == 2 and self.available2:
                if self.elevator2.get_level() == 1:
                    self.floorclosed12.mark(False)
                    sleep(1)
                    self.floorclosed12.mark(True)
                    self.movement_done.mark(True)
                    self.chosen.set(0)
                elif self.elevator2.get_level() == 2:
                    self.floorclosed22.mark(False)
                    sleep(1)
                    self.floorclosed22.mark(True)
                    self.movement_done.mark(True)
                    self.chosen.set(0)
                elif self.elevator2.get_level() == 3:
                    self.floorclosed32.mark(False)
                    sleep(1)
                    self.floorclosed32.mark(True)
                    self.movement_done.mark(True)
                    self.chosen.set(0)
            elif self.chosen == 3 and self.available3:
                if self.elevator3.get_level() == 1:
                    self.floorclosed13.mark(False)
                    sleep(1)
                    self.floorclosed13.mark(True)
                    self.movement_done.mark(True)
                    self.chosen.set(0)
                elif self.elevator3.get_level() == 2:
                    self.floorclosed23.mark(False)
                    sleep(1)
                    self.floorclosed23.mark(True)
                    self.movement_done.mark(True)
                    self.chosen.set(0)
                elif self.elevator3.get_level() == 3:
                    self.floorclosed33.mark(False)
                    sleep(1)
                    self.floorclosed33.mark(True)
                    self.movement_done.mark(True)
                    self.chosen.set(0)

    def update1(self):
        self.empty1.set(self.elevator1.get_empty())
        self.error1.set(self.elevator1.get_error())
        if self.elevator1.get_level() == self.elevator1.get_destination() and not self.elevator1.get_keyoverride() and self.error1 == 0:
            self.available1.mark(True)
        else:
            self.available1.mark(False)

        if self.go1:
            self.go1.mark(False)
            self.elevator1.set_destination(self.setDes1())
            self.elevator1.start()

        #if self.error1 == 0:
            #error1 = 1
        #elif self.error1 == 1:
            #error1 = 2
        #elif self.error1 == 2:
            #error1 = 3
        #elif self.error1 == 3:
            #error1 = 4

        if self.error1 == 0:
            self.errorm1.set("ok")
        elif self.error1 == 1:
            self.errorm1.set("Too much weight")
        elif self.error1 == 2:
            self.errorm1.set("EmergencyButton pressed")
        elif self.error1 == 3:
            self.errorm1.set("EmergencyBreak kicked in")

    def update2(self):
        self.empty2.set(self.elevator2.get_empty())
        self.error2.set(self.elevator2.get_error())
        if self.elevator2.get_level() == self.elevator2.get_destination() and not self.elevator2.get_keyoverride() and self.error2 == 0:
            self.available2.mark(True)
        else:
            self.available2.mark(False)

        if self.go2:
            self.go2.mark(False)
            self.elevator2.set_destination(self.setDes2())
            self.elevator2.start()

        if self.error2 == 0:
            self.errorm2.set("ok")
        elif self.error2 == 1:
            self.errorm2.set("Too much weight")
        elif self.error2 == 2:
            self.errorm2.set("EmergencyButton pressed")
        elif self.error2 == 3:
            self.errorm2.set("EmergencyBreak kicked in")

    def update3(self):
        self.empty3.set(self.elevator3.get_empty())
        self.error3.set(self.elevator3.get_error())
        if self.elevator3.get_level() == self.elevator3.get_destination() and not self.elevator3.get_keyoverride() and self.error3 == 0:
            self.available3.mark(True)
        else:
            self.available3.mark(False)

        if self.go3:
            self.go3.mark(False)
            self.elevator3.set_destination(self.setDes3())
            self.elevator3.start()

        if self.error3 == 0:
            self.errorm3.set("ok")
        elif self.error3 == 1:
            self.errorm3.set("Too much weight")
        elif self.error3 == 2:
            self.errorm3.set("EmergencyButton pressed")
        elif self.error3 == 3:
            self.errorm3.set("EmergencyBreak kicked in")
