
inf = float("inf")

class Game:
    def __init__(self, id):
        self.p1went = False
        self.p2went = False
        self.id = id
        self.wins = {'X':0, 'O':0}
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
    
    def winner(self):
        for line in self.possible_matches:
            get_sum = sum(self.game_array[i][j] for i, j in line)
            if get_sum == 0 or get_sum == 3:
                # indexing the string 'XO' based on the boolean condition
                self.winner = 'XO'[get_sum == 0]
                self.wins[self.winner] += 1

    def reset(self):
        self.p1went = False
        self.p2went = False 
    
    def bothWent(self):
        return self.p1went and self.p2went
