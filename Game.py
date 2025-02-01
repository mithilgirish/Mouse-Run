import pygame
import random
import time
import pygame.mixer
import MainMenu
import config 

# Initialize Pygame
pygame.init()

# Initialize the mixer
pygame.mixer.init()

# Set up the display
WIDTH = 525
HEIGHT = 725
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Mouse Run')

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GRAY = (200, 200, 200)

# Player
player_width = 63
player_height = 150
player_y = HEIGHT - player_height - 50
player_speed = 5
player_x = 0  # Initialize player_x

Mouse_images = [pygame.transform.scale(pygame.image.load(f'Mouse/M{i}.png'), (player_width, player_height)) for i in range(4)]
Mouse_images = Mouse_images * 3  # Repeat each image 3 times

image_index = 0
TempY = 1

# Tracks
track_count = 3
track_width = WIDTH // track_count
current_track = 1

# Trains
train_width = 80
train_height = 360
train_speed = 6
trains = []
max_trains = 2

train_image1 = pygame.transform.scale(pygame.image.load('Images/train1.png'), (train_width, train_height))
train_image2 = pygame.transform.scale(pygame.image.load('Images/train2.png'), (train_width, train_height))

background_image = pygame.transform.scale(pygame.image.load('Images/background.png'), (WIDTH, HEIGHT))

PlainBG = pygame.transform.scale(pygame.image.load('Images/PlainBG.png'), (WIDTH, HEIGHT))

GameOver = pygame.transform.scale(pygame.image.load('Images/gameover.png'), (150, 150))

# Cheese
cheese_width = 30
cheese_height = 30
cheese_image = pygame.transform.scale(pygame.image.load('Images/cheese.png'), (cheese_width, cheese_height))
cheese_imageGame = pygame.transform.scale(pygame.image.load('Images/cheese.png'), (cheese_width *1.5, cheese_height*1.5))
cheeses = []
cheese_count = 0

# Path
path_segment_height = 200
path_speed = 6
path_segments = []

# Background
background_y = 0

# Score and font
start_time = time.time()
final_score = 0
font = pygame.font.Font(None, 36)
fontH = pygame.font.Font(None, 100)

# Game state
game_over = False
paused = False

# Load sound effects
cheese_sound = pygame.mixer.Sound('Sounds/coin.mp3')
collision_sound = pygame.mixer.Sound('Sounds/gameover.mp3')
Move_sound = pygame.mixer.Sound('Sounds/move.mp3')

# Load background music
pygame.mixer.music.load('Sounds/Music.mp3')

# Game loop
clock = pygame.time.Clock()



def spawn_train():
    if len(trains) < max_trains:
        available_tracks = list(range(track_count))
        for train in trains:
            if train['track'] in available_tracks:
                available_tracks.remove(train['track'])
        
        if available_tracks:
            track = random.choice(available_tracks)
            train = {
                'x': track * track_width + (track_width - train_width) // 2,
                'y': -train_height,
                'track': track
            }
            trains.append(train)

def spawn_cheese():
    available_tracks = list(range(track_count))
    for train in trains:
        if train['track'] in available_tracks:
            available_tracks.remove(train['track'])
    
    if available_tracks:
        track = random.choice(available_tracks)
        cheese = {
            'x': track * track_width + (track_width - cheese_width) // 2,
            'y': -cheese_height
        }
        cheeses.append(cheese)

def handle_cheese():
    global cheese_count
    for cheese in cheeses[:]:
        cheese['y'] += path_speed
        if cheese['y'] > HEIGHT:
            cheeses.remove(cheese)
        elif check_cheese_collision(cheese):
            cheeses.remove(cheese)
            cheese_count += 1
            play_sfx(cheese_sound)

def check_cheese_collision(cheese):
    player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
    cheese_rect = pygame.Rect(cheese['x'], cheese['y'], cheese_width, cheese_height)
    return player_rect.colliderect(cheese_rect)

def create_path_segment(y_pos):
    segment = {
        'y': y_pos,
    }
    path_segments.append(segment)

def display_score():
    elapsed_time = int(time.time() - start_time)
    score_text = font.render(f"Score: {elapsed_time}", True, WHITE)
    cheese_count_text = font.render(f": {cheese_count}", True, WHITE)
    screen.blit(score_text, (WIDTH - 150, 10))
    screen.blit(cheese_image, (WIDTH - 150, 50))
    screen.blit(cheese_count_text, (WIDTH - 110, 50))

def check_collision():
    player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
    for train in trains:
        train_rect = pygame.Rect(train['x'], train['y'], train_width, train_height)
        if player_rect.colliderect(train_rect):
            return True
    return False

def handle_game_over():
    global game_over, start_time, trains, cheese_count

    screen.blit(PlainBG,(0,0))
    screen.blit(GameOver,(WIDTH // 2 - 80, HEIGHT // 2 -270))
    game_over_text = fontH.render("Game Over", True, RED)
    score_text = font.render(f"Score: {final_score}", True, WHITE)
    cheese_text = font.render(f": {cheese_count}", True, WHITE)
    screen.blit(cheese_image, (WIDTH // 2 - cheese_text.get_width() // 2 -30, HEIGHT // 2 + 45))
    restart_text = font.render("Press R to Restart", True, WHITE)
    menu_text = font.render("Press M for Menu", True, WHITE)

    screen.blit(game_over_text, (WIDTH // 2 - 180, HEIGHT // 2 - 100))
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2))
    screen.blit(cheese_text, (WIDTH // 2 - cheese_text.get_width() // 2 + 10, HEIGHT // 2 + 50))
    screen.blit(restart_text, (WIDTH // 2 - 100, HEIGHT // 2 + 100))
    screen.blit(menu_text, (WIDTH // 2 - menu_text.get_width() // 2, HEIGHT // 2 + 150))

    keys = pygame.key.get_pressed()
    if keys[pygame.K_r]:
        # Reset game
        game_over = False
        start_time = time.time()
        trains.clear()
        cheeses.clear()
        cheese_count = 0
        spawn_train()
        spawn_train()
        play_music()

def handle_pause():
    global paused

    if paused:
        pause_music()

    pause_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    pause_surface.fill((0, 0, 0, 128))  # Semi-transparent black
    screen.blit(pause_surface, (0, 0))
    screen.blit(PlainBG,(0,0))

    pause_text = fontH.render("PAUSED", True, WHITE)
    resume_text = font.render("Press P to Resume", True, WHITE)
    menu_text = font.render("Press M for Menu", True, WHITE)
    quit_text = font.render("Press Q to Quit", True, RED)

    screen.blit(pause_text, (WIDTH // 2 - pause_text.get_width() // 2, HEIGHT // 2 - 200))
    screen.blit(resume_text, (WIDTH // 2 - resume_text.get_width() // 2, HEIGHT // 2))
    screen.blit(menu_text, (WIDTH // 2 - menu_text.get_width() // 2, HEIGHT // 2 + 60))
    screen.blit(quit_text, (WIDTH // 2 - quit_text.get_width() // 2, HEIGHT // 2 + 120))

    keys = pygame.key.get_pressed()
    if keys[pygame.K_p]:
        paused = False
        unpause_music()
    elif keys[pygame.K_q]:
        pygame.quit()
        quit()
    elif keys[pygame.K_m]:
        MainMenu.main()

# Initialize path segments
for i in range(HEIGHT // path_segment_height + 2):
    create_path_segment(i * path_segment_height - path_segment_height)

# Spawn initial trains
spawn_train()
spawn_train()

def game():
    # Reset game
    global player_x, game_over, paused, current_track, image_index, TempY, player_y, background_y, final_score, start_time, cheese_count
    global play_sfx,play_music,pause_music,unpause_music,stop_music

        # Sound settings
    ####################
    SFX_Active = config.get_SFX_Active()
    Music_Active = config.get_Music_Active()
    ####################

    def play_sfx(sound):
        if SFX_Active:
            sound.play()

    def play_music():
        if Music_Active:
            pygame.mixer.music.play(-1)  # -1 means loop indefinitely

    def pause_music():
        if Music_Active:
            pygame.mixer.music.pause()

    def unpause_music():
        if Music_Active:
            pygame.mixer.music.unpause()

    def stop_music():
        if Music_Active:
            pygame.mixer.music.stop()

    game_over = False
    
    start_time = time.time()
    trains.clear()
    cheeses.clear()
    cheese_count = 0
    spawn_train()
    spawn_train()
    paused = False

    play_music()
    
    # Initialize train_image here
    train_image = random.choice([train_image1, train_image2])
    
    running = True
    while running:
        ####################
        SFX_Active = config.get_SFX_Active()
        Music_Active = config.get_Music_Active()
        ####################
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if not game_over and not paused:
                    if event.key == pygame.K_LEFT and current_track > 0:
                        current_track -= 1
                        play_sfx(Move_sound)
                    if event.key == pygame.K_RIGHT and current_track < 2:
                        current_track += 1
                        play_sfx(Move_sound)
                    if event.key == pygame.K_ESCAPE:
                        paused = True
                elif game_over:
                    if event.key == pygame.K_r:
                        # Reset game
                        game_over = False
                        start_time = time.time()
                        trains.clear()
                        cheeses.clear()
                        cheese_count = 0
                        spawn_train()
                        spawn_train()
                        play_music()
                    elif event.key == pygame.K_m:
                        MainMenu.main()
                        return
                elif paused:
                    if event.key == pygame.K_p:
                        paused = False
                        unpause_music()
                    elif event.key == pygame.K_m:
                        MainMenu.main()
                        return
                    elif event.key == pygame.K_q:
                        pygame.quit()
                        return

        if not game_over and not paused:
            # Game logic
            player_x = current_track * track_width + (track_width - player_width) // 2

            for train in trains[:]:
                train['y'] += train_speed
                if train['y'] > HEIGHT:
                    trains.remove(train)
                    spawn_train()
                    train_image = random.choice([train_image1, train_image2])

            if check_collision():
                game_over = True
                final_score = int(time.time() - start_time)
                play_sfx(collision_sound)
                stop_music()

            # Handle cheese
            if random.random() < 0.02 and len(cheeses) < 3:  # Limit to 3 cheeses on screen
                spawn_cheese()
            handle_cheese()

            # Move path segments and background
            for segment in path_segments:
                segment['y'] += path_speed
                if segment['y'] > HEIGHT:
                    path_segments.remove(segment)
                    create_path_segment(-path_segment_height)

            background_y = (background_y + path_speed) % HEIGHT

            # Draw game elements
            screen.blit(background_image, (0, background_y - HEIGHT))
            screen.blit(background_image, (0, background_y))

            for train in trains:
                screen.blit(train_image, (train['x'], train['y']))

            for cheese in cheeses:
                screen.blit(cheese_imageGame, (cheese['x'], cheese['y']))

            screen.blit(Mouse_images[image_index], (player_x, player_y))

            image_index = (image_index + 1) % len(Mouse_images)
            
            TempY = TempY * -1
            player_y = player_y + 1 * TempY

            display_score()
        elif game_over:
            handle_game_over()
        elif paused:
            handle_pause()

        pygame.display.flip()
        clock.tick(60)