# Python Snake Game

A classic Snake game implementation using Python and Pygame.

## Project Overview
This project is a modern recreation of the classic Snake game where players control a snake that grows longer as it eats food while avoiding collisions with walls and itself.

## Dependencies
- Python 3.x
- Pygame

## Installation
1. Ensure Python 3.x is installed on your system
2. Install Pygame using pip:
```bash
pip install pygame
```

## Game Features
- Snake movement with smooth controls
- Score tracking system
- Food spawning mechanics
- Collision detection
- Game over and restart functionality
- Progressive difficulty

## Controls
- Arrow Keys: Move snake
  - ↑: Up
  - ↓: Down
  - ←: Left
  - →: Right
- SPACE: Start/Restart game
- ESC: Pause game
- Q: Quit game

## Game Mechanics
1. The snake moves continuously in the current direction
2. Eating food:
   - Increases snake length
   - Adds to score
   - Spawns new food in random location
3. Game ends when snake:
   - Hits the walls
   - Collides with itself

## Configuration
### Window Settings
- Resolution: 800x600 pixels
- Grid Size: 20x20 pixels
- FPS: 60

### Game Settings
- Initial Snake Length: 3
- Starting Speed: 10 units/second
- Speed Increase: 5% after each food
- Background Color: Black
- Snake Color: Green
- Food Color: Red

## Development Goals
### Phase 1: Core Game
- [ ] Set up game window
- [ ] Implement snake movement
- [ ] Add food spawning
- [ ] Create collision detection

### Phase 2: Game Logic
- [ ] Score system
- [ ] Speed progression
- [ ] Game over state
- [ ] Restart functionality

### Phase 3: Polish
- [ ] Add sound effects
- [ ] Create menu system
- [ ] Implement high scores
- [ ] Add visual effects