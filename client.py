import pygame as pg
import sys
from network import Network
pg.font.init()

SCREEN_WIDTH = 600
CELL_SIZE = SCREEN_WIDTH // 3
inf = float("inf")
vec2 = pg.math.Vector2
CELL_CENTER = vec2(CELL_SIZE / 2)
win = pg.display.set_mode([SCREEN_WIDTH] * 2)
font_type = "comicsans"


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
        self.player = 0  # generate a random player to start with
        self.possible_matches = [[(0, 0), (0, 1), (0, 2)],
                                 [(1, 0), (1, 1), (1, 2)],
                                 [(2, 0), (2, 1), (2, 2)],
                                 [(0, 0), (1, 0), (2, 0)],
                                 [(1, 0), (1, 1), (1, 2)],
                                 [(2, 0), (2, 1), (2, 2)],
                                 [(0, 0), (1, 1), (2, 2)],
                                 [(0, 2), (1, 1), (2, 0)],
                                 [(0, 1), (1, 1), (2, 1)]
                                 ]  # All possible line crosses for a player to win the game.
        self.winner = None
        self.num_steps = 0
        self.scribble_audio = pg.mixer.Sound("audio\scribble.wav")
        self.win_audio = pg.mixer.Sound("audio\winner_clap.wav")
        self.new_game_audio = pg.mixer.Sound("audio\gong.wav")
        pg.mixer.Sound.play(self.new_game_audio)

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
                    self.game.screen.blit(
                        self.x_img if obj else self.o_img, vec2(x, y) * CELL_SIZE)

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
        elif self.num_steps == 9:  # board filled
            pg.display.set_caption(
                "Game over, no winners!! PRESS SPACE TO BEGIN NEW GAME")

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


def draw_winner_line(game):
    pg.draw.line(win, 'white', [game.winner_coordinates[0][0]*CELL_SIZE+CELL_CENTER, game.winner_coordinates[0][1]*CELL_SIZE + CELL_CENTER], [
                 game.winner_coordinates[1][0]*CELL_SIZE+CELL_CENTER, game.winner_coordinates[1][1]*CELL_SIZE+CELL_CENTER], CELL_SIZE // 8)


def redrawWindow(win, game, p):
    pass


def main():
    run = True
    clock = pg.time.Clock()
    n = Network()
    player = int(n.getp())
    print("Assigned player number", player)

    while run:
        try:
            game = n.send("get")
        except:
            run = False
            print("Could not find the game...")
            break
        if game.bothWent():
            redrawWindow(win, game, player)
            # wait for half a second after drawing the window
            pg.time.delay(500)
            try:
                game = n.send("reset")
            except:
                run = False
                print("Could not find the game")
                break

            font = pg.font.SysFont(font_type, 90)
            if (game.winner() == 1 and player == 1) or (game.winner() == 0 and player == 0):
                draw_winner_line(game)
                text = font.render("You Won!", 1, (255, 0, 0))
                audio = pg.mixer.Sound("")
            elif game.winner() == -1:
                text = font.render("No spaces left...", 1, (255, 0, 0))
                audio = pg.mixer.Sound("")
            else:
                text = font.render("You Lost....", 1, (255, 0, 0))
                audio = pg.mixer.Sound("")

            win.blit(text, (SCREEN_WIDTH/2 - text.get_width() /
                     2, SCREEN_WIDTH/2 - text.get_height()/2))
            pg.display.update()            
            pg.mixer.Sound.play(audio)
            pg.time.delay(2000)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False 
                pg.quit()
            
            if event.type == pg.MOUSEBUTTONDOWN:
                pos = pg.mouse.get_pos()
                c, r = map(int, pos)
                text = str(c)+','+str(r)
                if game.ready():
                    if player == 0:
                        if not game.p1went:
                            n.send(text)
                    else:
                        if not game.p2went:
                            n.send(text)
        redrawWindow(win, game, player)



def intro_screen():
    run = True
    clock = pg.time.Clock()

    while run:
        clock.tick(60)
        win.fill((128, 128, 128))
        font = pg.font.SysFont("comicsans", 60)
        text = font.render("Click to Play!", 1, (255, 0, 0))
        win.blit(text, (100, 200))
        pg.display.update()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                run = False
            if event.type == pg.MOUSEBUTTONDOWN:
                run = False

    main()


while True:
    intro_screen()
