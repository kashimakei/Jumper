'''
This is the main file of the platformer game.
'''
import pygame
import random
# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PLATFORM_WIDTH = 100
PLATFORM_HEIGHT = 20
PLAYER_WIDTH = 50
PLAYER_HEIGHT = 50
GRAVITY = 0.1
JUMP_FORCE = 15
LEVELS = 100
THEME_INTERVAL = 10
# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface([PLATFORM_WIDTH, PLATFORM_HEIGHT])
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([PLAYER_WIDTH, PLAYER_HEIGHT])
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH // 2 - PLAYER_WIDTH // 2
        self.rect.y = SCREEN_HEIGHT - PLAYER_HEIGHT
        self.velocity_y = 0
    def update(self):
        self.velocity_y += GRAVITY
        self.rect.y += self.velocity_y
        if self.rect.y >= SCREEN_HEIGHT - PLAYER_HEIGHT:
            self.rect.y = SCREEN_HEIGHT - PLAYER_HEIGHT
            self.velocity_y = 0
        elif self.rect.y < 0:
            self.rect.y = 0
            self.velocity_y = 0
    def jump(self):
        self.velocity_y -= JUMP_FORCE
def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Platformer Game")
    all_sprites = pygame.sprite.Group()
    platforms = pygame.sprite.Group()
    player = Player()
    all_sprites.add(player)
    current_level = 1
    current_theme = 1
    for i in range(10):
        platform_x = random.randint(0, SCREEN_WIDTH - PLATFORM_WIDTH)
        platform_y = i * 100
        try:
            platform = Platform(platform_x, platform_y)
            all_sprites.add(platform)
            platforms.add(platform)
        except Exception as e:
            print(f"Failed to generate platform at ({platform_x}, {platform_y}): {e}")
            continue
    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.jump()
        all_sprites.update()
        if player.rect.y <= SCREEN_HEIGHT // 4:
            player.rect.y = SCREEN_HEIGHT // 4
            for platform in platforms:
                platform.rect.y += abs(player.velocity_y)
                if platform.rect.top >= SCREEN_HEIGHT:
                    platform.kill()
                    new_platform_x = random.randint(0, SCREEN_WIDTH - PLATFORM_WIDTH)
                    new_platform_y = -PLATFORM_HEIGHT
                    try:
                        new_platform = Platform(new_platform_x, new_platform_y)
                        platforms.add(new_platform)
                        all_sprites.add(new_platform)
                    except Exception as e:
                        print(f"Failed to generate platform at ({new_platform_x}, {new_platform_y}): {e}")
                        continue
        if current_level % THEME_INTERVAL == 0:
            current_theme += 1
        if current_level > LEVELS:
            # Game over or win condition
            running = False
        screen.fill(BLUE)
        all_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()
if __name__ == "__main__":
    main()