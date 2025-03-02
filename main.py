import pygame
import asyncio
from game import Game

async def main():
    game = Game()
    running = True
    
    while running:
        running = game.handle_events()
        game.update()
        game.draw()
        pygame.display.flip()
        game.clock.tick(game.fps)
        # Add small delay for browser compatibility
        await asyncio.sleep(0)

    pygame.quit()

if __name__ == "__main__":
    asyncio.run(main())