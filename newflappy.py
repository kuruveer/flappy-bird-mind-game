# Importing the libraries
import pygame
import sys
import random, time
import mindwave

# Initializing pygame
pygame.init()

# Game window dimensions
width, height = 350, 622
clock = pygame.time.Clock()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Flappy Bird")

# Background and floor images
back_img = pygame.image.load("img_46.png")
floor_img = pygame.image.load("img_50.png")
floor_x = 0

# Bird images and variables
bird_up = pygame.image.load("img_47.png")
bird_mid = pygame.image.load("img_49.png")
bird_down = pygame.image.load("img_48.png")
birds = [bird_up, bird_mid, bird_down]
bird_index = 0
bird_flap = pygame.USEREVENT
pygame.time.set_timer(bird_flap, 200)
bird_img = birds[bird_index]
bird_rect = bird_img.get_rect(center=(67, height // 2))  # Centering the bird vertically
bird_movement = 0
gravity = 0.6

# Pipe image and variables
pipe_img = pygame.image.load("greenpipe.png")
pipe_heights = [400, 350, 533, 490]
pipes = []
create_pipe = pygame.USEREVENT + 1
pygame.time.set_timer(create_pipe, 1500)

# Game over image and variables
game_over = False
over_img = pygame.image.load("img_45.png").convert_alpha()
over_rect = over_img.get_rect(center=(width // 2, height // 2))

# Distance and time variables
distance_covered = 0
time_elapsed = 0

# Bird velocity and speed variables
bird_velocity = 1  # Initial velocity in meters per second
current_speed = 0  # Current speed in pixels per second

# Score font
score_font = pygame.font.Font("freesansbold.ttf", 20)

# Function to draw floor
def draw_floor():
    screen.blit(floor_img, (floor_x, height - floor_img.get_height()))
    screen.blit(floor_img, (floor_x + 448, height - floor_img.get_height()))

def draw_data(meditation, attention):
    meditation_text = score_font.render(f"med: {meditation}", True, (255, 255, 255))
    attention_text = score_font.render(f"att: {attention}", True, (255, 255, 255))
    screen.blit(meditation_text, (10, 10))
    screen.blit(attention_text, (width // 2 - 50, 10))

# Function to draw distance
def draw_distance(distance):
    distance_text = score_font.render(f"dis: {distance:.2f} m", True, (255, 255, 255))
    screen.blit(distance_text, (10, 30))

# Function to draw current speed
def draw_speed(speed):
    speed_text = score_font.render(f"speed: {speed} m/s", True, (255, 255, 255))
    screen.blit(speed_text, (width // 2 - 50, 30))

# Function to draw game time
def draw_time(time):
    time_text = score_font.render(f"Time: {time:.2f} s", True, (255, 255, 255))
    screen.blit(time_text, (10, 50))

# Function to create pipes
def create_pipes():
    pipe_y = random.choice(pipe_heights)
    top_pipe = pipe_img.get_rect(midbottom=(500, pipe_y - 250))
    bottom_pipe = pipe_img.get_rect(midtop=(500, pipe_y))
    return top_pipe, bottom_pipe

# Function for pipe animation and collision
def pipe_animation():
    global game_over, distance_covered, time_elapsed
    for pipe in pipes:
        if pipe.right <= 0:
            pipes.remove(pipe)
        else:
            pipe.centerx -= int(bird_velocity * 60)  # Move pipes according to current speed

        # Collision detection
        if bird_rect.colliderect(pipe):
            game_over = True

    if bird_rect.top <= 0 or bird_rect.bottom >= height - floor_img.get_height():
        game_over = True

headset = mindwave.Headset('/dev/tty.MindLink')
print('Connected, waiting 10 seconds for data to start streaming')
time.sleep(10)

# Game loop
running = True
while running:
    print ("Raw value: %s, Attention: %s, Meditation: %s" % (headset.raw_value, headset.attention, headset.meditation))
    print ("Waves: {}".format(headset.waves))
    print ("Values: ", list(headset.waves.values()))
    time.sleep(1)
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not game_over:
                bird_movement = -10  # Adjust jump strength as needed

            if event.key == pygame.K_SPACE and game_over:
                game_over = False
                pipes.clear()
                bird_rect.center = (67, height // 2)
                bird_movement = 0
                distance_covered = 0
                time_elapsed = 0
                pygame.time.set_timer(create_pipe, 1500)

            if event.key == pygame.K_RIGHT:  # Increase speed
                bird_velocity += 1

            if event.key == pygame.K_LEFT:  # Decrease speed (minimum 1 m/s)
                bird_velocity = max(1, bird_velocity - 1)

        if event.type == bird_flap:
            bird_index = (bird_index + 1) % len(birds)
            bird_img = birds[bird_index]


    # bird_velocity = headset.attention / 10


    # Bird movement
    # bird_movement += gravity 
    # bird_movement += gravity * (1 - (headset.attention / 100))
    bird_rect.centery += int(bird_movement)

    # Calculate current speed
    current_speed = bird_velocity  # Update current speed every frame

    # Update time elapsed
    if not game_over:
        time_elapsed += 1 / 60  # Update time elapsed (assuming 60 FPS)

    # Drawing elements
    screen.blit(back_img, (0, 0))

    if not game_over:
        distance_covered += current_speed / 60  # Increase distance based on velocity

        pipe_animation()
        screen.blit(bird_img, bird_rect)
        draw_data(headset.meditation, headset.attention)
        draw_distance(distance_covered)
        draw_speed(current_speed)  # Draw current speed
        draw_time(time_elapsed)  # Draw game time

    else:
        screen.blit(over_img, over_rect)

    draw_floor()
    pygame.display.update()

pygame.quit()
sys.exit()
