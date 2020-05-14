import time


class Game:
    def __init__(self):
        super().__init__()
        self.initialize_game()

    # set initial state of game with no plays
    def initialize_game(self):
        self.current_state = [[".", ".", "."],
                              [".", ".", "."],
                              [".", ".", "."]]

        #player x will get first turn
        self.player_turn = "X"

    # print the current play board
    def draw_board(self):
        for i in range(3):
            for j in range(3):
                print(f"{self.current_state[i][j]}|", end=" ")
            print()
        print()

    # determine is a play is legal
    def is_valid(self, px, py):
        if px < 0 or py < 0 or px > 2 or py > 2:
            return False
        if self.current_state[px][py] != ".":
            return False
        return True

    
    # Check if game is ended and return winner if game over
    def is_end(self):
        # Vertical win
        for i in range(0, 3):
            if (self.current_state[0][i] != '.' and
                self.current_state[0][i] == self.current_state[1][i] and
                self.current_state[1][i] == self.current_state[2][i]):
                return self.current_state[0][i]

        # Horizontal win
        for i in range(0, 3):
            if (self.current_state[i] == ['X', 'X', 'X']):
                return 'X'
            elif (self.current_state[i] == ['O', 'O', 'O']):
                return 'O'

        # 1st diagonal win
        if (self.current_state[0][0] != '.' and
            self.current_state[0][0] == self.current_state[1][1] and
            self.current_state[0][0] == self.current_state[2][2]):
            return self.current_state[0][0]

        # 2nd diagonal win
        if (self.current_state[0][2] != '.' and
            self.current_state[0][2] == self.current_state[1][1] and
            self.current_state[0][2] == self.current_state[2][0]):
            return self.current_state[0][2]

        # Is whole board full?
        for i in range(0, 3):
            for j in range(0, 3):
                # There's an empty field, continue the game
                if (self.current_state[i][j] == '.'):
                    return None

        # It's a tie!
        return '.'


    def optimize(self, mx):
        
        # mx is multiplier +ve for max and -ve for min
        # Possible values for minv are:
        # -1 - win
        # 0  - a tie
        # 1  - loss

        # We're initially setting it to worse than the worst case:
        # 2 for min and -2 for max
        optimalv = (-2 * mx)

        px = None
        py = None

        result = self.is_end()

        if result == 'X':
            return (-1, 0, 0)
        elif result == 'O':
            return (1, 0, 0)
        elif result == '.':
            return (0, 0, 0)

        for i in range(0, 3):
            for j in range(0, 3):
                if self.current_state[i][j] == '.':
                    if mx < 0: self.current_state[i][j] = 'X'
                    if mx > 0: self.current_state[i][j] = 'O'
                    # On the empty field player 'O' makes a move and calls optimize with a -ve mx value (min)
                    # That's one branch of the game tree.
                    # the next turn, we reverse the mx sign to switch from max to min to max
                    (m, opt_i, opt_j) = self.optimize(-mx)
                    
                    # only update values if we are calculating max and value is greater
                    # or if we are minimizing and value is less
                    if (mx == 1 and m > optimalv) or (mx == -1 and m < optimalv):
                        optimalv = m
                        px = i
                        py = j
                    self.current_state[i][j] = '.'

        return (optimalv, px, py)

    def play(self):
        while True:
            self.draw_board()
            self.result = self.is_end()

            # Printing the appropriate message if the game has ended
            if self.result != None:
                if self.result == 'X':
                    print('The winner is X!')
                elif self.result == 'O':
                    print('The winner is O!')
                elif self.result == '.':
                    print("It's a tie!")

                self.initialize_game()
                return

            # If it's player's turn, optimize for min
            if self.player_turn == 'X':

                while True:

                    start = time.time()
                    (m, qx, qy) = self.optimize(-1)
                    end = time.time()
                    print('Evaluation time: {}s'.format(round(end - start, 7)))
                    print('Recommended move: X = {}, Y = {}'.format(qx, qy))

                    px = int(input('Insert the X coordinate: '))
                    py = int(input('Insert the Y coordinate: '))

                    (qx, qy) = (px, py)

                    if self.is_valid(px, py):
                        self.current_state[px][py] = 'X'
                        self.player_turn = 'O'
                        break
                    else:
                        print('The move is not valid! Try again.')

            # If it's AI's turn, optimize for max
            else:
                (m, px, py) = self.optimize(1)
                self.current_state[px][py] = 'O'
                self.player_turn = 'X'


def main():
    g = Game()
    g.play()

if __name__ == "__main__":
    main()