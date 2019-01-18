from SimPyLC import *

class MainController(Module):
    def __init__(self, *elevators):
        Module.__init__(self)

        self.page('Main Controller')
        self.group('Run', True)
        self.runner = Runner()

        for i in range(len(elevators)):
            self.group('Elevator' + str(i + 1))
            setattr(self, 'elevator{}'.format(i), elevators[i]['elevator'])
            setattr(self, 'down{}'.format(i), Register())
            setattr(self, 'empty{}'.format(i), Register())
            setattr(self, 'available{}'.format(i), Marker())
            setattr(self, 'setDes{}'.format(i), Register())
            setattr(self, 'error{}'.format(i), Register())
            setattr(self, 'errorm{}'.format(i), Register())
            setattr(self, 'go{}'.format(i), Marker())

        self.group('Building Floors', True)
        for i in range(len(elevators)):
            for n in range(elevators[i]['floors']):
                self.group('Floor Level {}'.format(n))
                setattr(self, 'up{}'.format(i), Marker(False))
                setattr(self, 'down{}'.format(i), Marker(False))
                setattr(self, 'people{}'.format(i), Register())
                setattr(self, 'floorclosed{}{}'.format(i, n), Marker(True))
                setattr(self, 'closed{}{}'.format(i, n), Marker(True))
                # FIXME what is diff btwn floorclosed and closed?!?!

        self.group('Debug')
        self.chosen = Register()
        self.movement_done = Marker(True)

    def sweep(self):
        getattr(self, 'update{}'.format(i))()
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
               # if self.available1 == 0 and self.elevator0.get_level() == 0:
                    #destination == 1
                #self.chosen.set(0)
                #self.setDes1.set(1)
                    #elif self.available1 and self.elevator0.get_level() == 0 and self.chosen == 0:
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
        self.elevator0.add_people(self.people0)
        self.people0.set(0)
        print("the end")
    
    def test_chosenfunc(self):
        if self.movement_done and self.chosen == 1:
            self.setDes1.set(1) 
            self.people0.set(5) 
            #self.elevator0.add_people(self.people0)
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
                    #self.elevator0.add_people(self.people0)
            #if self.chosen == 1:
                #self.movement_done.mark(False)

            print("kom ik hier ?")
            #removepeople = self.people0 * -1
            #self.elevator0.add_people(removepeople)
            #self.people0.set(0)
            #self.chosen.set(0)
            #sleep(3)
        #elif self.chosen == 1 and not self.movement_done:
         #   self.chosen.set(0)
          #  self.people0.set(0)
            #removepeople = self.people0 * -1
            #self.elevator0.add_people(removepeople)
           ## self.elevator0.People = 0

    def test_movement(self):
        if self.people0 > 0 and self.movement_done:
            if self.lvl1: # lift 1 gaat van beganegrond naar verdieping 1
                self.setDes1.set(1)
                self.closed1.mark(False)
                self.elevator0.add_people(self.people0)
                print("People set to elevator0")
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
                self.elevator0.add_people(self.people1)
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
                if self.available1 == 0 and self.elevator0.get_level() == 0 and not self.closed1 and self.chosen == 1:  # Lege lift op 0 en deur open, lift gaat naar bestemming
                    self.setDes1.set(1)
                    self.elevator0.add_people(self.people0)
                    self.people0.set(0)
                    self.closed1.mark(True)
                    sleep(3)
                    self.go1.mark(True)
                    self.lvl1.mark(False)
                    self.movement_done.mark(False)
                elif self.available1 and self.elevator0.get_level() == 0 and self.closed1 and self.chosen == 1:  # Lege lift op 0 en deur dicht, deur gaat open
                    self.closed1.mark(False)
                    sleep(1)
                elif self.available1 and self.elevator0.get_level() == 0 and self.chosen == 0:  # Lege lift op andere verdieping wordt opgeroepen
                    self.chosen.set(1)

                elif self.available2 and self.elevator1.get_level() == 0 and not self.closed2 and self.chosen == 2:
                    self.setDes2.set(1)
                    self.elevator1.add_people(self.people0)
                    self.people0.set(0)
                    self.closed2.mark(True)
                    sleep(3)
                    self.go2.mark(True)
                    self.lvl1.mark(False)
                    self.movement_done.mark(False)
                elif self.available2 and self.elevator1.get_level() == 0 and self.closed2 and self.chosen == 2:
                    self.closed2.mark(False)
                    sleep(1)
                elif self.available2 and self.elevator1.get_level() == 0 and self.chosen == 0:
                    self.chosen.set(2)

                elif self.available3 and self.elevator2.get_level() == 0 and not self.closed3 and self.chosen == 3:  # Lege lift op 0 en deur open, lift gaat naar bestemming
                    self.setDes3.set(1)
                    self.elevator2.add_people(self.people0)
                    self.people0.set(0)
                    self.closed3.mark(True)
                    sleep(3)
                    self.go3.mark(True)
                    self.lvl1.mark(False)
                    self.movement_done.mark(False)
                elif self.available3 and self.elevator2.get_level() == 0 and self.closed3 and self.chosen == 3:  # Lege lift op 0 en deur dicht, deur gaat open
                    self.closed3.mark(False)
                    sleep(1)
                elif self.available3 and self.elevator2.get_level() == 0 and self.chosen == 0:  # Lege lift op andere verdieping wordt opgeroepen
                    self.chosen.set(3)

            elif self.lvl2:
                if self.available1 and self.elevator0.get_level() == 0 and not self.closed1 and self.chosen == 1:  # Lege lift op 0 en deur open, lift gaat naar bestemming
                    self.setDes1.set(2)
                    self.elevator0.add_people(self.people0)
                    self.people0.set(0)
                    self.closed1.mark(True)
                    sleep(3)
                    self.go1.mark(True)
                    self.lvl2.mark(False)
                    self.movement_done.mark(False)
                elif self.available1 and self.elevator0.get_level() == 0 and self.closed1 and self.chosen == 1:  # Lege lift op 0 en deur dicht, deur gaat open
                    self.closed1.mark(False)
                    sleep(1)
                elif self.available1 and self.elevator0.get_level() == 0 and self.chosen == 0:  # Lege lift op andere verdieping wordt opgeroepen
                    self.chosen.set(1)

                elif self.available2 and self.elevator1.get_level() == 0 and not self.closed2 and self.chosen == 2:
                    self.setDes2.set(2)
                    self.elevator1.add_people(self.people0)
                    self.people0.set(0)
                    self.closed2.mark(True)
                    sleep(3)
                    self.go2.mark(True)
                    self.lvl2.mark(False)
                    self.movement_done.mark(False)
                elif self.available2 and self.elevator1.get_level() == 0 and self.closed2 and self.chosen == 2:
                    self.closed2.mark(False)
                    sleep(1)
                elif self.available2 and self.elevator1.get_level() == 0 and self.chosen == 0:
                    self.chosen.set(2)

                elif self.available3 and self.elevator2.get_level() == 0 and not self.closed3 and self.chosen == 3:  # Lege lift op 0 en deur open, lift gaat naar bestemming
                    self.setDes3.set(2)
                    self.elevator2.add_people(self.people0)
                    self.people0.set(0)
                    self.closed3.mark(True)
                    sleep(3)
                    self.go3.mark(True)
                    self.lvl2.mark(False)
                    self.movement_done.mark(False)
                elif self.available3 and self.elevator2.get_level() == 0 and self.closed3 and self.chosen == 3:  # Lege lift op 0 en deur dicht, deur gaat open
                    self.closed3.mark(False)
                    sleep(1)
                elif self.available3 and self.elevator2.get_level() == 0 and self.chosen == 0:  # Lege lift op andere verdieping wordt opgeroepen
                    self.chosen.set(3)

            elif self.lvl3:
                if self.available1 and self.elevator0.get_level() == 0 and not self.closed1 and self.chosen == 1:  # Lege lift op 0 en deur open, lift gaat naar bestemming
                    self.setDes1.set(3)
                    self.elevator0.add_people(self.people0)
                    self.people0.set(0)
                    self.closed1.mark(True)
                    sleep(3)
                    self.go1.mark(True)
                    self.lvl3.mark(False)
                    self.movement_done.mark(False)
                elif self.available1 and self.elevator0.get_level() == 0 and self.closed1 and self.chosen == 1:  # Lege lift op 0 en deur dicht, deur gaat open
                    self.closed1.mark(False)
                    sleep(1)
                elif self.available1 and self.elevator0.get_level() == 0 and self.chosen == 0:  # Lege lift op andere verdieping wordt opgeroepen
                    self.chosen.set(1)

                elif self.available2 and self.elevator1.get_level() == 0 and not self.closed2 and self.chosen == 2:
                    self.setDes2.set(3)
                    self.elevator1.add_people(self.people0)
                    self.people0.set(0)
                    self.closed2.mark(True)
                    sleep(3)
                    self.go2.mark(True)
                    self.lvl3.mark(False)
                    self.movement_done.mark(False)
                elif self.available2 and self.elevator1.get_level() == 0 and self.closed2 and self.chosen == 2:
                    self.closed2.mark(False)
                    sleep(1)
                elif self.available2 and self.elevator1.get_level() == 0 and self.chosen == 0:
                    self.chosen.set(2)

                elif self.available3 and self.elevator2.get_level() == 0 and not self.closed3 and self.chosen == 3:  # Lege lift op 0 en deur open, lift gaat naar bestemming
                    self.setDes3.set(3)
                    self.elevator2.add_people(self.people0)
                    self.people0.set(0)
                    self.closed3.mark(True)
                    sleep(3)
                    self.go3.mark(True)
                    self.lvl3.mark(False)
                    self.movement_done.mark(False)
                elif self.available3 and self.elevator2.get_level() == 0 and self.closed3 and self.chosen == 3:  # Lege lift op 0 en deur dicht, deur gaat open
                    self.closed3.mark(False)
                    sleep(1)
                elif self.available3 and self.elevator2.get_level() == 0 and self.chosen == 0:  # Lege lift op andere verdieping wordt opgeroepen
                    self.chosen.set(3)

            elif self.lvl1 or self.lvl2 or self.lvl3:
                if self.available1 and self.elevator0.get_level() == 1 and self.chosen == 0:
                    self.setDes1.set(0)
                    self.go1.mark(True)
                    self.chosen.set(1)
                elif self.available2 and self.elevator1.get_level() == 1 and self.chosen == 0:
                    self.setDes2.set(0)
                    self.go2.mark(True)
                    self.chosen.set(2)
                elif self.available3 and self.elevator2.get_level() == 1 and self.chosen == 0:
                    self.setDes3.set(0)
                    self.go3.mark(True)
                    self.chosen.set(3)

                if self.available1 and self.elevator0.get_level() == 2 and self.chosen == 0:
                    self.setDes1.set(0)
                    self.go1.mark(True)
                    self.chosen.set(1)
                elif self.available2 and self.elevator1.get_level() == 2 and self.chosen == 0:
                    self.setDes2.set(0)
                    self.go2.mark(True)
                    self.chosen.set(2)
                elif self.available3 and self.elevator2.get_level() == 2 and self.chosen == 0:
                    self.setDes3.set(0)
                    self.go3.mark(True)
                    self.chosen.set(3)

                if self.available1 and self.elevator0.get_level() == 3 and self.chosen == 0:
                    self.setDes1.set(0)
                    self.go1.mark(True)
                    self.chosen.set(1)
                elif self.available2 and self.elevator1.get_level() == 3 and self.chosen == 0:
                    self.setDes2.set(0)
                    self.go2.mark(True)
                    self.chosen.set(2)
                elif self.available3 and self.elevator2.get_level() == 3 and self.chosen == 0:
                    self.setDes3.set(0)
                    self.go3.mark(True)
                    self.chosen.set(3)
        # Door control
        elif not self.movement_done():
            if self.chosen == 1 and self.available1:
                if self.elevator0.get_level() == 1:
                    self.floorclosed11.mark(False)
                    sleep(1)
                    self.floorclosed11.mark(True)
                    self.movement_done.mark(True)
                    self.chosen.set(0)
                elif self.elevator0.get_level() == 2:
                    self.floorclosed21.mark(False)
                    sleep(1)
                    self.floorclosed21.mark(True)
                    self.movement_done.mark(True)
                    self.chosen.set(0)
                elif self.elevator0.get_level() == 3:
                    self.floorclosed31.mark(False)
                    sleep(1)
                    self.floorclosed31.mark(True)
                    self.movement_done.mark(True)
                    self.chosen.set(0)
            elif self.chosen == 2 and self.available2:
                if self.elevator1.get_level() == 1:
                    self.floorclosed12.mark(False)
                    sleep(1)
                    self.floorclosed12.mark(True)
                    self.movement_done.mark(True)
                    self.chosen.set(0)
                elif self.elevator1.get_level() == 2:
                    self.floorclosed22.mark(False)
                    sleep(1)
                    self.floorclosed22.mark(True)
                    self.movement_done.mark(True)
                    self.chosen.set(0)
                elif self.elevator1.get_level() == 3:
                    self.floorclosed32.mark(False)
                    sleep(1)
                    self.floorclosed32.mark(True)
                    self.movement_done.mark(True)
                    self.chosen.set(0)
            elif self.chosen == 3 and self.available3:
                if self.elevator2.get_level() == 1:
                    self.floorclosed13.mark(False)
                    sleep(1)
                    self.floorclosed13.mark(True)
                    self.movement_done.mark(True)
                    self.chosen.set(0)
                elif self.elevator2.get_level() == 2:
                    self.floorclosed23.mark(False)
                    sleep(1)
                    self.floorclosed23.mark(True)
                    self.movement_done.mark(True)
                    self.chosen.set(0)
                elif self.elevator2.get_level() == 3:
                    self.floorclosed33.mark(False)
                    sleep(1)
                    self.floorclosed33.mark(True)
                    self.movement_done.mark(True)
                    self.chosen.set(0)

    def update1(self):
        self.empty1.set(self.elevator0.get_empty())
        self.error1.set(self.elevator0.get_error())
        if self.elevator0.get_level() == self.elevator0.get_destination() and not self.elevator0.get_keyoverride() and self.error1 == 0:
            self.available1.mark(True)
        else:
            self.available1.mark(False)

        if self.go1:
            self.go1.mark(False)
            self.elevator0.set_destination(self.setDes1())
            self.elevator0.start()

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
        self.empty2.set(self.elevator1.get_empty())
        self.error2.set(self.elevator1.get_error())
        if self.elevator1.get_level() == self.elevator1.get_destination() and not self.elevator1.get_keyoverride() and self.error2 == 0:
            self.available2.mark(True)
        else:
            self.available2.mark(False)

        if self.go2:
            self.go2.mark(False)
            self.elevator1.set_destination(self.setDes2())
            self.elevator1.start()

        if self.error2 == 0:
            self.errorm2.set("ok")
        elif self.error2 == 1:
            self.errorm2.set("Too much weight")
        elif self.error2 == 2:
            self.errorm2.set("EmergencyButton pressed")
        elif self.error2 == 3:
            self.errorm2.set("EmergencyBreak kicked in")

    def update3(self):
        self.empty3.set(self.elevator2.get_empty())
        self.error3.set(self.elevator2.get_error())
        if self.elevator2.get_level() == self.elevator2.get_destination() and not self.elevator2.get_keyoverride() and self.error3 == 0:
            self.available3.mark(True)
        else:
            self.available3.mark(False)

        if self.go3:
            self.go3.mark(False)
            self.elevator2.set_destination(self.setDes3())
            self.elevator2.start()

        if self.error3 == 0:
            self.errorm3.set("ok")
        elif self.error3 == 1:
            self.errorm3.set("Too much weight")
        elif self.error3 == 2:
            self.errorm3.set("EmergencyButton pressed")
        elif self.error3 == 3:
            self.errorm3.set("EmergencyBreak kicked in")
