import pygame as pg
from pygame.math import Vector2
from player import Player

class Ball:
    def __init__(self, spawn_loc):
        self.position = Vector2(spawn_loc)
        self.velocity = Vector2(0, 0)
        self.radius = 20
        self.is_overlap_player = False
        self.energy = 0

        # Physics parameters
        self.gravity = 0.3
        self.max_fall_speed = 15
        self.bounce_strength = 8
        self.max_bounce_strength = 80
        self.elastic = 0.6
        self.horizontal_influence = 0.08  # How much player's horizontal speed affects ball
        self.vertical_influence = 0.3    # How much player's vertical speed affects ball
        self.position_influence = 0.01
        
    def update(self):
        # Apply gravity
        self.velocity.y += self.gravity
        self.velocity.y = self.velocity.y#, self.max_fall_speed
        
        # Update position
        self.position += self.velocity

    def check_collision_with_ground(self, ground_y):
        if self.position.y + self.radius >= ground_y and self.velocity.y > 0:
            self.position.y = ground_y - self.radius
            self.velocity.y *= -self.elastic
            self.velocity.x += -self.velocity.x * self.elastic
            self.energy = 0
            
    def check_collision_with_player(self, player:Player, ground_y):
        # Player's edges
        closest_x = max(player.position.x, min(self.position.x, player.position.x + player.width))
        closest_y = max(player.position.y, min(self.position.y, player.position.y + player.height))

        distance = Vector2(self.position.x - closest_x, self.position.y - closest_y).length()
        
        if distance < self.radius and not self.is_overlap_player:
            # Player jumped on top of the ball, stomping it.
            if self.position.y + self.radius >= ground_y - 20 and player.velocity.y > 0:
                self.velocity = Vector2(0, -13)
            # normal bouncing
            else:
                # Calculate bounce direction based on player's velocity
                bounce_direction = Vector2(0, -1)  # Default upward bounce
                
                # player velocity influence
                bounce_direction.x += player.velocity.x * self.horizontal_influence
                
                # player position influence
                player_center_x = player.position.x + player.width/2
                ball_center_x = self.position.x
                position_difference = ball_center_x - player_center_x
                bounce_direction.x += position_difference * self.position_influence
                
                # Normalize and apply bounce
                if bounce_direction.length() > 0:
                    bounce_direction = bounce_direction.normalize()
                self.velocity = bounce_direction * self.bounce_strength
                print("vel y", min(player.velocity.y, 0) * self.vertical_influence - self.energy * 0.01)
                self.velocity.y += min(player.velocity.y, 0) * self.vertical_influence - self.energy * 0.01
                
            self.is_overlap_player = True
            self.energy += abs(self.velocity.y)

        elif distance > self.radius + 10:
            self.is_overlap_player = False
            
    def draw(self, screen):
        pg.draw.circle(screen, (255, 255, 0), (int(self.position.x), int(self.position.y)), self.radius)

    def luanch(self, mouse_xy: tuple):
        mx = mouse_xy[0]
        my = mouse_xy[1]

        direction = Vector2(mx - self.position.x, my - self.position.y).normalize()
        self.velocity = direction * (15 + self.energy)

    def check_window_bounds(self, left_bound, right_bound):
        # Bounce off horizontal bounds
        if self.position.x - self.radius < left_bound:
            self.position.x = left_bound + self.radius
            self.velocity.x *= -self.elastic
        elif self.position.x + self.radius > right_bound:
            self.position.x = right_bound - self.radius
            self.velocity.x *= -self.elastic