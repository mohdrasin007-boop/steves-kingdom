import pygame
import random
import sys

pygame.init()

# Window setup
WIDTH, HEIGHT = 800, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Steve's Kingdom For Men")

# Colors
WHITE = (255, 255, 255)
SKY = (180, 220, 255)
STEVE_COLOR = (0, 100, 220)
WOMAN_COLORS = [(255, 100, 150), (255, 160, 200), (255, 120, 170)]
TEXT_COLOR = (0, 0, 0)

# Fonts
FONT = pygame.font.SysFont("comicsansms", 30)

# Character setup
steve = pygame.Rect(100, HEIGHT - 150, 60, 100)

women = [
    pygame.Rect(500 + i * 80, HEIGHT - 150, 50, 90)
    for i in range(3)
]
active_woman_index = 0  # move the first woman with keys

# State
jumping = False
jump_vel = 0
message = ""
message_timer = 0

clock = pygame.time.Clock()

def draw_window():
    WIN.fill(SKY)
    
    # Draw Steve
    pygame.draw.rect(WIN, STEVE_COLOR, steve)
    name_text = FONT.render("Steve", True, TEXT_COLOR)
    WIN.blit(name_text, (steve.x, steve.y - 30))

    # Draw women
    for i, woman in enumerate(women):
        pygame.draw.rect(WIN, WOMAN_COLORS[i % len(WOMAN_COLORS)], woman)
        w_text = FONT.render(f"W{i+1}", True, TEXT_COLOR)
        WIN.blit(w_text, (woman.x, woman.y - 30))
    
    # Draw message if any
    if message:
        msg_surface = FONT.render(message, True, TEXT_COLOR)
        WIN.blit(msg_surface, (steve.centerx - msg_surface.get_width()//2, steve.y - 70))
    
    pygame.display.update()

def reset_steve():
    steve.bottom = HEIGHT - 50

def trigger_reaction():
    global jumping, jump_vel, message, message_timer
    jumping = True
    jump_vel = -15
    message = random.choice(["Hey!", "Back off!", "I'm Steve!", "Respect the King!"])
    message_timer = pygame.time.get_ticks()

def main():
    global jumping, jump_vel, message, message_timer

    running = True
    reset_steve()
    
    while running:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Move active woman with keys
        keys = pygame.key.get_pressed()
        woman = women[active_woman_index]
        speed = 5
        if keys[pygame.K_LEFT]:
            woman.x -= speed
        if keys[pygame.K_RIGHT]:
            woman.x += speed
        if keys[pygame.K_UP]:
            woman.y -= speed
        if keys[pygame.K_DOWN]:
            woman.y += speed

        # Check collision with Steve
        if steve.colliderect(woman):
            if not jumping:
                trigger_reaction()

        # Handle jumping animation
        if jumping:
            steve.y += jump_vel
            jump_vel += 1  # gravity
            if steve.bottom >= HEIGHT - 50:
                reset_steve()
                jumping = False

        # Clear message after 1.5 seconds
        if message and pygame.time.get_ticks() - message_timer > 1500:
            message = ""

        draw_window()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
