import pygame
import random
import math

class Ball:
    def __init__(self, x, y, width, height, screen_width, screen_height):
        # Original and current position
        self.original_x = x
        self.original_y = y
        self.x = x
        self.y = y
        self.prev_x = x
        self.prev_y = y

        self.width = width
        self.height = height
        self.screen_width = screen_width
        self.screen_height = screen_height

        # Random initial velocity
        self.velocity_x = random.choice([-5, 5])
        self.velocity_y = random.choice([-3, 3])
        self.vx = self.velocity_x
        self.vy = self.velocity_y

        # For collision detection
        self.radius = width // 2

    def move(self):
        # Store previous position
        self.prev_x, self.prev_y = self.x, self.y

        # Move ball
        self.x += self.vx
        self.y += self.vy

        # Bounce off top and bottom edges
        if self.y - self.radius < 0:
            self.y = self.radius
            self.vy *= -1
            if hasattr(self, 'game_engine'):
                self.game_engine.snd_wall.play()
        if self.y + self.radius > self.screen_height:
            self.y = self.screen_height - self.radius
            self.vy *= -1
            if hasattr(self, 'game_engine'):
                self.game_engine.snd_wall.play()

        # Clamp max speed to prevent tunneling
        max_speed = 15
        speed = math.hypot(self.vx, self.vy)
        if speed > max_speed:
            scale = max_speed / speed
            self.vx *= scale
            self.vy *= scale

    def check_collision(self, player, ai):
        # Task 1 : Sample along ball path to avoid tunneling
        for paddle in (player, ai):
            rect = paddle.rect()
            dx = self.x - self.prev_x
            dy = self.y - self.prev_y
            dist = max(abs(dx), abs(dy))
            steps = max(int(dist / max(1, self.radius)) * 2, 1)  # doubled for accuracy

            collided = False
            coll_y = self.y

            for i in range(1, steps + 1):
                t = i / steps
                sx = self.prev_x + dx * t
                sy = self.prev_y + dy * t
                if rect.collidepoint(sx, sy):
                    collided = True
                    coll_y = sy
                    break

            if collided:
                # Place ball just outside paddle to prevent sticking
                if self.vx > 0:  # ball moving right
                    self.x = rect.left - self.width
                else:            # ball moving left
                    self.x = rect.right

                # Reflect horizontal velocity and tweak vertical for 'angle'
                self.vx *= -1
                offset = (coll_y - rect.centery) / (rect.height / 2)
                self.vy += offset * 2
                if hasattr(self, 'game_engine'):
                    self.game_engine.snd_paddle.play()
                break

    def reset(self):
        # Reset position
        self.x = self.original_x
        self.y = self.original_y
        self.prev_x = self.x
        self.prev_y = self.y

        # Randomize direction
        self.velocity_x = random.choice([-5, 5])
        self.velocity_y = random.choice([-3, 3])
        self.vx = self.velocity_x
        self.vy = self.velocity_y

    def rect(self):
        # Return pygame.Rect for collision detection
        return pygame.Rect(self.x, self.y, self.width, self.height)
