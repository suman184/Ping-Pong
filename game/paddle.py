import pygame

class Paddle:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = 7

    def move(self, dy, screen_height):
        self.y += dy
        self.y = max(0, min(self.y, screen_height - self.height))

    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def auto_track(self, ball, screen_height):
        if ball.y < self.y:
            self.move(-self.speed, screen_height)
        elif ball.y > self.y + self.height:
            self.move(self.speed, screen_height)


# import pygame

# class Paddle:
#     def __init__(self, x, y, width, height):
#         self.x = x
#         self.y = y
#         self.width = width
#         self.height = height
#         self.speed = 7

#     def move(self, dy, screen_height):
#         self.y += dy

#         # 🔁 Wrap-around effect
#         if self.y > screen_height:
#             self.y = -self.height
#         elif self.y + self.height < 0:
#             self.y = screen_height

#     def rect(self):
#         return pygame.Rect(self.x, self.y, self.width, self.height)

#     def auto_track(self, ball, screen_height):
#         # 🧠 AI moves up/down towards the ball
#         if ball.y < self.y:
#             self.move(-self.speed, screen_height)
#         elif ball.y > self.y + self.height:
#             self.move(self.speed, screen_height)
