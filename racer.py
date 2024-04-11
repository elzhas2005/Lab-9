import pygame
import sys
import random
import time
from pygame.locals import *

pygame.init()

FPS = 60
FramePerSec = pygame.time.Clock()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
SPEED = 5
SCORE = 0
COIN_COUNT = 0
ENEMY_SPEED = 5  # Изначальная скорость врага
COIN_THRESHOLD = 20  # Пороговое значение для увеличения скорости врага

font_small = pygame.font.SysFont("Verdana", 20)
game_over = pygame.font.SysFont("Verdana", 60).render("Game Over", True, BLACK)

DISPLAYSURF = pygame.display.set_mode((400, 600))
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("Game")

background = pygame.image.load(r"C:\Users\user\Desktop\Lab-8\pngwing.com (1).png")
pygame.mixer.music.load(r"C:\Users\user\Desktop\Lab-8\shiloh-dynasty-hesitations.mp3")
pygame.mixer.music.play(-1)

player = pygame.image.load(r"C:\Users\user\Desktop\Lab-8\blue.png")
enemy = pygame.image.load(r"C:\Users\user\Desktop\Lab-8\yellow.png")
coin = pygame.image.load(r"C:\Users\user\Desktop\Lab-8\pngwing.com.png")
coin = pygame.transform.scale(coin, (40, 40))

player_rect = player.get_rect(center=(160, 520))
enemy_rect = enemy.get_rect(center=(random.randint(40, SCREEN_WIDTH - 40), 0))
coin_rect = coin.get_rect()
coin_rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    pressed_keys = pygame.key.get_pressed()

    if pressed_keys[pygame.K_UP]:
        player_rect.centery -= SPEED

    if pressed_keys[pygame.K_DOWN]:
        player_rect.centery += SPEED

    if pressed_keys[pygame.K_LEFT]:
        player_rect.centerx -= SPEED

    if pressed_keys[pygame.K_RIGHT]:
        player_rect.centerx += SPEED

    DISPLAYSURF.blit(background, (0, 0))
    scores = font_small.render(f"SCORE: {SCORE}", True, BLACK)
    coins = font_small.render(f"COINS: {COIN_COUNT}", True, BLACK)
    DISPLAYSURF.blit(scores, (10, 10))
    DISPLAYSURF.blit(coins, (310, 10))

    DISPLAYSURF.blit(player, player_rect)
    DISPLAYSURF.blit(enemy, enemy_rect)
    DISPLAYSURF.blit(coin, coin_rect)

    enemy_rect.centery += ENEMY_SPEED
    coin_rect.centery += SPEED

    if enemy_rect.top > SCREEN_HEIGHT:
        enemy_rect.top = 0
        enemy_rect.centerx = random.randint(40, SCREEN_WIDTH - 40)
        SCORE += 1

        # Проверяем, превышено ли пороговое значение монет
        if COIN_COUNT >= COIN_THRESHOLD:
            # Увеличиваем скорость врага
            ENEMY_SPEED += 1
            # Сбрасываем счетчик монет
            COIN_COUNT = 0

    if coin_rect.colliderect(player_rect):
        COIN_COUNT += random.randint(1, 3)  # Генерируем случайное количество монет
        coin_rect.top = 0
        coin_rect.centerx = random.randint(40, SCREEN_WIDTH - 40)

    if coin_rect.top > SCREEN_HEIGHT:
        coin_rect.top = 0
        coin_rect.centerx = random.randint(40, SCREEN_WIDTH - 40)

    if player_rect.colliderect(enemy_rect):
        time.sleep(0.5)
        DISPLAYSURF.fill(BLACK)
        DISPLAYSURF.blit(game_over, (30, 250))
        coin_text = font_small.render(f"COINS: {COIN_COUNT}", True, WHITE)
        DISPLAYSURF.blit(coin_text, (150, 350))
        pygame.display.update()
        time.sleep(2)

        SCORE = 0
        player_rect.center = (160, 520)
        enemy_rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)
        COIN_COUNT = 0

    pygame.display.update()
    FramePerSec.tick(FPS)
