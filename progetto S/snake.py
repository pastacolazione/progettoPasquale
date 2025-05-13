import pygame
import sys
import time
import random

pygame.init()
width, height = 600, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Snake')
clock = pygame.time.Clock()
FPS = 60

verde = (0, 255, 0)
verde_scuro = (0, 180, 0)
bianco = (255, 255, 255)
nero = (0, 0, 0)
blu = (0, 0, 255)
rosso = (255, 0, 0)
rosa = (255, 105, 180)

font_grande = pygame.font.Font(None, 60)
font_medio = pygame.font.Font(None, 40)

cieli = [
    pygame.image.load('cielo azzurro pixellato.JPG'),
    pygame.image.load('cielo azzurro tramonto pixellato-2.jpg'),
    pygame.image.load('notte stellata pixellato.JPG')
]
sky_width = cieli[0].get_width()
sky_x = 0
sky_speed = 0.2
background_index = 0
last_sky_change = time.time()
sky_change_interval = 10

testa_su = pygame.image.load('head_up.png')
testa_giu = pygame.image.load('head_down.png')
testa_left = pygame.image.load('head_left.png')
testa_right = pygame.image.load('head_right.png')

body_bl = pygame.image.load('body_bl.png')
body_br = pygame.image.load('body_br.png')
body_horizontal = pygame.image.load('body_horizontal.png')
body_tl = pygame.image.load('body_tl.png')
body_tr = pygame.image.load('body_tr.png')
body_vertical = pygame.image.load('body_vertical.png')

tail_down = pygame.image.load('tail_down.png')
tail_left = pygame.image.load('tail_left.png')
tail_right = pygame.image.load('tail_right.png')
tail_up = pygame.image.load('tail_up.png')

mela_img = pygame.image.load('red apple.png')  
mela_img = pygame.transform.scale(mela_img, (30, 30))  

snake_block = 20
snake_speed = 10

def disegna_menu():
    global sky_x, last_sky_change, background_index

    now = time.time()
    if now - last_sky_change > sky_change_interval:
        background_index = (background_index + 1) % len(cieli)
        last_sky_change = now
        sky_x = 0

    background = pygame.transform.scale(cieli[background_index], (width, height))
    for i in range((width // sky_width) + 2):
        screen.blit(background, (sky_x + i * sky_width, 0))
    sky_x -= sky_speed
    if sky_x <= -sky_width:
        sky_x = 0

    button_size = (200, 60)
    start_btn = pygame.Rect((width - button_size[0]) // 2, height // 2 - 40, *button_size)

    pygame.draw.rect(screen, blu, start_btn)
    screen.blit(font_medio.render("INIZIA", True, bianco), start_btn.move(50, 10))

    pygame.display.flip()
    return start_btn

def disegna_serpente(snake, direzione):
    for i in range(1, len(snake) - 1):
        x, y = snake[i]
        prev_x, prev_y = snake[i - 1]
        next_x, next_y = snake[i + 1]

        dir_from = (prev_x - x, prev_y - y)
        dir_to = (next_x - x, next_y - y)

        if dir_from[0] == 0 and dir_to[0] == 0:
            screen.blit(body_vertical, (x, y))
        elif dir_from[1] == 0 and dir_to[1] == 0:
            screen.blit(body_horizontal, (x, y))
        elif (dir_from == (-1, 0) and dir_to == (0, -1)) or (dir_from == (0, -1) and dir_to == (-1, 0)):
            screen.blit(body_tr, (x, y))
        elif (dir_from == (1, 0) and dir_to == (0, -1)) or (dir_from == (0, -1) and dir_to == (1, 0)):
            screen.blit(body_tl, (x, y))
        elif (dir_from == (-1, 0) and dir_to == (0, 1)) or (dir_from == (0, 1) and dir_to == (-1, 0)):
            screen.blit(body_br, (x, y))
        elif (dir_from == (1, 0) and dir_to == (0, 1)) or (dir_from == (0, 1) and dir_to == (1, 0)):
            screen.blit(body_bl, (x, y))

    if len(snake) > 1:
        tail_x, tail_y = snake[-1]
        before_tail_x, before_tail_y = snake[-2]
        dx = tail_x - before_tail_x
        dy = tail_y - before_tail_y

        if dx == 20:
            screen.blit(tail_right, (tail_x, tail_y))
        elif dx == -20:
            screen.blit(tail_left, (tail_x, tail_y))
        elif dy == 20:
            screen.blit(tail_down, (tail_x, tail_y))
        elif dy == -20:
            screen.blit(tail_up, (tail_x, tail_y))

    head_x, head_y = snake[0]
    if direzione == "su":
        screen.blit(testa_su, (head_x, head_y))
    elif direzione == "giu":
        screen.blit(testa_giu, (head_x, head_y))
    elif direzione == "sinistra":
        screen.blit(testa_left, (head_x, head_y))
    elif direzione == "destra":
        screen.blit(testa_right, (head_x, head_y))

    

def schermo_game_over():
    screen.fill(nero)
    messaggio = font_grande.render("Game Over! Premi R o Q", True, bianco)
    screen.blit(messaggio, messaggio.get_rect(center=(width // 2, height // 2)))
    pygame.display.flip()

def esegui_gioco():
    x, y = width // 2, height // 2
    dx, dy = snake_block, 0
    serpente = [[x, y]]
    score = 0

    food_x = random.randrange(0, width - snake_block, snake_block)
    food_y = random.randrange(0, height - snake_block, snake_block)

    direzione = "destra"
    game_over = False
    in_pausa = False

    while not game_over:
        while in_pausa:
            schermo_game_over()
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_q:
                        pygame.quit(); sys.exit()
                    if e.key == pygame.K_r:
                        return esegui_gioco()

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_LEFT and dx == 0:
                    dx, dy = -snake_block, 0
                    direzione = "sinistra"
                elif e.key == pygame.K_RIGHT and dx == 0:
                    dx, dy = snake_block, 0
                    direzione = "destra"
                elif e.key == pygame.K_UP and dy == 0:
                    dx, dy = 0, -snake_block
                    direzione = "su"
                elif e.key == pygame.K_DOWN and dy == 0:
                    dx, dy = 0, snake_block
                    direzione = "giu"

        x += dx
        y += dy
        nuova_testa = [x, y]

        if x < 0 or x >= width or y < 0 or y >= height:
            in_pausa = True

        serpente.insert(0, nuova_testa)

        if x == food_x and y == food_y:
            food_x = random.randrange(0, width - snake_block, snake_block)
            food_y = random.randrange(0, height - snake_block, snake_block)
            score += 1
        else:
            serpente.pop()

        if nuova_testa in serpente[1:]:
            in_pausa = True

        screen.fill(nero)
        screen.blit(mela_img, (food_x, food_y))
        disegna_serpente(serpente, direzione)

        score_text = font_medio.render(f"Punteggio: {score}", True, bianco)
        screen.blit(score_text, (10, 10))
        pygame.display.flip()
        clock.tick(snake_speed)

def main():
    global screen
    in_gioco = False
    sky_x = 0

    while True:
        clock.tick(FPS)
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if e.type == pygame.MOUSEBUTTONDOWN and not in_gioco:
                start_btn = disegna_menu()
                if start_btn.collidepoint(e.pos):
                    in_gioco = True
                    esegui_gioco()
                    in_gioco = False

        if not in_gioco:
            disegna_menu()

if __name__ == "__main__":
    main()
