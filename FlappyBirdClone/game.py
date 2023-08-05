import pygame
import random
import time

pygame.init()

width = 800
height = 600

obstacles = []

graphicsPath = "FlappyBirdClone/graphics/"
playerSprite = graphicsPath + "FlappyBirdPlayer.png"
background = graphicsPath + "FlappyBirdBG.png"
obstacleSprite = graphicsPath + "FlappyBirdObstacle.png"

background_img = pygame.image.load(background)
player_img = pygame.image.load(playerSprite)
obstacle_img = pygame.image.load(obstacleSprite)

score = 0

player_width = 68
player_height = 34
player_speed = 5
x_player = 50
y_player = height // 2 - player_height // 2
player_max_height = height - player_height
obstacle_width = 20
obstacle_height = 600

obstacle_img = pygame.transform.scale(obstacle_img, (obstacle_width, obstacle_height))

obstacle_speed = 2
obstacle_creation_time = time.time()
obstacle_creation_delay = 2.0

gap_height = player_height + random.randint(10, 200)

def draw_player(x, y):
    window.blit(player_img, (x, y))


def create_obstacle():
    gap_position = random.randint(100, height - gap_height - 100)
    obstacle = {
        'x': width,
        'y': gap_position,  # y-Position der Mitte der Lücke zwischen den Röhren
        'counted' : False
    }
    obstacles.append(obstacle)

def draw_obstacles():
    for obstacle in obstacles:
        obstacle['x'] -= obstacle_speed

        # Obere Röhre
        upper_pipe_rect = pygame.Rect(obstacle['x'], obstacle['y'] - gap_height // 2 - obstacle_height, obstacle_width, obstacle_height)
        window.blit(obstacle_img, upper_pipe_rect)
        # Untere Röhre
        lower_pipe_rect = pygame.Rect(obstacle['x'], obstacle['y'] + gap_height // 2, obstacle_width, obstacle_height)
        window.blit(obstacle_img, lower_pipe_rect)

def display_score():
    font = pygame.font.Font(None, 36)
    score_text = font.render("Score: " + str(score), True, (255, 255, 255))
    window.blit(score_text, (10, 10))

def display_game_over():
    font = pygame.font.Font(None, 50)
    game_over_text = font.render("Game Over! Final Score: " + str(score), True, (255, 255, 255), (0,0,0))
    window.blit(game_over_text, (width // 2 - game_over_text.get_width() // 2, height // 2 - game_over_text.get_height() // 2))

def check_collision():
    player_rect = pygame.Rect(x_player, y_player, player_width, player_height)
    for obstacle in obstacles:
        upper_pipe_rect = pygame.Rect(obstacle['x'], obstacle['y'] - gap_height // 2 - obstacle_height, obstacle_width, obstacle_height)
        lower_pipe_rect = pygame.Rect(obstacle['x'], obstacle['y'] + gap_height // 2, obstacle_width, obstacle_height)
        if player_rect.colliderect(upper_pipe_rect) or player_rect.colliderect(lower_pipe_rect):
            return True
    return False

window = pygame.display.set_mode((width, height))

pygame.display.set_caption("Crappy Bird")

window.blit(background_img, (0,0))

running = True

scoreIncreased = False
firstStart = True
game_over = False

while running:
    current_time = time.time()

    if current_time - obstacle_creation_time >= 5 and firstStart:
        create_obstacle()
        firstStart = False

    for obstacle in obstacles:
        if obstacle['x'] < - 100:
            obstacles.clear()
            gap_height = player_height + random.randint(10, 200)
            create_obstacle()
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        y_player -= player_speed
    if keys[pygame.K_DOWN]:
        y_player += player_speed
    if y_player > player_max_height:
        y_player = player_max_height
    if y_player < player_height:
        y_player = player_height

    window.blit(background_img, (0, 0))

    draw_obstacles()
    
    draw_player(x_player, y_player)

    for obstacle in obstacles:
        if obstacle['x'] + obstacle_width < x_player and not obstacle['counted']:
            obstacle['counted'] = True
            score += 1
    
    display_score()
    
    if check_collision():
        game_over = True
    
    while game_over:
        display_game_over()
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
    
    if score == 50 and scoreIncreased == False:
        obstacle_speed += 1
        scoreIncreased = True

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.update()

pygame.quit()