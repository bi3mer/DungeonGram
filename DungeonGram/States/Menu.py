from .State import State
import sys

class Menu(State):
    __slots__ = ['ready_to_transition']

    def __init__(self):
        self.ready_to_transition = False

    def on_enter(self):
        pass

    def on_exit(self):
        pass

    def update(self):
        pass

    def draw(self):
        print('Welcome to DungoenGram!')
        print()
        print()
        print()
        print('You are the @ character the screen. Avoid or attack the enemies!')
        print()
        print()
        print('Enter A to move left.')
        print('Enter S to move down.')
        print('Enter D to move right.')
        print('Enter W to move up.')
        print()
        print()
        print('Press enter to start. Q and enter to quit.')
        key_press = input()

        if key_press == 'q':
            print(chr(27) + "[2J") # clear the terminal
            sys.exit(1)

        self.ready_to_transition = True

    def should_transition(self):
        return self.ready_to_transition