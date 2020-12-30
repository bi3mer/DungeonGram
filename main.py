from src.States import *

def main():
    state = Menu()
    state_enum = 0

    while True:
        print(chr(27) + "[2J") # clear the terminal
        state.update()
        state.draw()

        if state.should_transition():
            if state_enum == 0:
                state = Game()
                state_enum = 1
            elif state_enum == 1:
                state = Death()
                state_enum = 2
            else:
                state = Menu()
                state_enum = 0

if __name__ == "__main__":
    main()