import pytest
from game import Snake, Food, GRID_WIDTH, GRID_HEIGHT, SNAKE_COLORS

def test_snake_initial_state():
    snake = Snake()
    assert snake.length == 31
    assert len(snake.positions) == 1
    assert snake.positions[0] == (GRID_WIDTH // 2, GRID_HEIGHT // 2)
    assert snake.direction == (1, 0)

def test_snake_color_cycling():
    snake = Snake()
    total_colors = len(SNAKE_COLORS)
    
    # Test color cycling
    assert snake.get_color_index(0) == 0
    assert snake.get_color_index(1) == 1
    assert snake.get_color_index(total_colors - 1) == total_colors - 1
    assert snake.get_color_index(total_colors) == 0
    
    # Test color offset update
    initial_offset = snake.color_offset
    snake.update_colors()
    assert snake.color_offset != initial_offset
    assert snake.color_offset == (initial_offset + snake.cycle_speed) % total_colors

def test_snake_movement():
    snake = Snake()
    initial_pos = snake.get_head_position()
    
    # Test moving right (initial direction)
    assert snake.move() == True
    new_pos = snake.get_head_position()
    assert new_pos == ((initial_pos[0] + 1) % GRID_WIDTH, initial_pos[1])
    
    # Test moving down
    snake.turn((0, 1))
    assert snake.move() == True
    newer_pos = snake.get_head_position()
    assert newer_pos == (new_pos[0], (new_pos[1] + 1) % GRID_HEIGHT)

def test_snake_growth():
    snake = Snake()
    initial_length = snake.length
    
    # Move a few times without growing
    for _ in range(3):
        snake.move()
    assert len(snake.positions) == initial_length
    
    # Simulate eating food by increasing length
    snake.length += 1
    for _ in range(3):
        snake.move()
    assert len(snake.positions) == initial_length + 1

def test_snake_collision():
    snake = Snake()
    snake.length = 4
    
    # Create a scenario where snake will collide with itself
    # Move right to grow
    for _ in range(4):
        snake.move()
    
    # Turn down
    snake.turn((0, 1))
    snake.move()
    
    # Turn left
    snake.turn((-1, 0))
    snake.move()
    
    # Turn up - this should cause collision
    snake.turn((0, -1))
    assert snake.move() == False

def test_snake_direction_reversal():
    snake = Snake()
    snake.length = 2
    snake.move()  # Get length to 2
    
    # Try to reverse direction (should be ignored)
    initial_direction = snake.direction
    snake.turn((-1 * initial_direction[0], -1 * initial_direction[1]))
    assert snake.direction == initial_direction

def test_food_spawning():
    food = Food()
    snake_positions = [(5, 5), (5, 6), (5, 7)]
    
    # Test initial spawn
    assert 0 <= food.position[0] < GRID_WIDTH
    assert 0 <= food.position[1] < GRID_HEIGHT
    
    # Test spawning with snake positions
    food.randomize_position(snake_positions)
    assert food.position not in snake_positions
    assert 0 <= food.position[0] < GRID_WIDTH
    assert 0 <= food.position[1] < GRID_HEIGHT

def test_food_collision():
    snake = Snake()
    food = Food()
    
    # Place food directly in front of snake
    next_pos = ((snake.get_head_position()[0] + 1) % GRID_WIDTH,
                snake.get_head_position()[1])
    food.position = next_pos
    
    # Move snake to food position
    assert snake.move() == True
    assert snake.get_head_position() == food.position