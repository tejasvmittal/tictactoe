import pygame as pg
import sys
from random import randint

SCREEN_WIDTH = 600
CELL_SIZE = SCREEN_WIDTH // 3
inf = float("inf")
vec2 = pg.math.Vector2
CELL_CENTER = vec2(CELL_SIZE / 2)

class TicTacToe:
    def __init__(self, game):
        self.game = game
        self.background_img = self.get_image(
            path='background.png', res=[SCREEN_WIDTH] * 2)
        self.x_img = self.get_image(path='x.png', res=[CELL_SIZE] * 2)
        self.o_img = self.get_image(path='o.png', res=[CELL_SIZE] * 2)
        self.game_array = [[inf, inf, inf],
                           [inf, inf, inf],
                           [inf, inf, inf]]
        self.player = randint(0, 1)  # generate a random player to start with
        self.possible_matches = [[(0,0), (0,1), (0,2)],
                                 [(1,0), (1,1), (1,2)],
                                 [(2,0), (2, 1), (2,2)],
                                 [(0,0), (1,0), (2,0)],
                                 [(1,0), (1,1), (1,2)],
                                 [(2,0), (2,1), (2,2)],
                                 [(0,0), (1,1), (2,2)],
                                 [(0,2), (1,1), (2,0)],
                                 [(0,1),(1,1),(2,1)]
                                 ] # All possible line crosses for a player to win the game.
        self.winner = None
        self.num_steps = 0
        self.scribble_audio = pg.mixer.Sound("audio\scribble.wav")
        self.win_audio = pg.mixer.Sound("audio\winner_clap.wav")
        self.new_game_audio = pg.mixer.Sound("audio\gong.wav")
        pg.mixer.Sound.play(self.new_game_audio)
    
    def check_winner(self):
        for line in self.possible_matches:
            get_sum = sum(self.game_array[i][j] for i, j in line)
            if get_sum == 0 or get_sum == 3:
                self.winner = 'XO'[get_sum == 0] # indexing the string 'XO' based on the boolean condition
                # To draw a line we need starting and ending coordinates 
                self.winner_line = [vec2(line[0][::-1]) * CELL_SIZE + CELL_CENTER, vec2(line[2][::-1]) * CELL_SIZE + CELL_CENTER]
                pg.mixer.Sound.play(self.win_audio)
    
    def draw_winner_line(self):
        if self.winner:
            pg.draw.line(self.game.screen, 'white', self.winner_line[0], self.winner_line[1], CELL_SIZE // 8)


    def run_game_process(self):
        mouse_cell = vec2(pg.mouse.get_pos()) // CELL_SIZE
        c, r = map(int, mouse_cell)
        # will return true if the left mouse button is pressed
        left_click = pg.mouse.get_pressed()[0]
        if left_click and self.game_array[r][c] == inf and not self.winner:
            pg.mixer.Sound.play(self.scribble_audio)
            self.game_array[r][c] = self.player
            self.player = not self.player
            self.num_steps += 1
            self.check_winner()


    def draw_objects(self):
        for y, row in enumerate(self.game_array):
            for x, obj in enumerate(row):
                if obj != inf:
                    self.game.screen.blit(self.x_img if obj else self.o_img, vec2(x, y) * CELL_SIZE)


    def draw(self):
        self.game.screen.blit(self.background_img, (0, 0))
        self.draw_objects()
        self.draw_winner_line()


    @staticmethod
    def get_image(path, res):
        im = pg.image.load(path)
        return pg.transform.smoothscale(im, res)

    def print_caption(self):
        pg.display.set_caption("Player "+'XO'[not self.player]+"'s turn!")
        if self.winner:
            pg.display.set_caption(
                "Player " + self.winner + " wins !! PRESS SPACE TO BEGIN NEW GAME")
        elif self.num_steps == 9: # board filled
            pg.display.set_caption("Game over, no winners!! PRESS SPACE TO BEGIN NEW GAME")


    def run(self):
        self.print_caption()
        self.draw()
        self.run_game_process()


class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode([SCREEN_WIDTH] * 2)
        self.clock = pg.time.Clock()
        self.tic_tac_toe = TicTacToe(self)

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    # begin a new game
                    self.new_game()

    def run(self):
        while True:
            self.tic_tac_toe.run()
            self.check_events()
            pg.display.update()
            self.clock.tick(60)
    
    def new_game(self):
        self.tic_tac_toe = TicTacToe(self)


if __name__ == '__main__':
    game = Game()
    game.run()
