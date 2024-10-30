import cv2
import mediapipe as mp
import pygame
import numpy as np

# Initialize MediaPipe Hand tracking
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mp_drawing = mp.solutions.drawing_utils

# Initialize pygame for sound
pygame.mixer.init()

# Map each finger tip to a piano note (MP3 files)
finger_note_map = {
    4: 'tone1.mp3',   # Thumb tip
    8: 'tone2.mp3',   # Index finger tip
    12: 'tone3.mp3',  # Middle finger tip
    16: 'tone4.mp3',  # Ring finger tip
    20: 'tone5.mp3'   # Pinky tip
}

# Load piano sound files from the absolute path
sounds = {}
for finger, note in finger_note_map.items():
    sounds[finger] = pygame.mixer.Sound(f'C:/Users/Gurudeep/OneDrive/Desktop/music/piano_sounds/{note}')

# Initialize the camera
cap = cv2.VideoCapture(0)

# Store the previous positions of finger tips
previous_positions = {finger: None for finger in finger_note_map.keys()}

def play_piano_note(finger_id):
    """Plays the corresponding piano note based on finger tip."""
    if finger_id in sounds:
        sounds[finger_id].play()

while cap.isOpened():
    success, image = cap.read()
    if not success:
        print("Ignoring empty camera frame.")
        continue

    # Flip the image horizontally for a selfie-view display
    image = cv2.flip(image, 1)

    # Convert the BGR image to RGB and process it with MediaPipe
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(image_rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            for id, landmark in enumerate(hand_landmarks.landmark):
                # Get the coordinates of each finger tip
                h, w, _ = image.shape
                cx, cy = int(landmark.x * w), int(landmark.y * h)

                # Check if the landmark is a finger tip (id 4, 8, 12, 16, 20)
                if id in finger_note_map.keys():
                    current_position = (cx, cy)

                    # Check for significant movement
                    if previous_positions[id] is None or np.linalg.norm(np.array(current_position) - np.array(previous_positions[id])) > 30:  # threshold
                        play_piano_note(id)

                    # Update the previous position
                    previous_positions[id] = current_position

            # Draw the hand landmarks on the image (optional)
            mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    # Display the result
    cv2.imshow('Hand Tracking and Piano', image)

    if cv2.waitKey(5) & 0xFF == 27:  # Press 'Esc' to exit
        break

# Clean up
cap.release()
cv2.destroyAllWindows()
pygame.quit()
