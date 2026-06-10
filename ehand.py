import cv2
import mediapipe as mp
import numpy as np

# Initialisation
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

FINGER_NAMES = ["Pouce", "Index", "Majeur", "Annulaire", "Auriculaire"]
FINGER_COLORS = [
    (180, 100, 255),  # Violet — Pouce
    (255, 180, 0),    # Cyan — Index
    (0, 255, 120),    # Vert — Majeur
    (0, 180, 255),    # Orange — Annulaire
    (255, 80, 80),    # Rouge — Auriculaire
]

FINGER_POINTS = [
    [1, 2, 3, 4],
    [5, 6, 7, 8],
    [9, 10, 11, 12],
    [13, 14, 15, 16],
    [17, 18, 19, 20]
]

def calculate_angle(p1, p2, p3):
    v1 = np.array(p1) - np.array(p2)
    v2 = np.array(p3) - np.array(p2)
    cos_angle = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2) + 1e-6)
    return np.degrees(np.arccos(np.clip(cos_angle, -1.0, 1.0)))

def angle_to_pwm(flexion_pct):
    """Convertit % flexion → signal PWM (544µs à 2400µs)"""
    return int(np.interp(flexion_pct, [0, 100], [544, 2400]))

def angle_to_servo_deg(flexion_pct):
    """Convertit % flexion → angle servo (0° à 180°)"""
    return int(np.interp(flexion_pct, [0, 100], [0, 180]))

cap = cv2.VideoCapture(0)
print("E-Hand — Simulation PWM Servos. Appuie sur Q pour quitter.")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Panneau de droite pour les servos
    panel = np.zeros((frame.shape[0], 300, 3), dtype=np.uint8)

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    flexions = [0] * 5
    pwm_values = [544] * 5
    servo_degs = [0] * 5

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            h, w, _ = frame.shape
            lm = hand_landmarks.landmark

            for i, points in enumerate(FINGER_POINTS):
                p1 = [lm[points[0]].x * w, lm[points[0]].y * h]
                p2 = [lm[points[1]].x * w, lm[points[1]].y * h]
                p3 = [lm[points[2]].x * w, lm[points[2]].y * h]
                angle = calculate_angle(p1, p2, p3)
                flexions[i] = int(np.interp(angle, [0, 180], [100, 0]))
                pwm_values[i] = angle_to_pwm(flexions[i])
                servo_degs[i] = angle_to_servo_deg(flexions[i])

    # ── PANNEAU SERVOS ──
    cv2.putText(panel, "E-Hand Servos", (20, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
    cv2.putText(panel, "Simulation PWM", (20, 52),
                cv2.FONT_HERSHEY_SIMPLEX, 0.45, (150, 150, 150), 1)
    cv2.line(panel, (10, 62), (290, 62), (50, 50, 50), 1)

    for i, name in enumerate(FINGER_NAMES):
        y = 90 + i * 80
        color = FINGER_COLORS[i]

        # Nom du doigt
        cv2.putText(panel, f"Servo {i+1} — {name}",
                    (15, y), cv2.FONT_HERSHEY_SIMPLEX, 0.45, color, 1)

        # Angle servo
        cv2.putText(panel, f"{servo_degs[i]:3d} deg",
                    (15, y + 18), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

        # PWM
        cv2.putText(panel, f"PWM: {pwm_values[i]} us",
                    (120, y + 18), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (200, 200, 200), 1)

        # Barre de progression
        cv2.rectangle(panel, (15, y + 26), (280, y + 44), (40, 40, 40), -1)
        bar_w = int(flexions[i] * 2.65)
        cv2.rectangle(panel, (15, y + 26), (15 + bar_w, y + 44), color, -1)
        cv2.putText(panel, f"{flexions[i]}%",
                    (245, y + 40), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)

    # ── TITRE CAMÉRA ──
    cv2.putText(frame, "E-Hand — Hand Tracking",
                (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

    # Fusion caméra + panneau
    combined = np.hstack([frame, panel])
    cv2.imshow("E-Hand — Bionic Hand Control", combined)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
