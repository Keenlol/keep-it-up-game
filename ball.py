import pygame as pg
from pygame.math import Vector2
from player import Player

class Ball:
    def __init__(self, spawn_loc):
        self.position = Vector2(spawn_loc)
        self.velocity = Vector2(0, 0)
        self.radius = 20
        
        # Physics parameters
        self.gravity = 0.3
        self.max_fall_speed = 15
        self.bounce_strength = 8
        self.horizontal_influence = 0.1  # How much player's horizontal speed affects ball
        self.vertical_influence = 0.9    # How much player's vertical speed affects ball
        
    def update(self):
        # Apply gravity
        self.velocity.y += self.gravity
        self.velocity.y = min(self.velocity.y, self.max_fall_speed)
        
        # Update position
        self.position += self.velocity
        
    def check_collision_with_ground(self, ground_y):
        if self.position.y + self.radius >= ground_y:
            self.position.y = ground_y - self.radius
            self.velocity.y = -self.bounce_strength * 0.2  # Bounce with 60% strength
            
    def check_collision_with_player(self, player:Player):
        # Calculate the closest point on the rectangle to the circle
        closest_x = max(player.position.x, min(self.position.x, player.position.x + player.width))
        closest_y = max(player.position.y, min(self.position.y, player.position.y + player.height))
        
        # Calculate distance between the circle's center and the closest point
        distance = Vector2(self.position.x - closest_x, self.position.y - closest_y).length()
        
        # If distance is less than the circle's radius, collision occurred
        if distance < self.radius:
            # Calculate bounce direction based on player's velocity
            bounce_direction = Vector2(0, -1)  # Default upward bounce
            
            # Add player's velocity influence
            bounce_direction.x += player.velocity.x * self.horizontal_influence
            bounce_direction.y += min(player.velocity.y, 0) * self.vertical_influence
            
            # Normalize and apply bounce
            if bounce_direction.length() > 0:
                bounce_direction = bounce_direction.normalize()
            self.velocity = bounce_direction * self.bounce_strength
            
            # Move ball outside of player to prevent multiple collisions
            overlap = self.radius - distance
            self.position += bounce_direction * overlap
            
    def draw(self, screen):
        pg.draw.circle(screen, (255, 255, 0), (int(self.position.x), int(self.position.y)), self.radius)