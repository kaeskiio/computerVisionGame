import pygame
import random
import sys

#ignore
# Initialize pygame
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
IMAGE_WIDTH, IMAGE_HEIGHT = 600, 450
BLOCK_SIZE = 50  # Reduced block size
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
GREEN = (50, 200, 50)
RED = (200, 50, 50)
FONT_SIZE = 24  # Reduced font size for smaller text
BUTTON_WIDTH, BUTTON_HEIGHT = 120, 60
CBUTTON_WIDTH, CBUTTON_HEIGHT = 100, 60
CHOICE_BOX_WIDTH, CHOICE_BOX_HEIGHT = 130, 40
CHOICE_BOX_GAP = 20
IMAGE_Y_OFFSET = 50  # Offset to scoot the image up

# Load celebrity images and names
celebrities = [
    ("celebrity.png", "Kacem"),
    ("jason.png", "Jason Momoa"),
    ("rock.png", "The Rock"),
    ("rihanna.png", "Rihanna"),
    ("roger.png", "Roger Federer"),
    ("djokovic.png", "Novak Djokovic"),
    ("messi.jpeg", "Lionel Messi"),
    ("drjoe.png", "Dr. Joe"),
    ("mrfranklin.png", "Mr. Franklin"),
    ("steve.png", "Steve Harvey"),
]

# Screen setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Guess the Celebrity')

# Font setup
font = pygame.font.Font(None, FONT_SIZE)

# Global variables
choices = []
celebrity_image = None
correct_answer = ""
revealed_blocks = set()  # Initialize revealed_blocks as a global set
game_over = False  # Initialize game_over as a global variable


def draw_button(text, x, y, width, height, active=True):
    color = GRAY if active else BLACK
    pygame.draw.rect(screen, color, (x, y, width, height))
    pygame.draw.rect(screen, BLACK, (x, y, width, height), 2)
    button_text = font.render(text, True, BLACK)
    text_rect = button_text.get_rect(center=(x + width // 2, y + height // 2))
    screen.blit(button_text, text_rect)


def draw_choices(choices):
    for i, choice in enumerate(choices):
        row = i // 2
        col = i % 2
        x = SCREEN_WIDTH // 2 - (CHOICE_BOX_WIDTH + CHOICE_BOX_GAP) + col * (CHOICE_BOX_WIDTH + CHOICE_BOX_GAP)
        y = SCREEN_HEIGHT - 120 + row * (CHOICE_BOX_HEIGHT + CHOICE_BOX_GAP)

        pygame.draw.rect(screen, BLACK, (x, y, CHOICE_BOX_WIDTH, CHOICE_BOX_HEIGHT), 2)

        if game_over:
            color = GREEN if choice == correct_answer else RED
        else:
            color = WHITE

        pygame.draw.rect(screen, color, (x + 2, y + 2, CHOICE_BOX_WIDTH - 4, CHOICE_BOX_HEIGHT - 4))

        choice_text = font.render(choice, True, BLACK)
        text_rect = choice_text.get_rect(center=(x + CHOICE_BOX_WIDTH // 2, y + CHOICE_BOX_HEIGHT // 2))
        screen.blit(choice_text, text_rect)


def new_round():
    global correct_answer, choices, celebrity_image, revealed_blocks, game_over
    revealed_blocks.clear()
    game_over = False
    # Select a random celebrity
    img, correct_answer = random.choice(celebrities)
    celebrity_image = pygame.transform.scale(pygame.image.load(img), (IMAGE_WIDTH, IMAGE_HEIGHT))

    if correct_answer in ["Mr. Franklin", "Steve Harvey"]:
        # Ensure both Mr. Franklin and Steve Harvey are included in the choices
        if correct_answer == "Mr. Franklin":
            similar_choice = "Steve Harvey"
        else:
            similar_choice = "Mr. Franklin"
        incorrect_choices = [name for _, name in celebrities if name not in [correct_answer, similar_choice]]
        choices = random.sample(incorrect_choices, 2) + [correct_answer, similar_choice]
    else:
        # Ensure the correct answer is in the choices and add three incorrect choices
        incorrect_choices = [name for _, name in celebrities if name != correct_answer]
        choices = random.sample(incorrect_choices, 3) + [correct_answer]

    random.shuffle(choices)


new_round()

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos

            if not game_over:
                # Check if the "Continue" button was clicked
                continue_button_x = SCREEN_WIDTH - CBUTTON_WIDTH - 40
                continue_button_y = SCREEN_HEIGHT - 150
                if continue_button_x < mouse_x < continue_button_x + CBUTTON_WIDTH and continue_button_y < mouse_y < continue_button_y + CBUTTON_HEIGHT:
                    while True:
                        x = random.randint(0, IMAGE_WIDTH // BLOCK_SIZE - 1)
                        y = random.randint(0, IMAGE_HEIGHT // BLOCK_SIZE - 1)
                        if (x, y) not in revealed_blocks:
                            revealed_blocks.add((x, y))
                            break

            # Check if any choice box was clicked
            for i, choice in enumerate(choices):
                row = i // 2
                col = i % 2
                choice_box_x = SCREEN_WIDTH // 2 - (CHOICE_BOX_WIDTH + CHOICE_BOX_GAP) + col * (CHOICE_BOX_WIDTH + CHOICE_BOX_GAP)
                choice_box_y = SCREEN_HEIGHT - 120 + row * (CHOICE_BOX_HEIGHT + CHOICE_BOX_GAP)
                if choice_box_x < mouse_x < choice_box_x + CHOICE_BOX_WIDTH and choice_box_y < mouse_y < choice_box_y + CHOICE_BOX_HEIGHT:
                    if choice == correct_answer:
                        print("Correct!")
                    else:
                        print("Wrong!")
                    game_over = True

            # Check if the "Next Round" button was clicked
            next_round_button_x = SCREEN_WIDTH - BUTTON_WIDTH - 30
            next_round_button_y = SCREEN_HEIGHT - 5 - BUTTON_HEIGHT - 20
            if game_over and next_round_button_x < mouse_x < next_round_button_x + BUTTON_WIDTH and next_round_button_y < mouse_y < next_round_button_y + BUTTON_HEIGHT:
                new_round()

            # Check if the "Show Picture" button was clicked
            show_picture_button_x = SCREEN_WIDTH - BUTTON_WIDTH - 600
            show_picture_button_y = SCREEN_HEIGHT - 5 - BUTTON_HEIGHT - 20
            if game_over and show_picture_button_x < mouse_x < show_picture_button_x + BUTTON_WIDTH and show_picture_button_y < mouse_y < show_picture_button_y + BUTTON_HEIGHT:
                for x in range(IMAGE_WIDTH // BLOCK_SIZE):
                    for y in range(IMAGE_HEIGHT // BLOCK_SIZE):
                        revealed_blocks.add((x, y))

        if event.type == pygame.KEYDOWN and game_over:
            if event.key == pygame.K_r:
                new_round()

    # Draw the game
    screen.fill(WHITE)
    for x, y in revealed_blocks:
        screen.blit(celebrity_image, (
            x * BLOCK_SIZE + (SCREEN_WIDTH - IMAGE_WIDTH) // 2, y * BLOCK_SIZE + (SCREEN_HEIGHT - IMAGE_HEIGHT) // 2 - IMAGE_Y_OFFSET),
                    (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

    # Draw the "Continue" button
    draw_button("Continue", SCREEN_WIDTH - CBUTTON_WIDTH - 40, SCREEN_HEIGHT - 150, CBUTTON_WIDTH, CBUTTON_HEIGHT,
                not game_over)

    if game_over:
        # Draw the "Next Round" button
        draw_button("Next Round", SCREEN_WIDTH - BUTTON_WIDTH - 30, SCREEN_HEIGHT - 5 - BUTTON_HEIGHT - 20,
                    BUTTON_WIDTH, BUTTON_HEIGHT)
        draw_button("Show Picture", SCREEN_WIDTH - BUTTON_WIDTH - 600, SCREEN_HEIGHT - 5 - BUTTON_HEIGHT - 20,
                    BUTTON_WIDTH, BUTTON_HEIGHT)

    # Draw the choices with feedback
    draw_choices(choices)

    pygame.display.flip()

pygame.quit()
