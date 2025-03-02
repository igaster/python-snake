import pygame
import sys
from typing import Tuple, List

# Initialize Pygame
pygame.init()

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
GRID_SIZE = 20
GRID_WIDTH = WINDOW_WIDTH // GRID_SIZE
GRID_HEIGHT = WINDOW_HEIGHT // GRID_SIZE
SPEED = 10  # Controls game speed (moves per second)

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
RED = (255, 0, 0)

# Text colors
TEXT_COLORS = {
    'score': WHITE,  # Use white color for score display
    'game_over': WHITE,  # Use white color for game over text
    'menu': WHITE  # Use white color for menu text
}

# Pantone-inspired colors for snake segments
SNAKE_COLORS = [
    (0, 168, 107),    # Pantone 2420 - Green
    (0, 172, 140),    # Pantone 2419
    (0, 176, 173),    # Pantone 2418
    (0, 180, 206),    # Pantone 2417
    (0, 184, 239),    # Pantone 2416
    (0, 188, 242),    # Pantone 2415
    (0, 192, 245),    # Pantone 2414
    (0, 196, 248),    # Pantone 2413
    (0, 200, 251),    # Pantone 2412
    (0, 204, 254),    # Pantone 2411 - Blue
    (102, 157, 246),  # Pantone 2716
    (157, 122, 210),  # Pantone 2715
    (183, 102, 196),  # Pantone 2714
    (198, 87, 183),   # Pantone 2713
    (213, 72, 170),   # Pantone 2712
    (228, 57, 157),   # Pantone 2711
    (243, 42, 144),   # Pantone 2710
    (255, 20, 130),   # Pantone 2709
    (255, 0, 116),    # Pantone 2708 - Pink
    (255, 0, 102)     # Pantone 2707 - Deep Pink
]

class Button:
    def __init__(self, x: int, y: int, width: int, height: int, text: str):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = WHITE
        self.active = False
        self.is_hovered = False
        self.bg_color = (50, 50, 50)  # Soft dark background for active state

    def draw(self, screen):
        if self.active or self.is_hovered:
            pygame.draw.rect(screen, self.bg_color, self.rect)  # Draw background when active
            pygame.draw.rect(screen, self.color, self.rect, 3)  # Thicker border (3 pixels) when active
        else:
            pygame.draw.rect(screen, self.color, self.rect, 1)  # Normal border (1 pixel) when inactive
        
        font = pygame.font.Font(None, 36)
        text = font.render(self.text, True, self.color)
        text_rect = text.get_rect(center=self.rect.center)
        screen.blit(text, text_rect)

    def handle_event(self, event) -> bool:
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                return True
        return False

class Slider:
    def __init__(self, x: int, y: int, width: int, min_val: int, max_val: int, initial_val: int):
        self.rect = pygame.Rect(x, y, width, 10)
        self.min_val = min_val
        self.max_val = max_val
        self.value = initial_val
        self.handle_rect = pygame.Rect(0, 0, 20, 20)
        self.update_handle_pos()
        self.dragging = False

    def update_handle_pos(self):
        val_range = self.max_val - self.min_val
        pos = ((self.value - self.min_val) / val_range) * self.rect.width
        self.handle_rect.centerx = self.rect.left + pos
        self.handle_rect.centery = self.rect.centery

    def draw(self, screen):
        pygame.draw.rect(screen, WHITE, self.rect)
        pygame.draw.rect(screen, GRAY, self.handle_rect)

    def handle_event(self, event) -> bool:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.handle_rect.collidepoint(event.pos):
                self.dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            rel_x = min(max(event.pos[0], self.rect.left), self.rect.right)
            rel_pos = (rel_x - self.rect.left) / self.rect.width
            self.value = int(self.min_val + (self.max_val - self.min_val) * rel_pos)
            self.update_handle_pos()
            return True
        return False

class Snake:
    def __init__(self):
        self.length = 3
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = (1, 0)  # Start moving right
        self.move_timer = 0
        self.color_offset = 0.0  # Add color offset for smooth cycling
        self.cycle_speed = 0.1   # Controls how fast colors cycle

    def get_head_position(self) -> Tuple[int, int]:
        return self.positions[0]

    def move(self):
        cur = self.get_head_position()
        x, y = self.direction
        new = ((cur[0] + x) % GRID_WIDTH, (cur[1] + y) % GRID_HEIGHT)
        if new in self.positions[3:]:
            return False  # Game over
        self.positions.insert(0, new)
        if len(self.positions) > self.length:
            self.positions.pop()
        return True

    def turn(self, direction: Tuple[int, int]):
        if len(self.positions) > 1 and \
           (direction[0] * -1, direction[1] * -1) == self.direction:
            return  # Prevent reversing direction
        self.direction = direction

    def get_color_index(self, segment_index: int) -> int:
        total_colors = len(SNAKE_COLORS)
        # Mathematical formula for color cycling:
        # (segment_index + color_offset) modulo total_colors
        # This creates a continuous flow of colors through the snake
        index = (segment_index + int(self.color_offset)) % total_colors
        return index

    def update_colors(self):
        # Update the color offset for continuous cycling
        self.color_offset = (self.color_offset + self.cycle_speed) % len(SNAKE_COLORS)

class Food:
    def __init__(self):
        self.position = (0, 0)
        self.color = RED
        self.randomize_position([])

    def randomize_position(self, snake_positions: List[Tuple[int, int]]):
        import random
        while True:
            self.position = (random.randint(0, GRID_WIDTH-1),
                           random.randint(0, GRID_HEIGHT-1))
            if self.position not in snake_positions:
                break

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Snake Game')
        self.clock = pygame.time.Clock()
        self.fps = 60
        self.move_timer = 0
        self.snake = None
        self.food = None
        self.score = 0
        self.game_over = False
        self.game_speed = SPEED
        self.state = 'menu'  # 'menu', 'settings', 'playing'
        self.font = pygame.font.Font(None, 36)  # Initialize font
        
        # Create menu buttons
        btn_width, btn_height = 200, 50
        center_x = WINDOW_WIDTH // 2 - btn_width // 2
        self.start_button = Button(center_x, 200, btn_width, btn_height, 'Start Game')
        self.settings_button = Button(center_x, 300, btn_width, btn_height, 'Settings')
        self.back_button = Button(center_x, 400, btn_width, btn_height, 'Back')
        
        # Create speed slider
        self.speed_slider = Slider(center_x, 250, btn_width, 5, 20, SPEED)

    def init_game(self):
        self.snake = Snake()
        self.food = Food()
        self.score = 0
        self.game_over = False
        self.game_speed = self.speed_slider.value

    def handle_menu_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                elif self.state == 'menu':
                    if event.key == pygame.K_UP:
                        self.settings_button.is_hovered = False
                        self.start_button.is_hovered = True
                    elif event.key == pygame.K_DOWN:
                        self.start_button.is_hovered = False
                        self.settings_button.is_hovered = True
                    elif event.key == pygame.K_RETURN:
                        if self.start_button.is_hovered:
                            self.state = 'playing'
                            self.init_game()
                        elif self.settings_button.is_hovered:
                            self.state = 'settings'
                elif self.state == 'settings':
                    if event.key == pygame.K_RETURN and self.back_button.is_hovered:
                        self.state = 'menu'
                    elif event.key == pygame.K_UP:
                        self.back_button.is_hovered = False
                    elif event.key == pygame.K_DOWN:
                        self.back_button.is_hovered = True
                    elif event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                        change = -1 if event.key == pygame.K_LEFT else 1
                        new_value = max(self.speed_slider.min_val, min(self.speed_slider.max_val, self.speed_slider.value + change))
                        self.speed_slider.value = new_value
                        self.speed_slider.update_handle_pos()
                        self.game_speed = new_value

            if self.state == 'menu':
                if self.start_button.handle_event(event):
                    self.state = 'playing'
                    self.init_game()
                elif self.settings_button.handle_event(event):
                    self.state = 'settings'
            elif self.state == 'settings':
                if self.back_button.handle_event(event):
                    self.state = 'menu'
                elif self.speed_slider.handle_event(event):
                    self.game_speed = self.speed_slider.value

        return True

    def draw_menu(self):
        self.screen.fill(BLACK)
        if self.state == 'menu':
            self.start_button.draw(self.screen)
            self.settings_button.draw(self.screen)
        elif self.state == 'settings':
            font = pygame.font.Font(None, 36)
            text = font.render(f'Game Speed: {self.speed_slider.value}', True, WHITE)
            text_rect = text.get_rect(center=(WINDOW_WIDTH//2, 200))
            self.screen.blit(text, text_rect)
            self.speed_slider.draw(self.screen)
            self.back_button.draw(self.screen)
        pygame.display.flip()

    def handle_events(self):
        if self.state != 'playing':
            return self.handle_menu_events()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.state = 'menu'
                    return True
                elif event.key == pygame.K_UP:
                    self.snake.turn((0, -1))
                elif event.key == pygame.K_DOWN:
                    self.snake.turn((0, 1))
                elif event.key == pygame.K_LEFT:
                    self.snake.turn((-1, 0))
                elif event.key == pygame.K_RIGHT:
                    self.snake.turn((1, 0))
        return True

    def update(self):
        if self.state != 'playing' or self.game_over:
            return

        # Update game speed based on snake length
        base_speed = self.speed_slider.value
        length_bonus = self.snake.length // 10
        self.game_speed = base_speed + length_bonus

        self.move_timer += 1
        if self.move_timer >= self.fps / self.game_speed:
            self.move_timer = 0
            if not self.snake.move():
                self.game_over = True
                return

            if self.snake.get_head_position() == self.food.position:
                self.snake.length += 1
                self.score += 1
                self.food.randomize_position(self.snake.positions)

    def draw(self):
        if self.state != 'playing':
            self.draw_menu()
            return

        self.screen.fill(BLACK)
        
        # Draw grid with semi-transparent dotted lines
        grid_color = (128, 128, 128, 64)  # Semi-transparent gray
        grid_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        
        # Draw vertical grid lines
        for x in range(0, WINDOW_WIDTH, GRID_SIZE):
            for y in range(0, WINDOW_HEIGHT, 2):  # Draw dotted lines
                if y % 4 == 0:  # Skip every other dot to create dotted effect
                    pygame.draw.line(grid_surface, grid_color, (x, y), (x, y + 1))
        
        # Draw horizontal grid lines
        for y in range(0, WINDOW_HEIGHT, GRID_SIZE):
            for x in range(0, WINDOW_WIDTH, 2):  # Draw dotted lines
                if x % 4 == 0:  # Skip every other dot to create dotted effect
                    pygame.draw.line(grid_surface, grid_color, (x, y), (x + 1, y))
        
        # Blit the grid surface onto the screen
        self.screen.blit(grid_surface, (0, 0))
        
        # Draw snake length and speed with semi-transparent background
        font = pygame.font.Font(None, 36)
        # Create a surface for the OSD with alpha channel
        osd_surface = pygame.Surface((400, 30), pygame.SRCALPHA)  # Reduced height, increased width
        pygame.draw.rect(osd_surface, (0, 0, 0, 128), (0, 0, 400, 30))  # Semi-transparent black background
        
        # Render text with smaller font
        font = pygame.font.Font(None, 24)  # Reduced font size
        text = font.render(f'🐍 {self.snake.length}   ⚡ {self.game_speed}', True, TEXT_COLORS['score'])
        text_rect = text.get_rect(center=(200, 15))  # Center text in OSD surface
        osd_surface.blit(text, text_rect)
        
        # Center OSD surface at the top of the screen
        self.screen.blit(osd_surface, (WINDOW_WIDTH//2 - 200, 10))
        
        # Draw snake segments with rounded corners
        for i, pos in enumerate(self.snake.positions):
            color_index = self.snake.get_color_index(i)
            
            # Draw main segment body
            rect = pygame.Rect(pos[0] * GRID_SIZE, pos[1] * GRID_SIZE,
                             GRID_SIZE-1, GRID_SIZE-1)
            pygame.draw.rect(self.screen, SNAKE_COLORS[color_index], rect, border_radius=5)
            
            # Draw rounded connection if not the last segment
            if i < len(self.snake.positions) - 1:
                next_pos = self.snake.positions[i + 1]
                # Calculate direction between current and next segment
                dx = next_pos[0] - pos[0]
                dy = next_pos[1] - pos[1]
                
                # Handle wrap-around cases
                if abs(dx) > 1:
                    dx = -1 if dx > 0 else 1
                if abs(dy) > 1:
                    dy = -1 if dy > 0 else 1
                
                # Draw connection rectangle with rounded corners
                if dx != 0:  # Horizontal connection
                    connect_rect = pygame.Rect(
                        min(pos[0], pos[0] + dx) * GRID_SIZE + GRID_SIZE//2,
                        pos[1] * GRID_SIZE,
                        abs(dx) * GRID_SIZE,
                        GRID_SIZE-1
                    )
                    pygame.draw.rect(self.screen, SNAKE_COLORS[color_index], connect_rect, border_radius=5)
                elif dy != 0:  # Vertical connection
                    connect_rect = pygame.Rect(
                        pos[0] * GRID_SIZE,
                        min(pos[1], pos[1] + dy) * GRID_SIZE + GRID_SIZE//2,
                        GRID_SIZE-1,
                        abs(dy) * GRID_SIZE
                    )
                    pygame.draw.rect(self.screen, SNAKE_COLORS[color_index], connect_rect, border_radius=5)

        # Draw food
        rect = pygame.Rect(self.food.position[0] * GRID_SIZE,
                         self.food.position[1] * GRID_SIZE,
                         GRID_SIZE-1, GRID_SIZE-1)
        pygame.draw.rect(self.screen, self.food.color, rect, border_radius=5)

        if self.game_over:
            font = pygame.font.Font(None, 48)
            text = font.render('Game Over! Press ESC for Menu', True, WHITE)
            text_rect = text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2))
            self.screen.blit(text, text_rect)

        pygame.display.flip()

    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(self.fps)

        pygame.quit()
        sys.exit()

if __name__ == '__main__':
    game = Game()
    game.run()