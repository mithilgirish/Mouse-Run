import pygame
import sys
import Game
import config

# Initialize Pygame
pygame.init()

# Set up the display
width, height = 525, 725
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Mouse Run')

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (169, 169, 169)

# Set up fonts
font = pygame.font.Font(None, 74)




BG_image = pygame.transform.scale( pygame.image.load('Images/Main Menu.png'), (width, height))
Settings_image = pygame.transform.scale( pygame.image.load('Images/settings.png'), (width, height))

check_image = pygame.transform.scale( pygame.image.load('Images/check.png'), (40, 40))

# Define button properties
button_width, button_height = 318, 68
play_button = pygame.Rect((105,390), (button_width, button_height))
settings_button = pygame.Rect((105,500), (button_width, button_height))


Back_button = pygame.Rect((14,14), (55, 55))

Music_button = pygame.Rect((327,180), (50, 50))
SFX_button =  pygame.Rect((327,295), (50, 50))

# Function to draw buttons
def draw_button(rect, text):
    pygame.draw.rect(screen, GRAY, rect)
    text_surf = font.render(text, True, BLACK)
    text_rect = text_surf.get_rect(center=rect.center)
    screen.blit(text_surf, text_rect)



def main():


    running = True
    while running:
        screen.blit(BG_image, (0,0))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.collidepoint(event.pos):
                    Game.game()
                elif settings_button.collidepoint(event.pos):
                    Settings()

        # Draw buttons
        #draw_button(play_button, 'Play')
        #draw_button(settings_button, 'Settings')

        # Update display
        pygame.display.flip()


def Settings():
    global Music_Active, SFX_Active
   
    running = True

    while running:
         ####################
        SFX_Active = config.get_SFX_Active()
        Music_Active = config.get_Music_Active()
        ####################
        screen.blit(Settings_image, (0,0))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if Back_button.collidepoint(event.pos):
                    main()
                if SFX_button.collidepoint(event.pos):
                    if SFX_Active == False:
                        config.set_SFX_Active(True)
                    elif SFX_Active == True:
                        config.set_SFX_Active(False)
                if Music_button.collidepoint(event.pos):
                    if Music_Active == False:
                        config.set_Music_Active(True)
                    elif Music_Active == True:
                        config.set_Music_Active(False)

        if Music_Active == True:
            screen.blit(check_image,(Music_button.x +5,Music_button.y+5))

        if SFX_Active == True:
            screen.blit(check_image,(SFX_button.x+5,SFX_button.y+3))
                

        # Draw buttons

        #draw_button(Back_button, '')
        #draw_button(VFX_button, '')
        #draw_button(Music_button, '')

        # Update display
        pygame.display.flip()



