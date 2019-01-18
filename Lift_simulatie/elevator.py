from SimPyLC import *


class Elevator(Module):
    def __init__(self, number, floors, floorheight, express):
        Module.__init__(self, 'Elevator ' + str(number))
        self.page('Elevator ' + str(number))
        self.group('Timers', True)
        self.dt = Timer()
        self.runtime = Timer()
        self.runner = Runner()

        self.group('Building paramaters')
        self.floors = Register(floors)
        self.floorHeight = Register(floorheight)
        self.express = Marker(False)
        self.express.mark(True, floors >= 10 and express)

        self.bodyWeight = Register(50)

        self.group('Elevator panel', True)
        self.f0 = Marker(False)
        self.f1 = Marker(False)
        self.f2 = Marker(False)
        self.f3 = Marker(False)
        self.keyOverride = Marker(False)
        self.open = Marker(False)
        self.close = Marker(False)
        self.emergencyButton = Marker(False)

        self.group('Elevator Parameters')
        self.level = Register(0)
        self.position = Register(0)
        self.speed = Register(0.0)
        self.acceleration = Register(0.0)
        self.cargoWeight = Register(0.0)
        self.cablesOK = Marker(False)
        self.emergencyHatchOpen = Marker(False)
        self.lightsOn = Marker(False)
        self.motorPowerN = Register()
        self.maxCargoWeight = Register(1000)
        self.elevatorWeight = Register(500)
        self.overWeight = Marker(False)
        self.emergencyBreak = Marker(False)
        self.emergencyOverride = Marker(False)
        self.call911 = Marker(False)

        self.group('Debug')
        self.peopleInside = Register(0)
        self.maxAcceleration = Register(2.0)
        self.maxSpeed = Register(2.0)
        self.stop_at = Register(0)
        self.distanceToStop = Register()
        self.brakeDistance = Register(1.0)
        self.brakeUp = Marker(False)
        self.brakeDown = Marker(False)
        self.reset = Marker(False)
        self.goUp = Marker(False)
        self.goDown = Marker(False)
        self.go = Marker(False)
        self.oldPos = Register()
        self.errors = Marker()
        self.error = Register()

    def sweep(self):
        # updaters
        self.light_control()
        self.cable_check()
        self.weight_check()
        self.key_check()
        self.move_up_check()
        self.move_down_check()
        self.motorPowerN.set((self.cargoWeight + self.elevatorWeight) * self.acceleration)
        self.emergency_button_check()
        self.emergency_break_control()
        self.floor_indicator()
        self.errors_check()

        self.distanceToStop.set(self.stop_at * self.floorHeight - self.position)

        if not self.errors and not self.level == self.stop_at:  # if no errors the elevator works

            if self.stop_at > self.level and self.go:  # up
                # one time setup
                self.go.mark(False)
                self.goUp.mark(True)
                self.acceleration.set(self.maxAcceleration)
                self.dt.reset()
                self.oldPos.set(self.position)

            if self.stop_at < self.level and self.go:  # down
                # one time setup
                self.go.mark(False)
                self.goDown.mark(True)
                self.acceleration.set(0 - self.maxAcceleration)
                self.dt.reset()
                self.oldPos.set(self.position)
        else:
            self.goUp.mark(False)
            self.goDown.mark(False)
            self.acceleration.set(0.0)
            self.speed.set(0.0)

    def light_control(self):
        if self.cargoWeight > 10:
            self.lightsOn.mark(True)
        else:
            self.lightsOn.mark(False)

    def cable_check(self):
        if -3.0 < self.speed < 3.0:
            self.cablesOK.mark(True)
        else:
            self.cablesOK.mark(False)

    def weight_check(self):
        self.cargoWeight.set(self.bodyWeight * self.peopleInside)
        if self.cargoWeight > self.maxCargoWeight:
            self.overWeight.mark(True)
        else:
            self.overWeight.mark(False)

    def key_check(self):
        if self.keyOverride:
            self.emergencyOverride.mark(True)
        else:
            self.emergencyOverride.mark(False)

    def emergency_button_check(self):
        if self.emergencyButton:
            self.call911.mark(True)
        else:
            self.call911.mark(False)

    def emergency_break_control(self):
        if not self.cablesOK or self.emergencyHatchOpen:
            self.emergencyBreak.mark(True)
        else:
            self.emergencyBreak.mark(False)

    def floor_indicator(self):
        if self.stop_at == 0:
            self.f0.mark(True)
        elif self.stop_at == 1:
            self.f1.mark(True)
        elif self.stop_at == 2:
            self.f2.mark(True)
        elif self.stop_at == 3:
            self.f3.mark(True)
        else:
            self.f0.mark(False)
            self.f1.mark(False)
            self.f2.mark(False)
            self.f3.mark(False)

    def errors_check(self):
        if self.overWeight:
            self.error.set(1)
            self.errors.mark(True)
        elif self.emergencyButton:
            self.error.set(2)
            self.errors.mark(True)
        elif self.emergencyBreak:
            self.error.set(3)
            self.errors.mark(True)
        else:
            self.errors.mark(False)
            self.error.set(0)

    def move_up_check(self):
        # eenparige versnelde beweging
        if self.goUp and self.distanceToStop > self.brakeDistance:
            if self.speed < self.maxSpeed:
                # accelerate to 2.0 m/s
                v = self.acceleration * self.dt  # v = a * t
                s = 0.5 * v * self.dt  # s = 1/2at^2
                self.speed.set(v)
                self.position.set(self.oldPos + s)

                # constante snelheid
            elif self.speed >= self.maxSpeed:
                if not self.reset:
                    self.dt.reset()
                    self.acceleration.set(0.0)
                    self.oldPos.set(self.position)
                    self.reset.mark(True)
                # keep max speed 2.0 m/s
                self.speed.set(self.maxSpeed)
                s = self.speed * self.dt  # s = v * t
                self.position.set(self.oldPos + s)

        elif self.goUp:
            self.goUp.mark(False)
            self.brakeUp.mark(True)
            self.dt.reset()
            self.oldPos.set(self.position)
            self.acceleration.set(0 - self.maxAcceleration)

            # eenparige vertraagde beweging
        if self.brakeUp and self.speed > 0.0:
            # brake from 2.0 m/s to 0.0m/s
            # s = brakeDistance + 1/2a(t-brakeDistance)^2
            s = self.brakeDistance + 0.5 * self.acceleration * (self.dt - self.brakeDistance) * (self.dt - self.brakeDistance)
            self.position.set(self.oldPos + s)
            v = self.maxSpeed + self.acceleration * self.dt  # v = v0 + a * t
            self.speed.set(v)

        elif self.brakeUp:
            self.brakeUp.mark(False)
            self.peopleInside.set(0)
            # correction
            self.speed.set(0.0)
            self.acceleration.set(0.0)
            self.position.set(self.stop_at * self.floorHeight)
            self.current_level()
            self.reset.mark(False)

    def move_down_check(self):
        if self.goDown and self.distanceToStop < (0.0 - self.brakeDistance):
            if self.speed > (0.0 - self.maxSpeed):
                # accelerate to -2.0 m/s
                v = self.acceleration * self.dt  # v = a * t
                s = 0.5 * v * self.dt  # s = 1/2at^2
                self.speed.set(v)
                self.position.set(self.oldPos + s)

                # constante snelheid
            elif self.speed <= (0.0 - self.maxSpeed):
                if not self.reset:
                    self.dt.reset()
                    self.acceleration.set(0.0)
                    self.oldPos.set(self.position)
                    self.reset.mark(True)
                # keep max speed 2.0 m/s
                self.speed.set(0.0 - self.maxSpeed)
                s = self.speed * self.dt  # s = v * t
                self.position.set(self.oldPos + s)

        elif self.goDown:
            self.goDown.mark(False)
            self.brakeDown.mark(True)
            self.dt.reset()
            self.oldPos.set(self.position)
            self.acceleration.set(self.maxAcceleration)

        if self.brakeDown and self.speed <= 0.0:
            # brake from -2.0 m/s to 0.0m/s
            # s = 1/2a(t-brakeDistance)^2 -brakeDistance
            s = 0.5 * self.acceleration * (self.dt - self.brakeDistance) * (self.dt - self.brakeDistance) - self.brakeDistance
            self.position.set(self.oldPos + s)
            v = (0.0 - self.maxSpeed) + self.acceleration * self.dt  # v = v0 + a * t
            self.speed.set(v)

        elif self.brakeDown:
            self.brakeDown.mark(False)
            self.peopleInside.set(0)
            # correction
            self.speed.set(0.0)
            self.acceleration.set(0.0)
            self.position.set(self.stop_at * self.floorHeight)
            self.current_level()
            self.reset.mark(False)

    def current_level(self):
        self.level.set(self.position / self.floorHeight)

# getters and setters

    def get_keyoverride(self):
        if self.keyOverride:
            return True
        return False

    def get_level(self):
        return self.level()

    def get_error(self):
        return self.error()

    def get_empty(self):
        if self.cargoWeight == 0:
            return True
        else:
            return False

    def get_destination(self):
        return self.stop_at()

    def add_people(self, people):
        self.peopleInside.set(self.peopleInside + people)

    def set_destination(self, level):
        self.stop_at.set(level)

    def start(self):
        self.go.mark(True)


class Plotter(Chart):
    def __init__(self, number, elevator):
        self.elevator = elevator
        Chart.__init__(self, 'Elevator ' + str(number))

    def define(self):
        self.channel(self.elevator.position, (0.0, 1.0, 1.0), 0, self.elevator.floorHeight * (self.elevator.floors - 1), 200)
        self.channel(self.elevator.speed, (0.0, 1.0, 0.0), -2, 2, 100)
        self.channel(self.elevator.acceleration, (1.0, 0.0, 0.0), -2, 2, 100)
