import pygame
import sys
from player import Player

class Game:
    def __init__(self, width=800, height=600):
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Keep IT Up")
        self.clock = pygame.time.Clock()
        self.running = True
        self.load_assets()
        self.player = Player((100, 100))
        self.ground_y = 550

    def load_assets(self):
        # Load images and other assets here
        # Example: self.player_image = pygame.image.load('path/to/player.png')
        pass

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            # Handle other events like key presses here

    def update(self):
        keys = pygame.key.get_pressed()
        self.player.move(keys)
        self.player.check_collision_with_ground(self.ground_y)

    def draw(self):
        self.screen.fill((0, 0, 0))  # Clear screen with black
        self.player.draw(self.screen)
        pygame.draw.line(self.screen, (255, 255, 255), (0, self.ground_y), (800, self.ground_y), 2)  # Draw the ground
        pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)  # Limit to 60 frames per second

if __name__ == "__main__":
    game = Game()
    game.run()
    pygame.quit()
    sys.exit()
