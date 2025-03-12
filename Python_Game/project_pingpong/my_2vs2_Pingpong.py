import pygame
from pygame.locals import *

pygame.init()

def draw_player():
    pygame.draw.rect(screen, BLACK, (player_x_pos, 520, player_width, player_height))

def draw_ball():
    pygame.draw.circle(screen, WHITE, (int(ball_x), int(ball_y)), ball_radius)

def draw_life(life):
    text_surface = font.render(f"Life : {life}", True, WHITE)
    screen.blit(text_surface, (10, 10))

block_destroyed = [[False] * 4 for _ in range(10)]

def display_block():
    for column in range(10):
        for row in range(4):
            block_top_left = (column * (block_width + 1.5), 100 + row * (block_height + 1.5))
            if not block_rect[column][row]:
                block_rect[column][row] = pygame.Rect(block_top_left[0], block_top_left[1], block_width, block_height)
            
            if not block_destroyed[column][row] and ball_rect.colliderect(block_rect[column][row]):
                global ball_speed_y
                ball_speed_y *= -1
                screen.fill(LIGHT_PINK, rect = block_rect[column][row])
                block_rect[column][row] = None
                block_destroyed[column][row] = True
            elif not block_destroyed[column][row]:
                screen.blit(block, block_top_left)

def display_game_over():
    game_font = pygame.font.SysFont("arialrounded", 60)
    txt_game_over = game_font.render(game_result, True, BLACK)
    rect_game_over = txt_game_over.get_rect(cetner = (int(screen_width / 2), int(screen_height / 2)))
    screen.blit(txt_game_over, rect_game_over)

screen_width = 450
screen_height = 630
screen = pygame.display.set_mode((screen_width, screen_height))

SURFACE = pygame.display.set_mode((screen_width, screen_height))
Bigfont = pygame.font.SysFont(None, 80)
game_result = Bigfont.render("! Game Over !", True, (255,255,255))

pygame.display.set_caption("공 튕기기 게임")

clock = pygame.time.Clock()

# 색상 정의
LIGHT_PINK = (255, 182, 193)
WHITE = (255, 255, 255)
BLACK = (33, 33, 33)

# 플레이어 설정 
player_width = 100
player_height = 10

player_x_pos = screen_width / 2 - (player_width / 2)
player_y_pos = 520

player_speed = 6
to_x = 0


# 공 설정
ball_radius = 15
ball_speed = 3
ball_speed_x = 0.25
ball_speed_y = 0.25

ball_x = ball_start_x = screen_width - ball_radius*2
ball_y = ball_start_y = (screen_width - ball_radius*2) / 2


# 벽돌 설정
block = pygame.image.load("C:\\Users\\ljm03\\Python_Game\\project_pingpong\\block_45_30.png")
block_size = block.get_rect().size
block_width = block_size[0]
block_height = block_size[1]

block_x_pos = screen_width / 10
block_y_pos = 0

block_rect = [[None]*4 for _ in range(10)]

column_save = 0
row_save = 0


# 게임 변수 설정
life = 3
font_size = 30
font = pygame.font.Font(None, font_size)
running = True
block_destroy = 0

while running:
    dt = clock.tick(60)
    
    ball_x += ball_speed_x * dt
    ball_y += ball_speed_y * dt
    
    
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                to_x -= player_speed
                
            elif event.key == pygame.K_RIGHT:
                to_x += player_speed
                
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT : 
                to_x = 0
                
    player_x_pos += to_x
    
    if player_x_pos < 0:
        player_x_pos = 0
        
    elif player_x_pos > screen_width - player_width :
        player_x_pos = screen_width - player_width
                
    
    ball_rect = pygame.Rect(int(ball_x - ball_radius), int(ball_y - ball_radius), ball_radius * 2, ball_radius * 2)
    ball_rect.centerx = int(ball_rect.centerx)
    ball_rect.centery = int(ball_rect.centery)

    player_rect = pygame.Rect(player_x_pos, player_y_pos, player_width, player_height)

    collision_result = bool(player_rect.colliderect(ball_rect))

    if collision_result and ball_y + ball_radius > player_y_pos + player_height - 10 and ball_y + ball_radius < player_y_pos + player_height + 10:
        print("!!BAR HIT !!")
        ball_speed_y *= -1.3
            
    if ball_x < -ball_radius: 
        print("LEFT HIT")
        ball_speed_x = -ball_speed_x
        ball_x = 0
    
    elif ball_x > screen_width - ball_radius*2: 
        print("RIGHT HIT")
        ball_speed_x = -ball_speed_x
        
    if ball_y <= 0: 
        print("TOP HIT")
        ball_speed_y = -ball_speed_y
        ball_y = 0
    
    elif ball_y >= screen_height - ball_radius * 2: 
        print("Bottom HIT")
        life -= 1
        ball_speed_y = -ball_speed_y
        ball_y = screen_height - ball_radius*2    
        
    if life == 0:
        running = False
        SURFACE.blit(game_result, (300,300))
        display_game_over        
    
        
    
    screen.fill(LIGHT_PINK)
    draw_ball()
    draw_player()
    display_block()
    draw_life(life)
  
    pygame.display.update()
    
pygame.time.delay(500)
pygame.quit()