import pygame
import sys

# ---------- BASIC SETUP ----------
pygame.init()
WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Steve's Kingdom For Men")

clock = pygame.time.Clock()
FONT = pygame.font.SysFont("arial", 28, bold=True)

# ---------- COLORS ----------
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
STEVE_COLOR = (50, 150, 255)
WOMAN_COLOR = (255, 100, 150)
TEXT_BG = (255, 255, 0)

# ---------- STEVE (MALE) ----------
steve_width, steve_height = 80, 140
steve_x = 80
steve_y_ground = HEIGHT - steve_height - 50
steve_y = steve_y_ground
steve_rect = pygame.Rect(steve_x, steve_y, steve_width, steve_height)

# Jump / arrogance animation
is_jumping = False
jump_velocity = 0
JUMP_STRENGTH = -18
GRAVITY = 1

# ---------- WOMEN ----------
woman_width, woman_height = 60, 120
women = []

# Create 3 women on the right side
start_x = WIDTH - 200
for i in range(3):
    rect = pygame.Rect(start_x + i * 70, HEIGHT - woman_height - 50, woman_width, woman_height)
    women.append(rect)

selected_woman = None
offset_x = 0
offset_y = 0

# ---------- REACTION TEXT ----------
reaction_active = False
reaction_timer = 0
REACTION_DURATION = 60  # frames
reaction_texts = [
    "Stay back!",
    "Know your place!",
    "Steve is above this!",
    "How dare you approach!",
]
current_reaction = ""

def trigger_reaction():
    global reaction_active, reaction_timer, current_reaction, is_jumping, jump_velocity
    import random
    current_reaction = random.choice(reaction_texts)
    reaction_active = True
    reaction_timer = REACTION_DURATION

    # Start jump
    if not is_jumping:
        is_jumping = True
        jump_velocity = JUMP_STRENGTH

def handle_jump():
    global steve_y, is_jumping, jump_velocity, steve_rect
    if is_jumping:
        steve_y += jump_velocity
        jump_velocity += GRAVITY

        # Land back on ground
        if steve_y >= steve_y_ground:
            steve_y = steve_y_ground
            is_jumping = False
            jump_velocity = 0

        steve_rect.y = steve_y

def draw_reaction():
    if not reaction_active:
        return

    # Render text
    text_surface = FONT.render(current_reaction, True, BLACK)
    padding = 10
    bg_rect = text_surface.get_rect()
    bg_rect.centerx = steve_rect.centerx
    bg_rect.bottom = steve_rect.top - 10
    bg_rect.inflate_ip(padding * 2, padding * 2)

    pygame.draw.rect(screen, TEXT_BG, bg_rect)
    pygame.draw.rect(screen, BLACK, bg_rect, 2)
    screen.blit(text_surface, text_surface.get_rect(center=bg_rect.center))

def main():
    global selected_woman, offset_x, offset_y
    global reaction_active, reaction_timer

    running = True
    while running:
        clock.tick(60)

        # ---------- EVENTS ----------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Mouse down: pick a woman if clicked
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = event.pos
                for w in women:
                    if w.collidepoint(mouse_pos):
                        selected_woman = w
                        offset_x = w.x - mouse_pos[0]
                        offset_y = w.y - mouse_pos[1]
                        break

            # Mouse up: release woman
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                selected_woman = None

            # Mouse move: drag selected woman
            elif event.type == pygame.MOUSEMOTION and selected_woman is not None:
                mouse_pos = event.pos
                selected_woman.x = mouse_pos[0] + offset_x
                selected_woman.y = mouse_pos[1] + offset_y

        # ---------- LOGIC ----------
        handle_jump()

        # Check collision between Steve and any woman
        for w in women:
            if steve_rect.colliderect(w):
                if not reaction_active:  # trigger once per contact
                    trigger_reaction()
                break
        else:
            # No collision with any woman
            pass

        # Update reaction timer
        if reaction_active:
            reaction_timer -= 1
            if reaction_timer <= 0:
                reaction_active = False

        # ---------- DRAW ----------
        screen.fill(WHITE)

        # Ground line
        pygame.draw.line(screen, BLACK, (0, HEIGHT - 50), (WIDTH, HEIGHT - 50), 3)

        # Draw Steve
        pygame.draw.rect(screen, STEVE_COLOR, steve_rect)
        name_text = FONT.render("Steve", True, BLACK)
        screen.blit(name_text, (steve_rect.x + 5, steve_rect.y - 30))

        # Draw women
        for i, w in enumerate(women, start=1):
            pygame.draw.rect(screen, WOMAN_COLOR, w)
            label = FONT.render(f"Woman {i}", True, BLACK)
            screen.blit(label, (w.x + 2, w.y - 30))

        # Draw reaction text
        draw_reaction()

        # Title
        title_text = FONT.render("Steve's Kingdom For Men", True, BLACK)
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 10))

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
