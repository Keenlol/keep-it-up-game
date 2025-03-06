import pygame as pg
import sys
from player import Player
from ball import Ball

class Game:
    def __init__(self, width=800, height=600):
        pg.init()
        self.screen = pg.display.set_mode((width, height))
        pg.display.set_caption("Keep IT Up")
        self.clock = pg.time.Clock()
        self.running = True
        self.load_assets()
        self.player = Player((100, 100))
        self.ground_y = 550
        self.ball = Ball((400, 100))  # Create ball in middle of screen

    def load_assets(self):
        # Load images and other assets here
        # Example: self.player_image = pg.image.load('path/to/player.png')
        pass

    def handle_events(self):

        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False

            #Key Pressed
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE or event.key == pg.K_w:
                    self.player.jump()
                if event.key == pg.K_s:
                    self.player.force_fall()

        #Key held
        held_key = pg.key.get_pressed()
        if held_key[pg.K_a]:
            self.player.move_left()
        if held_key[pg.K_d]:
            self.player.move_right()


    def update(self):
        self.player.update_movement()
        self.player.check_collision_with_ground(self.ground_y)
        self.ball.update()
        self.ball.check_collision_with_player(self.player, self.ground_y)
        self.ball.check_collision_with_ground(self.ground_y)

    def draw(self):
        self.screen.fill((0, 0, 0))  # Clear screen with black
        self.player.draw(self.screen)
        self.ball.draw(self.screen)
        pg.draw.line(self.screen, (255, 255, 255), (0, self.ground_y), (800, self.ground_y), 2)  # Draw the ground
        pg.display.flip()

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)  # Limit to 60 frames per second

if __name__ == "__main__":
    game = Game()
    game.run()
    pg.quit()
    sys.exit()
