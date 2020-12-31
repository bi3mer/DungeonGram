from DungeonGram.States import *

def main():
    menu_state = Menu()
    game_state = Game()
    death_state = Death()

    state = menu_state
    state_enum = 0

    while True:
        print(chr(27) + "[2J") # clear the terminal
        state.draw()
        state.update()

        if state.should_transition():
            if state_enum == 0:
                state = game_state
                state_enum = 1
            elif state_enum == 1:
                state.reset()
                state = death_state
                state_enum = 2
            else:
                state = menu_state
                state_enum = 0

if __name__ == "__main__":
    main()