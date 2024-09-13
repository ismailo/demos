import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions and setup
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Squirrel Finder')

# Load and scale images
koala_img = pygame.image.load('koala.png')
koala_img = pygame.transform.scale(koala_img, (40, 40))

strawberry_img = pygame.image.load('strawberry.png')
strawberry_img = pygame.transform.scale(strawberry_img, (40, 40))

squirrel_img = pygame.image.load('squirrel.png')
squirrel_img = pygame.transform.scale(squirrel_img, (40, 40))

# Colors and fonts
BACKGROUND_COLOR = (0, 0, 40)  # Dark background
font = pygame.font.Font(None, 36)

# Function to draw text
def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    surface.blit(textobj, (x, y))

def main():
    clock = pygame.time.Clock()
    game_state = 'start_screen'
    koala_rect = koala_img.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    koala_speed = 7

    # Initialize variables in the enclosing scope
    strawberry_list = []
    squirrel = None
    last_strawberry_spawn_time = pygame.time.get_ticks()
    game_start_time = pygame.time.get_ticks()

    def initialize_game():
        nonlocal koala_rect, strawberry_list, squirrel, last_strawberry_spawn_time, game_start_time
        koala_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        strawberry_list = []
        squirrel = None
        last_strawberry_spawn_time = pygame.time.get_ticks()
        game_start_time = pygame.time.get_ticks()

    initialize_game()
    game_over_start_time = None

    while True:
        current_time = pygame.time.get_ticks()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if game_state == 'start_screen':
                if event.type == pygame.KEYDOWN:
                    game_state = 'playing'
                    initialize_game()

        keys = pygame.key.get_pressed()
        if game_state == 'playing':
            # Move koala
            if keys[pygame.K_LEFT]:
                koala_rect.x -= koala_speed
            if keys[pygame.K_RIGHT]:
                koala_rect.x += koala_speed
            if keys[pygame.K_UP]:
                koala_rect.y -= koala_speed
            if keys[pygame.K_DOWN]:
                koala_rect.y += koala_speed

            # Keep koala on screen
            koala_rect.clamp_ip(screen.get_rect())

            # Spawn strawberries
            if current_time - last_strawberry_spawn_time >= 1000:
                strawberry_rect = strawberry_img.get_rect(
                    topleft=(random.randint(0, SCREEN_WIDTH - 40), random.randint(0, SCREEN_HEIGHT - 40)))
                strawberry_speed = [random.choice([-3, -2, -1, 1, 2, 3]),
                                    random.choice([-3, -2, -1, 1, 2, 3])]
                strawberry_list.append([strawberry_rect, strawberry_speed])
                last_strawberry_spawn_time = current_time

            # Move strawberries
            for strawberry in strawberry_list:
                strawberry_rect, strawberry_speed = strawberry
                strawberry_rect.x += strawberry_speed[0]
                strawberry_rect.y += strawberry_speed[1]
                if strawberry_rect.left <= 0 or strawberry_rect.right >= SCREEN_WIDTH:
                    strawberry_speed[0] = -strawberry_speed[0]
                if strawberry_rect.top <= 0 or strawberry_rect.bottom >= SCREEN_HEIGHT:
                    strawberry_speed[1] = -strawberry_speed[1]
                if koala_rect.colliderect(strawberry_rect):
                    game_state = 'game_over'
                    game_over_start_time = pygame.time.get_ticks()

            # Spawn squirrel after 3 seconds
            if squirrel is None and current_time - game_start_time >= 3000:
                squirrel_rect = squirrel_img.get_rect(
                    topleft=(random.randint(0, SCREEN_WIDTH - 40), random.randint(0, SCREEN_HEIGHT - 40)))
                squirrel_speed = [random.choice([-3, -2, -1, 1, 2, 3]),
                                  random.choice([-3, -2, -1, 1, 2, 3])]
                squirrel = [squirrel_rect, squirrel_speed]

            # Move squirrel
            if squirrel:
                squirrel_rect, squirrel_speed = squirrel
                squirrel_rect.x += squirrel_speed[0]
                squirrel_rect.y += squirrel_speed[1]
                if squirrel_rect.left <= 0 or squirrel_rect.right >= SCREEN_WIDTH:
                    squirrel_speed[0] = -squirrel_speed[0]
                if squirrel_rect.top <= 0 or squirrel_rect.bottom >= SCREEN_HEIGHT:
                    squirrel_speed[1] = -squirrel_speed[1]
                if koala_rect.colliderect(squirrel_rect):
                    game_state = 'win'
                    game_over_start_time = pygame.time.get_ticks()

            # Drawing
            screen.fill(BACKGROUND_COLOR)
            screen.blit(koala_img, koala_rect)
            for strawberry in strawberry_list:
                screen.blit(strawberry_img, strawberry[0])
            if squirrel:
                screen.blit(squirrel_img, squirrel[0])
            draw_text('openai', font, (255, 255, 255), screen, SCREEN_WIDTH - 100, SCREEN_HEIGHT - 30)
            elapsed_time = (current_time - game_start_time) // 1000
            draw_text(f'Time: {elapsed_time}', font, (255, 255, 255), screen, SCREEN_WIDTH - 150, 10)
            pygame.display.flip()
            clock.tick(60)

        elif game_state == 'game_over':
            screen.fill(BACKGROUND_COLOR)
            draw_text('Game Over!', font, (255, 0, 0), screen, SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT // 2 - 20)
            pygame.display.flip()
            if pygame.time.get_ticks() - game_over_start_time >= 2000:
                game_state = 'playing'
                initialize_game()
            clock.tick(60)

        elif game_state == 'win':
            screen.fill(BACKGROUND_COLOR)
            draw_text('You Win!', font, (0, 255, 0), screen, SCREEN_WIDTH // 2 - 70, SCREEN_HEIGHT // 2 - 20)
            pygame.display.flip()
            if pygame.time.get_ticks() - game_over_start_time >= 2000:
                game_state = 'playing'
                initialize_game()
            clock.tick(60)

        elif game_state == 'start_screen':
            screen.fill(BACKGROUND_COLOR)
            draw_text('Welcome to Squirrel Finder!', font, (255, 255, 255), screen, 20, 20)
            draw_text('Instructions:', font, (255, 255, 255), screen, 20, 70)
            draw_text('You are the koala. Use arrow keys to move.', font, (255, 255, 255), screen, 20, 110)
            draw_text('Avoid strawberries. If touched, you die.', font, (255, 255, 255), screen, 20, 150)
            draw_text('After 3 seconds, a squirrel appears.', font, (255, 255, 255), screen, 20, 190)
            draw_text('Touch the squirrel to win.', font, (255, 255, 255), screen, 20, 230)
            draw_text('Press any key to start.', font, (255, 255, 255), screen, 20, 270)
            pygame.display.flip()
            clock.tick(60)

if __name__ == '__main__':
    main()
