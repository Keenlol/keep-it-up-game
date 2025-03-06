import pygame as pg
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
        self.force_falling = False
        self.jump_count = 0  # Track the number of jumps

        # Physics parameters
        self.acceleration_rate = 0.9
        self.deceleration_rate = 0.3
        self.max_speed = 5
        self.jump_strength = -10
        self.gravity = 0.5
        self.max_fall_speed = 10
        self.force_fall_speed = 20  # Increased fall speed for force falling

    def move_left(self):
        self.acceleration.x = -self.acceleration_rate

    def move_right(self):
        self.acceleration.x = self.acceleration_rate

    def jump(self):
        if self.on_ground or self.jump_count < 2:  # Allow double jump
                self.velocity.y = self.jump_strength
                self.on_ground = False
                self.jump_count += 1

    def force_fall(self):
        self.force_falling = True

    def update_movement(self):
        # Apply friction
        if self.velocity.x != 0:
            self.acceleration.x -= self.deceleration_rate * self.velocity.x / abs(self.velocity.x)

        # Update velocity and position
        self.velocity += self.acceleration
        self.velocity.y += self.gravity
        self.velocity.x = max(-self.max_speed, min(self.velocity.x, self.max_speed))

        #Prevent sliding on the floor

        if self.force_falling:
            self.velocity.y = self.force_fall_speed
        else:
            self.velocity.y = min(self.velocity.y, self.max_fall_speed)

        self.position += self.velocity
        self.acceleration.x = 0

    def check_collision_with_ground(self, ground_y):
        if self.position.y + self.height >= ground_y:
            self.position.y = ground_y - self.height
            self.velocity.y = 0
            self.on_ground = True
            self.force_falling = False
            self.jump_count = 0  # Reset jump count when on the ground

    def draw(self, screen):
        # print(self.velocity.x)
        print(self.jump_count)
        # Draw the player's hitbox
        pg.draw.rect(screen, (255, 0, 0), (self.position.x, self.position.y, self.width, self.height))
