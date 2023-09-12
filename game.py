
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

    def isReady(self):
        return self.ready

    def play(self, player, cell):
        """
        Update the game array with 'X' (corresponding to 1) and 'O' (corresponding to 0), 
        and get the cell which is to be updated within the game array.

        """
        self.game_array[cell[0]][cell[1]] = player
        if player == 0:
            self.p1went = True
        else:
            self.p2went = True

    def winner(self):
        for line in self.possible_matches:
            get_sum = sum(self.game_array[i][j] for i, j in line)
            if get_sum == 0 or get_sum == 3:
                # indexing the string 'XO' based on the boolean condition
                self.winner = 'XO'[get_sum == 0]
                self.wins[self.winner] += 1
        return self.winner  # return 'X' or 'O' or -1 if nobody wins.

    def reset(self):
        self.p1went = False
        self.p2went = False

    def bothWent(self):
        return self.p1went and self.p2went
