import pygame
import sys
import random
import json
import os

# Inicjalizacja PyGame
pygame.init()

# Ustawienia ekranu
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("MultiRun 1.0.0a")

# Kolory
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 100, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
GRAY = (150, 150, 150)

# Czcionki
font_medium = pygame.font.SysFont('Arial', 36)
font_small = pygame.font.SysFont('Arial', 24)

# Ścieżka do pliku zapisu
SAVE_FILE = "game_save.json"

# Domyślne dane gry
default_game_data = {
    "nick": "",
    "current_level": 1,
    "coins": 0,
    "gems": 0,
    "wins": 0,
    "coin_multiplier": 1,
    "gem_multiplier": 1,
    "size_multiplier": 1,
    "speed_multiplier": 1
}

def load_game():
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, 'r') as f:
            try:
                return json.load(f)
            except:
                return default_game_data
    return default_game_data

def save_game():
    game_data = {
        "nick": nick,
        "current_level": current_level,
        "coins": coins,
        "gems": gems,
        "wins": wins,
        "coin_multiplier": coin_multiplier,
        "gem_multiplier": gem_multiplier,
        "size_multiplier": size_multiplier,
        "speed_multiplier": speed_multiplier
    }
    with open(SAVE_FILE, 'w') as f:
        json.dump(game_data, f)

# Inicjalizacja danych gry
game_data = load_game()
nick = game_data["nick"]
current_level = game_data["current_level"]
coins = game_data["coins"]
gems = game_data["gems"]
wins = game_data["wins"]
coin_multiplier = game_data["coin_multiplier"]
gem_multiplier = game_data["gem_multiplier"]
size_multiplier = game_data["size_multiplier"]
speed_multiplier = game_data["speed_multiplier"]

# Gracz
base_player_size = 40
player_x = 100
player_y = HEIGHT - base_player_size - 50
player_speed = 5
player_rect = pygame.Rect(player_x, player_y, base_player_size * size_multiplier, base_player_size * size_multiplier)

def setup_level(level):
    global enemies, goal, player_rect, goal_speed
    
    # Podłoga
    floor = pygame.Rect(0, HEIGHT - 50, WIDTH, 50)
    
    # Wrogowie
    enemies = []
    for i in range(level * 2):
        enemy_size = random.randint(20, 40)
        enemies.append({
            "rect": pygame.Rect(
                random.randint(0, WIDTH - enemy_size),
                random.randint(0, HEIGHT - enemy_size - 50),
                enemy_size, enemy_size
            ),
            "speed_x": random.choice([-3, -2, -1, 1, 2, 3]),
            "speed_y": random.choice([-3, -2, -1, 1, 2, 3])
        })
    
    # Cel w losowym miejscu (zależnym od poziomu)
    goal_size = 40
    goal_x = random.randint(100, WIDTH - 100)
    goal_y = random.randint(100, HEIGHT - 150)
    goal = pygame.Rect(goal_x, goal_y, goal_size, goal_size)
    
    # Prędkość celu zależna od poziomu i mnożnika
    base_speed = 1 + (level / 5)
    goal_speed = [
        random.choice([-base_speed, base_speed]) * speed_multiplier,
        random.choice([-base_speed, base_speed]) * speed_multiplier
    ]
    
    player_rect.x = 100
    player_rect.y = HEIGHT - player_rect.height - 50
    player_rect.width = base_player_size * size_multiplier
    player_rect.height = base_player_size * size_multiplier

def draw_nick_input():
    screen.fill(WHITE)
    title = font_medium.render("Wprowadź swój nick", True, BLACK)
    screen.blit(title, (WIDTH//2 - title.get_width()//2, 100))
    
    input_rect = pygame.Rect(WIDTH//2 - 200, 200, 400, 50)
    pygame.draw.rect(screen, BLACK, input_rect, 2)
    
    nick_surface = font_medium.render(nick, True, BLACK)
    screen.blit(nick_surface, (input_rect.x + 10, input_rect.y + 10))
    
    continue_rect = pygame.Rect(WIDTH//2 - 100, 300, 200, 50)
    pygame.draw.rect(screen, BLUE, continue_rect)
    continue_text = font_medium.render("Kontynuuj", True, WHITE)
    screen.blit(continue_text, (continue_rect.centerx - continue_text.get_width()//2, 
                              continue_rect.centery - continue_text.get_height()//2))
    
    return input_rect, continue_rect

def draw_main_menu():
    screen.fill(WHITE)
    
    stats = [
        f"Wygrany: {wins}",
        f"Monety: {coins} (x{coin_multiplier})",
        f"Gemy: {gems} (x{gem_multiplier})",
        f"Poziom: {current_level}",
        f"Rozmiar: x{size_multiplier:.1f}",
        f"Prędkość celu: x{speed_multiplier:.1f}"
    ]
    
    for i, stat in enumerate(stats):
        stat_text = font_small.render(stat, True, BLACK)
        screen.blit(stat_text, (20, 20 + i * 25))
    
    nick_text = font_medium.render(nick, True, BLACK)
    screen.blit(nick_text, (WIDTH//2 - nick_text.get_width()//2, 100))
    
    play_rect = pygame.Rect(WIDTH - 220, HEIGHT - 80, 200, 50)
    pygame.draw.rect(screen, BLUE, play_rect)
    play_text = font_medium.render("Graj", True, WHITE)
    screen.blit(play_text, (play_rect.centerx - play_text.get_width()//2, 
                           play_rect.centery - play_text.get_height()//2))
    
    upgrade_rect = pygame.Rect(WIDTH - 220, HEIGHT - 150, 200, 50)
    pygame.draw.rect(screen, GREEN, upgrade_rect)
    upgrade_text = font_medium.render("Ulepszenia", True, WHITE)
    screen.blit(upgrade_text, (upgrade_rect.centerx - upgrade_text.get_width()//2, 
                              upgrade_rect.centery - upgrade_text.get_height()//2))
    
    return play_rect, upgrade_rect

def draw_upgrade_menu():
    screen.fill(WHITE)
    
    title = font_medium.render("Ulepszenia", True, BLACK)
    screen.blit(title, (WIDTH//2 - title.get_width()//2, 50))
    
    # Ulepszenie monet
    coin_upgrade_cost = 100 * coin_multiplier
    coin_upgrade_rect = pygame.Rect(100, 120, 250, 50)
    pygame.draw.rect(screen, YELLOW if coins >= coin_upgrade_cost else GRAY, coin_upgrade_rect)
    coin_text = font_small.render(f"Monety x{coin_multiplier}->x{coin_multiplier+1}", True, BLACK)
    cost_text = font_small.render(f"Koszt: {coin_upgrade_cost} monet", True, BLACK)
    screen.blit(coin_text, (coin_upgrade_rect.x + 10, coin_upgrade_rect.y + 5))
    screen.blit(cost_text, (coin_upgrade_rect.x + 10, coin_upgrade_rect.y + 25))
    
    # Ulepszenie gemów
    gem_upgrade_cost = 15 * gem_multiplier
    gem_upgrade_rect = pygame.Rect(100, 190, 250, 50)
    pygame.draw.rect(screen, YELLOW if gems >= gem_upgrade_cost else GRAY, gem_upgrade_rect)
    gem_text = font_small.render(f"Gemy x{gem_multiplier}->x{gem_multiplier+1}", True, BLACK)
    cost_text = font_small.render(f"Koszt: {gem_upgrade_cost} gemów", True, BLACK)
    screen.blit(gem_text, (gem_upgrade_rect.x + 10, gem_upgrade_rect.y + 5))
    screen.blit(cost_text, (gem_upgrade_rect.x + 10, gem_upgrade_rect.y + 25))
    
    # Mniejszy gracz
    size_upgrade_cost = 50 * size_multiplier
    size_upgrade_rect = pygame.Rect(100, 260, 250, 50)
    pygame.draw.rect(screen, BLUE if coins >= size_upgrade_cost else GRAY, size_upgrade_rect)
    size_text = font_small.render(f"Rozmiar x{size_multiplier:.1f}->x{size_multiplier-0.1:.1f}", True, BLACK)
    cost_text = font_small.render(f"Koszt: {size_upgrade_cost} monet", True, BLACK)
    screen.blit(size_text, (size_upgrade_rect.x + 10, size_upgrade_rect.y + 5))
    screen.blit(cost_text, (size_upgrade_rect.x + 10, size_upgrade_rect.y + 25))
    
    # Szybszy cel
    speed_upgrade_cost = 30 * speed_multiplier
    speed_upgrade_rect = pygame.Rect(100, 330, 250, 50)
    pygame.draw.rect(screen, RED if gems >= speed_upgrade_cost else GRAY, speed_upgrade_rect)
    speed_text = font_small.render(f"Prędkość celu x{speed_multiplier:.1f}->x{speed_multiplier+0.1:.1f}", True, BLACK)
    cost_text = font_small.render(f"Koszt: {speed_upgrade_cost} gemów", True, BLACK)
    screen.blit(speed_text, (speed_upgrade_rect.x + 10, speed_upgrade_rect.y + 5))
    screen.blit(cost_text, (speed_upgrade_rect.x + 10, speed_upgrade_rect.y + 25))
    
    # Powrót
    back_rect = pygame.Rect(WIDTH - 220, HEIGHT - 80, 200, 50)
    pygame.draw.rect(screen, BLUE, back_rect)
    back_text = font_medium.render("Powrót", True, WHITE)
    screen.blit(back_text, (back_rect.centerx - back_text.get_width()//2, 
                           back_rect.centery - back_text.get_height()//2))
    
    return coin_upgrade_rect, gem_upgrade_rect, size_upgrade_rect, speed_upgrade_rect, back_rect

def draw_game():
    screen.fill(WHITE)
    
    # Podłoga
    pygame.draw.rect(screen, GREEN, (0, HEIGHT - 50, WIDTH, 50))
    
    # Wrogowie
    for enemy in enemies:
        pygame.draw.rect(screen, RED, enemy["rect"])
    
    # Cel
    pygame.draw.rect(screen, YELLOW, goal)
    
    # Gracz
    pygame.draw.rect(screen, BLUE, player_rect)
    
    # Informacje
    level_text = font_small.render(f"Poziom: {current_level}", True, BLACK)
    screen.blit(level_text, (20, 20))
    
    controls_text = font_small.render("Sterowanie: W/S/A/D", True, BLACK)
    screen.blit(controls_text, (20, 50))
    
    stats_text = font_small.render(f"Monety: {coins} | Gemy: {gems}", True, BLACK)
    screen.blit(stats_text, (20, 80))

def move_entities():
    # Poruszanie wrogów
    for enemy in enemies:
        enemy["rect"].x += enemy["speed_x"]
        enemy["rect"].y += enemy["speed_y"]
        
        if enemy["rect"].left <= 0 or enemy["rect"].right >= WIDTH:
            enemy["speed_x"] *= -1
        if enemy["rect"].top <= 0 or enemy["rect"].bottom >= HEIGHT - 50:
            enemy["speed_y"] *= -1
        
        enemy["rect"].x = max(0, min(WIDTH - enemy["rect"].width, enemy["rect"].x))
        enemy["rect"].y = max(0, min(HEIGHT - enemy["rect"].height - 50, enemy["rect"].y))
    
    # Poruszanie celu
    global goal_speed
    goal.x += goal_speed[0]
    goal.y += goal_speed[1]
    
    if goal.left <= 0 or goal.right >= WIDTH:
        goal_speed[0] *= -1
    if goal.top <= 0 or goal.bottom >= HEIGHT - 50:
        goal_speed[1] *= -1

# Inicjalizacja poziomu
setup_level(current_level)

# Główna pętla gry
running = True
clock = pygame.time.Clock()
game_state = "nick_input" if nick == "" else "main_menu"
upgrade_menu = False

while running:
    clock.tick(60)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            save_game()
            running = False
        
        if game_state == "nick_input":
            input_rect, continue_rect = draw_nick_input()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_rect.collidepoint(event.pos):
                    active_input = True
                else:
                    active_input = False
                    
                if continue_rect.collidepoint(event.pos) and nick:
                    game_state = "main_menu"
                    save_game()
            
            if event.type == pygame.KEYDOWN:
                if active_input:
                    if event.key == pygame.K_BACKSPACE:
                        nick = nick[:-1]
                    elif event.key == pygame.K_RETURN:
                        if nick:
                            game_state = "main_menu"
                            save_game()
                    else:
                        if len(nick) < 15:
                            nick += event.unicode
        
        elif game_state == "main_menu" and not upgrade_menu:
            play_rect, upgrade_rect = draw_main_menu()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_rect.collidepoint(event.pos):
                    game_state = "game"
                    setup_level(current_level)
                elif upgrade_rect.collidepoint(event.pos):
                    upgrade_menu = True
        
        elif upgrade_menu:
            coin_rect, gem_rect, size_rect, speed_rect, back_rect = draw_upgrade_menu()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_rect.collidepoint(event.pos):
                    upgrade_menu = False
                elif coin_rect.collidepoint(event.pos) and coins >= 100 * coin_multiplier:
                    coins -= 100 * coin_multiplier
                    coin_multiplier += 1
                    save_game()
                elif gem_rect.collidepoint(event.pos) and gems >= 15 * gem_multiplier:
                    gems -= 15 * gem_multiplier
                    gem_multiplier += 1
                    save_game()
                elif size_rect.collidepoint(event.pos) and coins >= 50 * size_multiplier and size_multiplier > 0.5:
                    coins -= 50 * size_multiplier
                    size_multiplier -= 0.1
                    player_rect.width = base_player_size * size_multiplier
                    player_rect.height = base_player_size * size_multiplier
                    save_game()
                elif speed_rect.collidepoint(event.pos) and gems >= 30 * speed_multiplier:
                    gems -= 30 * speed_multiplier
                    speed_multiplier += 0.1
                    save_game()
        
        elif game_state == "game":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_state = "main_menu"
                    save_game()

    if game_state == "nick_input":
        draw_nick_input()
    
    elif game_state == "main_menu":
        if upgrade_menu:
            draw_upgrade_menu()
        else:
            draw_main_menu()
    
    elif game_state == "game":
        # Poruszanie graczem
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and player_rect.left > 0:
            player_rect.x -= player_speed
        if keys[pygame.K_d] and player_rect.right < WIDTH:
            player_rect.x += player_speed
        if keys[pygame.K_w] and player_rect.top > 0:
            player_rect.y -= player_speed
        if keys[pygame.K_s] and player_rect.bottom < HEIGHT:
            player_rect.y += player_speed
        
        if player_rect.bottom > HEIGHT - 50:
            player_rect.bottom = HEIGHT - 50
        
        move_entities()
        
        # Kolizje z wrogami
        for enemy in enemies[:]:
            if player_rect.colliderect(enemy["rect"]):
                game_state = "main_menu"
                save_game()
        
        # Kolizja z celem
        if player_rect.colliderect(goal):
            wins += 1
            coins += 250 * current_level * coin_multiplier
            gems += 15 * current_level * gem_multiplier
            current_level += 1
            game_state = "main_menu"
            save_game()
            setup_level(current_level)
        
        draw_game()
    
    pygame.display.flip()

pygame.quit()
sys.exit()