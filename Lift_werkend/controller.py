from SimPyLC import *

class MainController(Module):
    def __init__(self, elevators):
        generator = Generator()

        for i in range(len(elevators)):
            setattr(self, 'update{}'.format(i), generator.update(self, elevators[i]))
        self.sweep = generator.sweep(elevators)

        # initialize SimPyLC
        Module.__init__(self)

        self.page('Main Controller')
        self.group('Run', True)
        self.runner = Runner()

        # elevator properties
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

        # floor properties
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

        # XXX debug code
        self.group('Debug')
        self.chosen = Register()
        self.movement_done = Marker(True)
