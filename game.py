inf = float("inf")
class Game:
    def __init__(self, id):
        self.p1went = False
        self.p2went = False
        self.id = id
        self.wins = {'X': 0, 'O': 0}
        self.ready = False
        self.game_array = [[inf, inf, inf],
                           [inf, inf, inf],
                           [inf, inf, inf]]
        self.possible_matches = [[(0, 0), (0, 1), (0, 2)],
                                 [(1, 0), (1, 1), (1, 2)],
                                 [(2, 0), (2, 1), (2, 2)],
                                 [(0, 0), (1, 0), (2, 0)],
                                 [(1, 0), (1, 1), (1, 2)],
                                 [(2, 0), (2, 1), (2, 2)],
                                 [(0, 0), (1, 1), (2, 2)],
                                 [(0, 2), (1, 1), (2, 0)],
                                 [(0, 1), (1, 1), (2, 1)]]
        self.winner = -1
        self.winner_coordinates = None

    def isReady(self):
        return self.ready

    def play(self, player, cell):
        """
        Update the game array with 'X' (corresponding to 1) and 'O' (corresponding to 0), 
        and get the cell which is to be updated within the game array.

        """
        # convert cell to a list from string
        cell = [int(i) for i in cell.split(',')]
        print("Inside game.play!", cell)
        if self.game_array[cell[1]][cell[0]] == inf:
            print("Inside the if statement of game.play")
            self.game_array[cell[1]][cell[0]] = player
            if player == 0:
                print("set p2went to false")
                self.p1went = True
                self.p2went = False
            else:
                print("set p1went to false")
                self.p2went = True
                self.p1went = False

    def getWinner(self):
        for line in self.possible_matches:
            get_sum = sum(self.game_array[i][j] for i, j in line)
            if get_sum == 0 or get_sum == 3:
                # indexing the string 'XO' based on the boolean condition
                self.winner = 'XO'[get_sum == 0]
                self.wins[self.winner] += 1
                self.winner_coordinates = [line[0][::-1], line[2][::-1]]
        return self.winner  # return 'X' or 'O' or -1 if nobody wins.

    def gameOver(self):
        for line in self.game_array:
            for i in line:
                if i == inf:
                    return False
        return True

    def reset(self):
        self.p1went = False
        self.p2went = False

    def bothWent(self):
        return self.p1went and self.p2went
