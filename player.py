import pygame
import sys
from pygame.math import Vector2

class Player:
    def __init__(self, spawn_loc):
        self.position = Vector2(spawn_loc)
        self.velocity = Vector2(0, 0)
        self.acceleration = Vector2(0, 0)
        self.width = 30
        self.height = 50
        self.on_ground = False

        # Physics parameters
        self.acceleration_rate = 0.9
        self.deceleration_rate = 0.3
        self.max_speed = 5
        self.jump_strength = -10
        self.gravity = 0.5
        self.max_fall_speed = 10

    def move(self, keys):
        self.acceleration.x = 0

        if keys[pygame.K_a]:  # Move left
            self.acceleration.x = -self.acceleration_rate
        if keys[pygame.K_d]:  # Move right
            self.acceleration.x = self.acceleration_rate
        if keys[pygame.K_SPACE] or keys[pygame.K_w]:  # Jump
            if self.on_ground:
                self.velocity.y = self.jump_strength
                self.on_ground = False

        # Apply friction
        if self.velocity.x != 0:
            self.acceleration.x -= self.deceleration_rate * self.velocity.x / abs(self.velocity.x)

        # Update velocity and position
        self.velocity += self.acceleration
        self.velocity.y += self.gravity
        self.velocity.x = max(-self.max_speed, min(self.velocity.x, self.max_speed))
        self.velocity.y = min(self.velocity.y, self.max_fall_speed)

        self.position += self.velocity

    def check_collision_with_ground(self, ground_y):
        if self.position.y + self.height >= ground_y:
            self.position.y = ground_y - self.height
            self.velocity.y = 0
            self.on_ground = True

    def draw(self, screen):
        # Draw the player's hitbox
        pygame.draw.rect(screen, (255, 0, 0), (self.position.x, self.position.y, self.width, self.height))
