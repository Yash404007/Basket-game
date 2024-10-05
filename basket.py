import cv2 
import numpy as np 
import random

# Initialize game parameters
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
BASKET_WIDTH = 100
BASKET_HEIGHT = 50
LETTER_SIZE = 30
FALL_SPEED = 5
SPAWN_RATE = 60  # Frames between letter spawns

# Initialize game state
score = 0
letters = []
basket_x = WINDOW_WIDTH // 2 - BASKET_WIDTH // 2

# Create a function to generate random letters
def generate_letter():
    letter = chr(random.randint(65, 90))  # ASCII values for A-Z
    x = random.randint(0, WINDOW_WIDTH - LETTER_SIZE)
    return {'char': letter, 'x': x, 'y': 0}

# Main game loop
def game_loop():
    global score, letters, basket_x

    # Create a window
    cv2.namedWindow('Letter Collection Game')

    frame_count = 0

    while True:
        # Create a blank image
        frame = np.zeros((WINDOW_HEIGHT, WINDOW_WIDTH, 3), dtype=np.uint8)

        # Spawn new letters
        if frame_count % SPAWN_RATE == 0:
            letters.append(generate_letter())

        # Update letter positions and check for collection
        for letter in letters[:]:
            letter['y'] += FALL_SPEED
            
            # Check if letter is collected
            if (letter['y'] + LETTER_SIZE > WINDOW_HEIGHT - BASKET_HEIGHT and
                basket_x < letter['x'] < basket_x + BASKET_WIDTH):
                score += 1
                letters.remove(letter)
            # Remove letters that fall off the screen
            elif letter['y'] > WINDOW_HEIGHT:
                letters.remove(letter)

        # Draw letters
        for letter in letters:
            cv2.putText(frame, letter['char'], (letter['x'], letter['y']), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        # Draw basket
        cv2.rectangle(frame, (basket_x, WINDOW_HEIGHT - BASKET_HEIGHT),
                      (basket_x + BASKET_WIDTH, WINDOW_HEIGHT), (0, 255, 0), -1)

        # Draw score
        cv2.putText(frame, f'Score: {score}', (10, 30), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        # Show the frame
        cv2.imshow('Letter Collection Game', frame)

        # Handle keyboard input
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('a') and basket_x > 0:
            basket_x -= 10
        elif key == ord('d') and basket_x < WINDOW_WIDTH - BASKET_WIDTH:
            basket_x += 10

        frame_count += 1

    cv2.destroyAllWindows()

if __name__ == "__main__":
    game_loop()