import cv2
import mediapipe as mp
import random
import math
import time
import sys
import numpy as np

# ================= SAFE IMAGE LOAD =================
def load_image(path):
    img = cv2.imread(path, cv2.IMREAD_UNCHANGED)
    if img is None:
        print(f"ERROR: Cannot load {path}")
        sys.exit(1)
    return img

# ================= IMAGE OVERLAY =================
def overlay_png(bg, fg, x, y):
    h, w = fg.shape[:2]
    if x < 0 or y < 0 or x + w > bg.shape[1] or y + h > bg.shape[0]:
        return

    if fg.shape[2] == 3:
        bg[y:y+h, x:x+w] = fg
        return

    img = fg[:, :, :3]
    mask = fg[:, :, 3] / 255.0
    mask = mask[:, :, None]
    bg[y:y+h, x:x+w] = bg[y:y+h, x:x+w] * (1 - mask) + img * mask

# ================= LOAD ASSETS =================
apple = load_image("assets/apple.png")
banana = load_image("assets/banana.png")
orange = load_image("assets/orange.png")
bomb_img = load_image("assets/bomb.png")

fruit_imgs = [apple, banana, orange]

# ================= CAMERA =================
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Camera error")
    sys.exit(1)

# ================= MEDIAPIPE =================
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

# ================= GAME DATA =================
fruits, bombs, splits = [], [], []
score = 0
game_over = False
last_spawn = time.time()

# ================= NEON SWORD =================
trail = []
MAX_TRAIL = 18

def draw_neon_trail(frame, points):
    glow = frame.copy()

    for i in range(1, len(points)):
        thickness = max(1, int(12 * i / len(points)))  # ✅ FIX
        cv2.line(
            glow,
            points[i-1],
            points[i],
            (255, 0, 255),
            thickness
        )

    glow = cv2.GaussianBlur(glow, (21, 21), 0)
    frame[:] = cv2.addWeighted(frame, 0.7, glow, 0.6, 0)

    for i in range(1, len(points)):
        cv2.line(
            frame,
            points[i-1],
            points[i],
            (255, 255, 255),
            2
        )

# ================= SPAWN =================
def spawn_fruit(w):
    img = cv2.resize(random.choice(fruit_imgs), (80, 80))
    return {
        "x": random.randint(100, w-100),
        "y": 0,
        "vy": random.randint(5, 8),
        "img": img,
        "r": 40
    }

def spawn_bomb(w):
    img = cv2.resize(bomb_img, (70, 70))
    return {
        "x": random.randint(100, w-100),
        "y": 0,
        "vy": random.randint(6, 10),
        "img": img,
        "r": 35
    }

def split_fruit(fruit):
    img = fruit["img"]
    h, w = img.shape[:2]

    splits.append({
        "img": img[:, :w//2],
        "x": fruit["x"] - 20,
        "y": fruit["y"],
        "vx": -4,
        "vy": 3
    })
    splits.append({
        "img": img[:, w//2:],
        "x": fruit["x"] + 20,
        "y": fruit["y"],
        "vx": 4,
        "vy": 3
    })

# ================= MAIN LOOP =================
while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    fx, fy = None, None

    if result.multi_hand_landmarks:
        hand = result.multi_hand_landmarks[0]
        mp_draw.draw_landmarks(frame, hand, mp_hands.HAND_CONNECTIONS)
        tip = hand.landmark[8]
        fx, fy = int(tip.x * w), int(tip.y * h)

        trail.append((fx, fy))
        if len(trail) > MAX_TRAIL:
            trail.pop(0)
    else:
        trail.clear()

    if len(trail) > 1:
        draw_neon_trail(frame, trail)

    if time.time() - last_spawn > 1:
        fruits.append(spawn_fruit(w))
        if random.random() < 0.3:
            bombs.append(spawn_bomb(w))
        last_spawn = time.time()

    for fruit in fruits[:]:
        fruit["y"] += fruit["vy"]
        overlay_png(frame, fruit["img"], fruit["x"]-40, fruit["y"]-40)

        if fx is not None and math.hypot(fruit["x"]-fx, fruit["y"]-fy) < fruit["r"]:
            score += 1
            split_fruit(fruit)
            fruits.remove(fruit)
        elif fruit["y"] > h:
            fruits.remove(fruit)

    for s in splits[:]:
        s["x"] += s["vx"]
        s["y"] += s["vy"]
        s["vy"] += 0.3
        overlay_png(frame, s["img"], int(s["x"]), int(s["y"]))
        if s["y"] > h:
            splits.remove(s)

    for bomb in bombs[:]:
        bomb["y"] += bomb["vy"]
        overlay_png(frame, bomb["img"], bomb["x"]-35, bomb["y"]-35)

        if fx is not None and math.hypot(bomb["x"]-fx, bomb["y"]-fy) < bomb["r"]:
            game_over = True
        elif bomb["y"] > h:
            bombs.remove(bomb)

    cv2.putText(
        frame,
        f"Score: {score}",
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (255,255,255),
        2
    )

    if game_over:
        cv2.putText(
            frame,
            "GAME OVER",
            (120, h//2),
            cv2.FONT_HERSHEY_SIMPLEX,
            2,
            (0,0,255),
            4
        )
        cv2.imshow("Fruit Ninja", frame)
        cv2.waitKey(2000)
        break

    cv2.imshow("Fruit Ninja", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
