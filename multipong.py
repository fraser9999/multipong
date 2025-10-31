# Multipong Game
# Hermann knopp 2025
# Multi Ball Pong
# 31.10.2025 (Early Alpha 0.1a Version)
 


import os
os.system("cls")

print("importing libs...")



import pygame
import random
import time

# ====== EINSTELLUNGEN ======
WIDTH, HEIGHT = 800, 600
PADDLE_WIDTH, PADDLE_HEIGHT = 100, 10
BALL_RADIUS = 10
TIMER_INTERVAL = 10  # Sekunden bis neuer Ball
BALL_SPEED = 3
PADDLE_SPEED = 10
MAX_BALL_SPEED_X = 5  # maximale X-Geschwindigkeit nach Abprall
PREP_TIME = 5  # Sekunden Vorbereitung vor Ballbewegung

# Highscore-Datei im selben Verzeichnis wie das Skript
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
HIGHSCORE_FILE = os.path.join(SCRIPT_DIR, "highscore.txt")

# ====== HIGH SCORE LADEN ======
if os.path.exists(HIGHSCORE_FILE):
    with open(HIGHSCORE_FILE, "r") as f:
        highscore = int(f.read().strip())
else:
    highscore = 0


# ======= System Message ========

print("")
print("")
print("Multi Ball Pong Game")
print("")
print("use: Arrow Keys to Play.")
print("")
print("click on Pygame Window for Focus")
print("")
a=input("Wait Return Key")






# ====== SPIELINITIALISIERUNG ======
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("MultiPong: play with Arrow Keys")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)
large_font = pygame.font.SysFont(None, 72)

# ====== HELFER ======
def add_ball():
    balls.append({
        "x": random.randint(BALL_RADIUS, WIDTH-BALL_RADIUS),
        "y": 50,
        "dx": random.choice([-BALL_SPEED, BALL_SPEED]),
        "dy": BALL_SPEED
    })

def reset_game():
    global paddle, balls, score, timer, last_timer_tick, game_over, prep_start_time, prep_phase
    paddle = pygame.Rect(WIDTH//2 - PADDLE_WIDTH//2, HEIGHT-30, PADDLE_WIDTH, PADDLE_HEIGHT)
    balls = [{"x": WIDTH//2, "y": 50, "dx": BALL_SPEED, "dy": BALL_SPEED}]
    score = 0
    timer = TIMER_INTERVAL
    last_timer_tick = pygame.time.get_ticks()
    game_over = False
    prep_phase = True
    prep_start_time = time.time()

def draw():
    screen.fill((0, 0, 0))
    
    # Paddle
    pygame.draw.rect(screen, (255, 255, 255), paddle)
    
    # Balls
    for ball in balls:
        pygame.draw.circle(screen, (255, 0, 0), (int(ball["x"]), int(ball["y"])), BALL_RADIUS)
    
    # Anzeige
    score_text = font.render(f"Points: {score}  Highscore: {highscore}  Timer: {timer}", True, (255, 255, 255))
    screen.blit(score_text, (20, 20))
    
    # Game Over Anzeige
    if game_over:
        over_text = font.render("GAME OVER! Press SPACE to Restart", True, (255, 0, 0))
        screen.blit(over_text, (WIDTH//2 - over_text.get_width()//2, HEIGHT//2 - 20))
    
    # Vorbereitungsphase Countdown
    if prep_phase:
        remaining = max(0, PREP_TIME - int(time.time() - prep_start_time))
        countdown_text = large_font.render(f"Start in {remaining}", True, (0, 255, 0))
        screen.blit(countdown_text, (WIDTH//2 - countdown_text.get_width()//2, HEIGHT//2 - 50))
    
    pygame.display.flip()

# ====== SPIELSTART ======
reset_game()
running = True

while running:
    dt = clock.tick(60)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    keys = pygame.key.get_pressed()
    
    if not game_over:
        # Paddle-Steuerung mit Pfeiltasten
        if keys[pygame.K_LEFT] and paddle.left > 0:
            paddle.x -= PADDLE_SPEED
        if keys[pygame.K_RIGHT] and paddle.right < WIDTH:
            paddle.x += PADDLE_SPEED
        
        # Vorbereitungsphase
        if prep_phase:
            if time.time() - prep_start_time >= PREP_TIME:
                prep_phase = False  # Ballbewegung starten
        else:
            # Timer aktualisieren
            current_ticks = pygame.time.get_ticks()
            if current_ticks - last_timer_tick >= 1000:
                timer -= 1
                last_timer_tick = current_ticks
                if timer <= 0:
                    add_ball()
                    timer = TIMER_INTERVAL
            
            # Balls bewegen
            for ball in balls:
                ball["x"] += ball["dx"]
                ball["y"] += ball["dy"]
                
                # Wände
                if ball["x"] <= BALL_RADIUS or ball["x"] >= WIDTH-BALL_RADIUS:
                    ball["dx"] *= -1
                if ball["y"] <= BALL_RADIUS:
                    ball["dy"] *= -1
                
                # Paddle mit Winkel abhängig vom Treffpunkt
                if paddle.top <= ball["y"] + BALL_RADIUS <= paddle.bottom and paddle.left <= ball["x"] <= paddle.right:
                    paddle_center = paddle.left + PADDLE_WIDTH / 2
                    hit_pos = (ball["x"] - paddle_center) / (PADDLE_WIDTH / 2)  # -1 ... 1
                    ball["dx"] = hit_pos * MAX_BALL_SPEED_X
                    ball["dy"] = -abs(ball["dy"])
                    score += 1
                
                # Unteres Ende -> Game Over
                if ball["y"] >= HEIGHT:
                    game_over = True
                    # Highscore speichern
                    if score > highscore:
                        highscore = score
                        with open(HIGHSCORE_FILE, "w") as f:
                            f.write(str(highscore))
    else:
        # Neustart mit Space
        if keys[pygame.K_SPACE]:
            reset_game()
    
    draw()

pygame.quit()
