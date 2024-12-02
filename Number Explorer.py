import pygame
import sys

pygame.init()

tile_size = 50
screen_width = tile_size * 8
screen_height = tile_size * 8

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Number Explorer')

# Font
font = pygame.font.SysFont("arialblack", 20)
TEXT_COL = (255, 255, 255)

def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

class Player:
    def __init__(self, x, y, grid_size, screen_height, screen_width):
        # Load and scale the images for walking animation
        self.images_right = [pygame.transform.scale(pygame.image.load(f'img/player_right_{i}.png'), (grid_size, grid_size)) for i in range(1, 4)]
        self.images_left = [pygame.transform.scale(pygame.image.load(f'img/player_left_{i}.png'), (grid_size, grid_size)) for i in range(1, 4)]
        self.image = self.images_right[0]  # Default to the first frame
        self.rect = self.image.get_rect()
        self.rect.x = x * grid_size
        self.rect.y = y * grid_size
        self.grid_size = grid_size
        self.screen_height = screen_height
        self.screen_width = screen_width

        # Animation variables
        self.direction = 1  # 1 for right, -1 for left
        self.counter = 0
        self.index = 0
        self.walk_cooldown = 10  # Adjust for animation speed

        # Player stats
        self.score = 0
        self.traps_triggered = 0
        self.level = 1

    def move(self, traps, powerups):
        """Handles player movement, collision detection, and animation."""
        dx, dy = 0, 0
        key = pygame.key.get_pressed()

        if key[pygame.K_UP]:
            dy = -1
        if key[pygame.K_DOWN]:
            dy = 1
        if key[pygame.K_LEFT]:
            dx = -1
            self.direction = -1  # Facing left
        if key[pygame.K_RIGHT]:
            dx = 1
            self.direction = 1  # Facing right

        # New grid position
        new_x = (self.rect.x // self.grid_size) + dx
        new_y = (self.rect.y // self.grid_size) + dy

        # Ensure the player stays within bounds
        if 0 <= new_x < self.screen_width // self.grid_size and 0 <= new_y < self.screen_height // self.grid_size:
            self.rect.x += dx * self.grid_size
            self.rect.y += dy * self.grid_size

            # Check for trap collision
            if (new_x, new_y) in traps:
                self.traps_triggered += 1
                traps.remove((new_x, new_y))  # Clear trap after collision

            # Check for power-up collision
            if (new_x, new_y) in powerups:
                self.collect_powerup(powerups, (new_x, new_y))

            # Update score
            self.score += 1  # Points for moving

        # Handle walking animation
        if dx != 0 or dy != 0:
            self.counter += 1
            if self.counter > self.walk_cooldown:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images_right):
                    self.index = 0
                if self.direction == 1:
                    self.image = self.images_right[self.index]
                if self.direction == -1:
                    self.image = self.images_left[self.index]
        else:
            # Reset animation if the player stops moving
            self.index = 0
            if self.direction == 1:
                self.image = self.images_right[0]
            else:
                self.image = self.images_left[0]

    def collect_powerup(self, powerups, position):
        """Handles power-up effects."""
        print(f"Collected power-up at {position}!")
        powerups.remove(position)

    def draw(self, screen):
        """Draw the player onto the screen."""
        screen.blit(self.image, self.rect)


class World:
    def __init__(self, data, tile_size):
        self.tile_list = []
        self.traps = set()
        self.powerups = set()
        trap_img = pygame.image.load('img/trap.png')
        powerup_img = pygame.image.load('img/powerup.png')
        empty_img = pygame.image.load('img/empty.png')

        for row_idx, row in enumerate(data):
            for col_idx, tile in enumerate(row):
                if tile == 1:
                    img = pygame.transform.scale(trap_img, (tile_size, tile_size))
                    self.traps.add((col_idx, row_idx))
                elif tile == 2:
                    img = pygame.transform.scale(powerup_img, (tile_size, tile_size))
                    self.powerups.add((col_idx, row_idx))
                else:
                    img = pygame.transform.scale(empty_img, (tile_size, tile_size))
                
                img_rect = img.get_rect()
                img_rect.x = col_idx * tile_size
                img_rect.y = row_idx * tile_size
                self.tile_list.append((img, img_rect))

    def draw(self, screen):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])

world_data = [
    [0, 0, 0, 1, 0, 0, 2, 0],
    [0, 2, 0, 0, 0, 1, 0, 0],
    [1, 0, 0, 0, 2, 0, 0, 1],
    [0, 0, 1, 0, 0, 0, 2, 0],
    [0, 1, 0, 0, 0, 2, 0, 0],
    [2, 0, 0, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 0, 2],
    [0, 0, 2, 0, 0, 0, 1, 0],
]

clock = pygame.time.Clock()
player = Player(0, 7, tile_size, screen_height, screen_width)
world = World(world_data, tile_size)

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    screen.fill((255, 221, 174))
    world.draw(screen)
    player.move(world.traps, world.powerups)
    player.draw(screen)
    pygame.display.flip()
    clock.tick(30)

pygame.quit()
