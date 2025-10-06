# import pygame
# from .paddle import Paddle
# from .ball import Ball

# # Game Engine

# WHITE = (255, 255, 255)

# class GameEngine:
#     def __init__(self, width, height,score_limit=1):
#         self.width = width
#         self.height = height
#         self.paddle_width = 10
#         self.paddle_height = 100

#         self.player = Paddle(10, height // 2 - 50, self.paddle_width, self.paddle_height)
#         self.ai = Paddle(width - 20, height // 2 - 50, self.paddle_width, self.paddle_height)
#         self.ball = Ball(width // 2, height // 2, 7, 7, width, height)

#         self.player_score = 0
#         self.ai_score = 0
#         self.font = pygame.font.SysFont("Arial", 30)
        
#         self.score_limit = score_limit
#         self.game_over = False


#     def handle_input(self):
#         keys = pygame.key.get_pressed()
#         if keys[pygame.K_w]:
#             self.player.move(-10, self.height)
#         if keys[pygame.K_s]:
#             self.player.move(10, self.height)

#     def update(self):
#         self.ball.move()
#         self.ball.check_collision(self.player, self.ai)

#         if self.ball.x <= 0:
#             self.ai_score += 1
#             self.ball.reset()
#         elif self.ball.x >= self.width:
#             self.player_score += 1
#             self.ball.reset()

#         self.ai.auto_track(self.ball, self.height)

#     def render(self, screen):
#         # Draw paddles and ball
#         pygame.draw.rect(screen, WHITE, self.player.rect())
#         pygame.draw.rect(screen, WHITE, self.ai.rect())
#         pygame.draw.ellipse(screen, WHITE, self.ball.rect())
#         pygame.draw.aaline(screen, WHITE, (self.width//2, 0), (self.width//2, self.height))

#         # Draw score
#         player_text = self.font.render(str(self.player_score), True, WHITE)
#         ai_text = self.font.render(str(self.ai_score), True, WHITE)
#         screen.blit(player_text, (self.width//4, 20))
#         screen.blit(ai_text, (self.width * 3//4, 20))
        
#         if(self.ai_score >= 1 or self.player_score >= 1):
#             end_text = self.font.render("Game Over", True, WHITE)
#             screen.blit(end_text, (self.width//2 - end_text.get_width()//2, self.height//2 - end_text.get_height()//2))
#             end_text2 = self.font.render("Press R to Restart", True, WHITE)
#             screen.blit(end_text2, (self.width//2 - end_text2.get_width()//2, self.height//2 + end_text.get_height()))
            
import pygame
from .paddle import Paddle
from .ball import Ball

# ...existing code...

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

class GameEngine:
    def __init__(self, width, height, score_limit=1):
        self.width = width
        self.height = height
        self.paddle_width = 10
        self.paddle_height = 100
        self.paused = False #Task 3 : pause functionality
        #Task 4 : suound effects
        pygame.mixer.init()

        self.snd_paddle = pygame.mixer.Sound("sounds/paddle_hit.wav")
        self.snd_wall   = pygame.mixer.Sound("sounds/wall_bounce.wav")
        self.snd_score  = pygame.mixer.Sound("sounds/score.wav")

        # initial positions
        self.player_start_x = 10
        self.player_start_y = height // 2 - self.paddle_height // 2
        self.ai_start_x = width - 20
        self.ai_start_y = height // 2 - self.paddle_height // 2

        self.player = Paddle(self.player_start_x, self.player_start_y, self.paddle_width, self.paddle_height)
        self.ai = Paddle(self.ai_start_x, self.ai_start_y, self.paddle_width, self.paddle_height)
        self.ball = Ball(width // 2, height // 2, 7, 7, width, height)
        
        self.ball.game_engine = self  #Task 4 component Link back for sound effects
        
        self.player_score = 0
        self.ai_score = 0
        self.font = pygame.font.SysFont("Arial", 30)

        self.score_limit = score_limit
        self.game_over = False
        self.winner = None

    def handle_input(self):
        if self.game_over:
            return
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.player.move(-10, self.height)
        if keys[pygame.K_s]:
            self.player.move(10, self.height)

    def handle_event(self, event):
        # call this from your main loop for one-shot keys (restart, quit, etc.)
        if event.type == pygame.KEYDOWN:
            # Restart only when game over
            if event.key == pygame.K_p and not self.game_over:
                self.paused = not self.paused
            if event.key == pygame.K_r and self.game_over:
                self.reset_game()

            if self.game_over:
            # Choose new match length
                if event.key == pygame.K_3:
                    self.score_limit = 3
                    self.reset_game()
                elif event.key == pygame.K_5:
                    self.score_limit = 5
                    self.reset_game()
                elif event.key == pygame.K_7:
                    self.score_limit = 7
                    self.reset_game()
                elif event.key == pygame.K_q:
                    pygame.quit()
                    raise SystemExit()
            else:
                # In-game keys
                if event.key == pygame.K_r:
                    self.reset_game()
                elif event.key == pygame.K_q:
                    pygame.quit()
                    raise SystemExit()

    def update(self):
        if self.ball.x <= 0:
            self.ai_score += 1
            self.snd_score.play()
            self.ball.reset()
        elif self.ball.x >= self.width:
            self.player_score += 1
            self.snd_score.play()
            self.ball.reset()
            
        if self.game_over or self.paused:
            return

        self.ball.move()
        self.ball.check_collision(self.player, self.ai)

        if self.ball.x <= 0:
            self.ai_score += 1
            self.ball.reset()
        elif self.ball.x >= self.width:
            self.player_score += 1
            self.ball.reset()

        self.ai.auto_track(self.ball, self.height)

        # Check for end condition and record winner
        if self.player_score >= self.score_limit:
            self.game_over = True
            self.winner = "Suman"
        elif self.ai_score >= self.score_limit:
            self.game_over = True
            self.winner = "AI"

    def render(self, screen):
        
        # Draw paddles and ball
        pygame.draw.rect(screen, WHITE, self.player.rect())
        pygame.draw.rect(screen, WHITE, self.ai.rect())
        pygame.draw.ellipse(screen, WHITE, self.ball.rect())
        pygame.draw.aaline(screen, WHITE, (self.width//2, 0), (self.width//2, self.height))

        # Draw score
        player_text = self.font.render(str(self.player_score), True, WHITE)
        ai_text = self.font.render(str(self.ai_score), True, WHITE)
        screen.blit(player_text, (self.width//4, 20))
        screen.blit(ai_text, (self.width * 3//4, 20))
        
        # Game over overlay with winner and instructions
        if self.game_over:
            overlay = pygame.Surface((self.width, self.height))
            overlay.set_alpha(180)
            overlay.fill(BLACK)
            screen.blit(overlay, (0, 0))

            title_font = pygame.font.SysFont("Arial", 48, bold=True)
            small_font = pygame.font.SysFont("Arial", 24)

            winner_text = f"{self.winner} Wins!"
            winner_surf = title_font.render(winner_text, True, WHITE)
            winner_rect = winner_surf.get_rect(center=(self.width // 2, self.height // 2 - 30))
            screen.blit(winner_surf, winner_rect)

            score_text = f"Final Score — Suman: {self.player_score}  |  AI: {self.ai_score}"
            score_surf = self.font.render(score_text, True, WHITE)
            score_rect = score_surf.get_rect(center=(self.width // 2, self.height // 2 + 10))
            screen.blit(score_surf, score_rect)

            instr_surf = small_font.render("Press R to Restart or Q to Quit", True, WHITE)
            instr_rect = instr_surf.get_rect(center=(self.width // 2, self.height // 2 + 60))
            screen.blit(instr_surf, instr_rect)
            
            small_font = pygame.font.SysFont("Arial", 24)
            instr_text = "Press 3 / 5 / 7 for Best of 3, 5, 7 or Q to Quit"
            instr_surf = small_font.render(instr_text, True, (255, 255, 255))
            screen.blit(instr_surf, instr_surf.get_rect(center=(self.width//2, self.height//2 + 90)))

        if self.paused and not self.game_over:
            overlay = pygame.Surface((self.width, self.height))
            overlay.set_alpha(150)
            overlay.fill((0, 0, 0))
            screen.blit(overlay, (0, 0))
            pause_font = pygame.font.SysFont("Arial", 48, bold=True)
            pause_text = pause_font.render("PAUSED", True, (255, 255, 255))
            screen.blit(
                pause_text,
                pause_text.get_rect(center=(self.width//2, self.height//2 - 20))
            )
        if self.paused :
            small_font = pygame.font.SysFont("Arial", 24)
            instr = small_font.render("Press P to Resume", True, (255, 255, 255))
            screen.blit(instr, instr.get_rect(center=(self.width//2, self.height//2 + 30)))
    
    def reset_game(self):
        # reset scores and positions
        self.player_score = 0
        self.ai_score = 0
        self.game_over = False
        self.winner = None

        # reset ball and paddles to their starting positions
        self.ball.reset()
        self.player.x = self.player_start_x
        self.player.y = self.player_start_y
        self.ai.x = self.ai_start_x
        self.ai.y = self.ai_start_y

# ...existing code...