import pygame
import random
import math
from pygame import mixer

# Initialize Pygame
pygame.init()

# Screen settings
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Load assets
icon = pygame.image.load('ufo.png')
background = pygame.image.load('space.jpg')
background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
guns_img = pygame.image.load('guns.png')
bullet_img = pygame.image.load('bullet.png')
enemy_img = pygame.image.load('alien.png')

# Sounds
mixer.music.load('Background.wav')
mixer.music.play(-1)
bullet_sound = mixer.Sound('Shot.wav')
hit_sound = mixer.Sound('Hit.wav')
game_over_sound = mixer.Sound('Game over.wav')

# Game settings
PLAYER_SPEED = 0.5
BULLET_SPEED = 1.6
ENEMY_SPEED = 0.6
NUM_ENEMIES = 6

# Fonts
font = pygame.font.Font('freesansbold.ttf', 32)
over_font = pygame.font.Font('freesansbold.ttf', 64)

# Set window title and icon
pygame.display.set_caption("Space Invaders")
pygame.display.set_icon(icon)


class Player:
    def __init__(self):
        self.image = guns_img
        self.x = 368
        self.y = 480
        self.x_change = 0

    def move(self):
        self.x += self.x_change
        self.x = max(0, min(self.x, SCREEN_WIDTH - 64))  # Keep player within bounds

    def draw(self):
        screen.blit(self.image, (self.x, self.y))


class Enemy:
    def __init__(self):
        self.image = enemy_img
        self.x = random.randint(0, SCREEN_WIDTH - 64)
        self.y = random.randint(50, 200)
        self.x_change = ENEMY_SPEED
        self.y_change = 50  # Move down on screen when hitting edge

    def move(self):
        self.x += self.x_change
        if self.x <= 0 or self.x >= SCREEN_WIDTH - 64:
            self.x_change *= -1
            self.y += self.y_change  # Move down on screen

    def draw(self):
        screen.blit(self.image, (self.x, self.y))


class Bullet:
    def __init__(self):
        self.image = bullet_img
        self.x = 0
        self.y = 480
        self.y_change = BULLET_SPEED
        self.state = "ready"

    def fire(self, x):
        if self.state == "ready":
            bullet_sound.play()
            self.state = "fire"
            self.x = x

    def move(self):
        if self.state == "fire":
            self.y -= self.y_change
            if self.y < 0:
                self.state = "ready"
                self.y = 480

    def draw(self):
        if self.state == "fire":
            screen.blit(self.image, (self.x + 20, self.y + 10))


class Game:
    def __init__(self):
        self.player = Player()
        self.enemies = [Enemy() for _ in range(NUM_ENEMIES)]
        self.bullet = Bullet()
        self.score = 0
        self.running = True

    def check_collision(self, x1, y1, x2, y2):
        return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2) < 27

    def show_score(self):
        score_text = font.render(f"Score: {self.score}", True, (255, 255, 255))
        screen.blit(score_text, (600, 32))

    def game_over(self):
        over_text = over_font.render("GAME OVER", True, (255, 255, 255))
        screen.blit(over_text, (220, 300))
        mixer.music.stop()
        game_over_sound.play()
        pygame.time.delay(3000)  # Delay before closing game
        self.running = False

    def run(self):
        while self.running:
            screen.fill((155, 100, 55))
            screen.blit(background, (0, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.player.x_change = -PLAYER_SPEED
                    if event.key == pygame.K_RIGHT:
                        self.player.x_change = PLAYER_SPEED
                    if event.key == pygame.K_SPACE:
                        self.bullet.fire(self.player.x)
                if event.type == pygame.KEYUP:
                    if event.key in {pygame.K_LEFT, pygame.K_RIGHT}:
                        self.player.x_change = 0

            self.player.move()
            self.bullet.move()

            for enemy in self.enemies:
                enemy.move()
                if enemy.y > 420:
                    self.game_over()
                    return

                if self.check_collision(enemy.x, enemy.y, self.bullet.x, self.bullet.y) and self.bullet.state == "fire":
                    hit_sound.play()
                    self.bullet.state = "ready"
                    self.bullet.y = 480
                    self.score += 1
                    enemy.x = random.randint(0, SCREEN_WIDTH - 64)
                    enemy.y = random.randint(50, 200)

                enemy.draw()

            self.player.draw()
            self.bullet.draw()
            self.show_score()

            pygame.display.update()


if __name__ == "__main__":
    game = Game()
    game.run()
