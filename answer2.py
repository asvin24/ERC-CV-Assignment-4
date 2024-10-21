
import cv2
import mediapipe as mp
import numpy as np
import random


# Initialize MediaPipe Hands
mpHands=mp.solutions.hands
hands=mpHands.Hands()
mpDraw=mp.solutions.drawing_utils


# Game settings
width, height = 1280, 640
player_pos = [320, 440]


# enemy speed, size, and list initialization
enemy_speed=5
spawn_rate_parameter=0.05
size=50             #enemy size=player size
enemy_list=[]



# Initialize score
score=0

# Create random enemy

def create_enemy():
    ex=random.randrange(width-size)
    return [ex,0]


    

# Move enemies down
def move_enemies(enemy_list):
    global enemy_speed
    for enemy in enemy_list:
        enemy[1] += enemy_speed
    
# Check if enemy is off-screen
def check_off_screen(enemy_list):
    global score
    global enemy_speed
    global spawn_rate_parameter
    for enemy in enemy_list:
        if enemy[1] > height:
            enemy_list.remove(enemy)
            score += 1             # Increment score for each enemy that goes off-screen
            spawn_rate_parameter+=0.005      



# Check for collisions
def check_collision(player_pos, enemy_list):
    global size
    for enemy in enemy_list: 
        if (player_pos[0] < enemy[0] + size and
            player_pos[0] + size > enemy[0] and
            player_pos[1] < enemy[1] + size and
            player_pos[1] + size > enemy[1]):
            return True
    return False
    
    
# Initialize webcam
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH,width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT,height)



while True:
    ret, frame = cap.read()
    
    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    
    # Process the frame with MediaPipe
    results=hands.process(rgb_frame)
       
    # Get coordinates of the index finger tip (landmark 8)
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            cx,cy=int(handLms.landmark[8].x*width),int(handLms.landmark[8].y*height)
            player_pos=[cx,cy]            # Move player based on hand movement
            
   
    # Add new enemies
    if random.random() < spawn_rate_parameter:       #adjusting the spawn rate
        enemy_list.append(create_enemy())

    
    # Move enemies
    move_enemies(enemy_list)

    #check for off screen enemies
    check_off_screen(enemy_list)


    
    # Check for collision
    if check_collision(player_pos, enemy_list):
        print("Game Over! Final Score:", str(score))
        break

    
    # Draw game elements
    frame = cv2.rectangle(frame, (player_pos[0], player_pos[1]), (player_pos[0] + size, player_pos[1] + size), (0, 255, 0), -1)

    for enemy in enemy_list:
        frame = cv2.rectangle(frame, (enemy[0], enemy[1]), (enemy[0] + size, enemy[1] +size), (0, 0, 255), -1)


    
    # Display score on the frame
    cv2.putText(frame, 'Score:'+str(score), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)



    cv2.imshow("Object Dodging Game", frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()