import pygame as pg
from network import Network
pg.font.init()
pg.mixer.init()

SCREEN_WIDTH = 600
CELL_SIZE = SCREEN_WIDTH // 3
inf = float("inf")
vec2 = pg.math.Vector2
win = pg.display.set_mode([SCREEN_WIDTH] * 2)
font_type = "comicsans"

def get_image(path, res):
    im = pg.image.load(path)
    return pg.transform.smoothscale(im, res)

def draw_winner_line(game):
    pg.draw.line(win, 'white', [game.winner_coordinates[0][0]*CELL_SIZE+(CELL_SIZE/2), game.winner_coordinates[0][1]*CELL_SIZE + (CELL_SIZE/2)], [
                 game.winner_coordinates[1][0]*CELL_SIZE+(CELL_SIZE/2), game.winner_coordinates[1][1]*CELL_SIZE+(CELL_SIZE/2)], CELL_SIZE // 8)

def draw_objects(win, game):
    x_img = get_image(path='x.png', res=[CELL_SIZE] * 2)
    o_img = get_image(path='o.png', res=[CELL_SIZE] * 2)
    for y, row in enumerate(game.game_array):
        for x, obj in enumerate(row):
            if obj != inf:
                win.blit(
                    x_img if obj else o_img, vec2(x, y) * CELL_SIZE)
                

def redrawWindow(win, game, p):
    background_img = get_image(
        path='background.png', res=[SCREEN_WIDTH] * 2)
    win.blit(background_img, (0, 0))
    draw_objects(win, game)
    if not game.isReady():
        font = pg.font.SysFont(font_type, 60)
        text = font.render("Waiting for Player...", 1, (255,255,255), True)
        win.blit(text, (SCREEN_WIDTH/2 - text.get_width()/2, SCREEN_WIDTH/2 - text.get_height()/2))
    else:
        # Both players are connected
        font = pg.font.SysFont(font_type, 60)
        if game.getWinner() == -1:
            print(game.winner)
            if (game.p1went and p == 0) or (game.p2went and p == 1):
                text = font.render("Waiting...", 1, (0,0,0))
            elif (not game.p1went) and (not game.p2went):
                text = font.render("Make a move", 1, (0,0,0))
            else:
                text = font.render("Your turn", 1, (0,0,0))
            win.blit(text, (SCREEN_WIDTH/2 - text.get_width() /
                        2, SCREEN_WIDTH/2 - text.get_height()/2))


    pg.display.update()


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
        if game.p1went or game.p2went:
            redrawWindow(win, game, player)
            # wait for half a second after drawing the window
            pg.time.delay(500)
            font = pg.font.SysFont(font_type, 90)
            if (game.getWinner() == 'X' and player == 1) or (game.getWinner() == 'O' and player == 0):
                draw_winner_line(game)
                text = font.render("You Won!", 1, (255, 0, 0))
                audio = pg.mixer.Sound("audio\winner_clap.wav")
            elif (game.getWinner() == -1) and (game.gameOver()):
                text = font.render("No spaces left...", 1, (255, 0, 0))
                audio = pg.mixer.Sound("audio\gong.wav")
            elif (game.getWinner() == 'X' and player == 0) or (game.getWinner() == 'O' and player == 1):
                draw_winner_line(game)
                text = font.render("You Lost", 1, (255, 0, 0))
                audio = pg.mixer.Sound("audio\winner_clap.wav")
            else:
                text = font.render("", 1, (255,0,0))

            win.blit(text, (SCREEN_WIDTH/2 - text.get_width() /
                     2, SCREEN_WIDTH/2 - text.get_height()/2))
            pg.display.update()            
            # pg.mixer.Sound.play(audio)
            # pg.time.delay(2000)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False 
                pg.quit()
            
            if (event.type == pg.MOUSEBUTTONDOWN) and (game.getWinner() == -1):
                pos = pg.mouse.get_pos()
                c, r = map(int, pos)
                c, r = int(c//(SCREEN_WIDTH/3)), int(r//(SCREEN_WIDTH/3))
                text = str(c)+','+str(r)
                if game.isReady():
                    if player == 0:
                        if not game.p1went:
                            # not executing
                            print("Sending", text)
                            n.send(text)
                    else:
                        if not game.p2went:
                            # not executing
                            print("Sending", text)
                            n.send(text)
            if (event.type == pg.KEYDOWN):
                if (event.key == pg.K_SPACE) and (game.winner != -1):
                    # start a new game
                    pass
        redrawWindow(win, game, player)



def intro_screen():
    run = True
    clock = pg.time.Clock()

    while run:
        clock.tick(60)
        win.fill((128, 128, 128))
        font = pg.font.SysFont(font_type, 60)
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
