import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 538, 948
GRID_SIZE = 40
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE
FPS = 10

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

# Load assets
snake_head = pygame.image.load("snake_head.png")
snake_body = pygame.image.load("snake_body.png")
food = pygame.image.load("food.png")
background = pygame.image.load("background.jpg")
start_screen = pygame.image.load("kkk.webp")
game_over_screen = pygame.image.load("head_f.png")

# Resize assets to match grid size
snake_head = pygame.transform.scale(snake_head, (GRID_SIZE, GRID_SIZE))
snake_body = pygame.transform.scale(snake_body, (GRID_SIZE, GRID_SIZE))
food = pygame.transform.scale(food, (GRID_SIZE, GRID_SIZE))
background = pygame.transform.scale(background, (WIDTH, HEIGHT))
start_screen = pygame.transform.scale(start_screen, (WIDTH, HEIGHT))
game_over_screen = pygame.transform.scale(game_over_screen, (WIDTH, HEIGHT))

# Font
font = pygame.font.Font(None, 36)

# Blur the background
def blur_surface(surface, amount):
    scale = 1.0 / float(amount)
    surf_size = surface.get_size()
    scale_size = (int(surf_size[0] * scale), int(surf_size[1] * scale))
    surf = pygame.transform.smoothscale(surface, scale_size)
    surf = pygame.transform.smoothscale(surf, surf_size)
    return surf

blurred_background =  background #blur_surface(background, 3)

# Create a glowing effect for food
def create_glow_surface(size, color, intensity):
    glow = pygame.Surface((size * 3, size * 3), pygame.SRCALPHA)
    pygame.draw.circle(glow, (*color, 0), (size * 1.5, size * 1.5), size * 1.5)
    for i in range(size):
        alpha = int((1 - float(i) / size) * intensity)
        pygame.draw.circle(glow, (*color, alpha), (size * 1.5, size * 1.5), size * 1.5 - i)
    return glow

glow_surface = create_glow_surface(GRID_SIZE, (255, 255, 0), 160)

class Snake:
    def __init__(self):
        self.body = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = RIGHT
        self.grow = False
        self.turns = {}

    def move(self):
        head = self.body[0]
        new_head = (head[0] + self.direction[0], head[1] + self.direction[1])
        
        # Check if the new head position is out of bounds
        if (new_head[0] < 0 or new_head[0] >= GRID_WIDTH or
            new_head[1] < 0 or new_head[1] >= GRID_HEIGHT):
            return False  # Game over

        self.body.insert(0, new_head)
        if not self.grow:
            self.body.pop()
        else:
            self.grow = False

        self.turns[self.body[0]] = self.direction
        return True  # Continue game
    def change_direction(self, new_direction):
        if (new_direction[0] * -1, new_direction[1] * -1) != self.direction:
            self.direction = new_direction
            self.turns[self.body[0]] = self.direction

    def check_collision(self):
        return len(self.body) != len(set(self.body))

def generate_food(snake):
    while True:
        food_pos = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
        if food_pos not in snake.body:
            return food_pos

def get_angle(direction):
    return {UP: 90, DOWN: -90, LEFT: 180, RIGHT: 0}[direction]

def draw_score(screen, score):
    score_surface = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_surface, (10, 10))

def draw_game_over(screen, score):
    screen.blit(game_over_screen, (0, 0))
    game_over_surface = font.render("Game Over", True, RED)
    score_surface = font.render(f"Final Score: {score}", True, WHITE)
    replay_surface = font.render("Press SPACE to replay", True, WHITE)
    
    screen.blit(game_over_surface, (WIDTH // 2 - game_over_surface.get_width() // 2, HEIGHT // 2 - 60))
    screen.blit(score_surface, (WIDTH // 2 - score_surface.get_width() // 2, HEIGHT // 2))
    screen.blit(replay_surface, (WIDTH // 2 - replay_surface.get_width() // 2, HEIGHT // 2 + 60))
    
    pygame.display.flip()

def main():
    clock = pygame.time.Clock()
    snake = Snake()
    food_pos = generate_food(snake)
    running = True
    score = 0
    food_alpha = 255
    food_alpha_change = -5

    # Display the start screen
    screen.blit(start_screen, (0, 0))
    start_text = font.render("*** PRESS SPACE TO START ***", True, RED)
    screen.blit(start_text, (WIDTH // 2 - start_text.get_width() // 2, HEIGHT // 2 + 60))


    pygame.display.flip()

    # Wait for the user to press the space key to start the game
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                waiting = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    snake.change_direction(UP)
                elif event.key == pygame.K_DOWN:
                    snake.change_direction(DOWN)
                elif event.key == pygame.K_LEFT:
                    snake.change_direction(LEFT)
                elif event.key == pygame.K_RIGHT:
                    snake.change_direction(RIGHT)

        if not snake.move():  # Game over if move returns False
            draw_game_over(screen, score)
            waiting = True
            while waiting:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        return
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                        waiting = False
                        snake = Snake()
                        food_pos = generate_food(snake)
                        score = 0
            continue

        if snake.body[0] == food_pos:
            snake.grow = True
            food_pos = generate_food(snake)
            score += 1

        if snake.check_collision():
            draw_game_over(screen, score)
            waiting = True
            while waiting:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        return
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                        waiting = False
                        snake = Snake()
                        food_pos = generate_food(snake)
                        score = 0
            continue

        screen.blit(blurred_background, (0, 0))

        # Draw glowing food
        food_alpha += food_alpha_change
        if food_alpha <= 100 or food_alpha >= 255:
            food_alpha_change *= -1
        glow_surface.set_alpha(food_alpha)
        screen.blit(glow_surface, ((food_pos[0] * GRID_SIZE) - GRID_SIZE, (food_pos[1] * GRID_SIZE) - GRID_SIZE))
        screen.blit(food, (food_pos[0] * GRID_SIZE, food_pos[1] * GRID_SIZE))

        # Draw snake
        for i, segment in enumerate(snake.body):
            if i == 0:
                angle = get_angle(snake.direction)
            else:
                prev_segment = snake.body[i-1]
                next_segment = snake.body[i+1] if i+1 < len(snake.body) else None
                
                if next_segment:
                    dx, dy = prev_segment[0] - next_segment[0], prev_segment[1] - next_segment[1]
                    if dx != 0:
                        angle = 0 if dx > 0 else 180
                    else:
                        angle = 90 if dy < 0 else -90
                else:
                    dx, dy = segment[0] - prev_segment[0], segment[1] - prev_segment[1]
                    if dx != 0:
                        angle = 0 if dx < 0 else 180
                    else:
                        angle = 90 if dy > 0 else -90

            image = snake_head if i == 0 else snake_body
            rotated_image = pygame.transform.rotate(image, angle)
            screen.blit(rotated_image, (segment[0] * GRID_SIZE, segment[1] * GRID_SIZE))

        draw_score(screen, score)
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
