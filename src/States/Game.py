from .State import State

class Game(State):
    __slots__ = ['ready_to_transition']

    def __init__(self):
        self.ready_to_transition = False

    def update(self):
        pass

    def draw(self):
        print('In game!')
        input()
        self.ready_to_transition = True

    def should_transition(self):
        return self.ready_to_transition