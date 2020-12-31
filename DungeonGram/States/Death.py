from .State import State
import sys

class Death(State):
    __slots__ = ['ready_to_transition']

    def __init__(self):
        self.ready_to_transition = False

    def update(self):
        pass

    def draw(self):
        print('You have died. Press enter to go back to the main menu. Or q to quit.')

        if 'q' == input():
            print(chr(27) + "[2J") # clear the terminal
            sys.exit(0)

        self.ready_to_transition = True

    def should_transition(self):
        return self.ready_to_transition