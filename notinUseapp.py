import tkinter as tk
from tkinter import filedialog
import customtkinter as ck
import cv2
import mediapipe as mp
import numpy as np
from PIL import Image, ImageTk

# Initialize Mediapipe pose detection
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

# Function to calculate angle
def calculate_angle(a, b, c):
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)
    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians * 180.0 / np.pi)
    if angle > 180.0:
        angle = 360 - angle
    return angle

# Function to process video and provide feedback
def process_video(video_path):
    cap = cv2.VideoCapture(video_path)
    feedback = 'hi'
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            width = cap.get(3)
            height = cap.get(4)
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False
            results = pose.process(image)
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            try:
                landmarks = results.pose_landmarks.landmark
                shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x, landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
                knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x, landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
                ankle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x, landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]
                angle = calculate_angle(shoulder, hip, knee)
                angle2 = calculate_angle(hip, knee, ankle)
                angle_diff = angle - angle2
                if angle2 < 80:
                    if angle_diff < -10:
                        feedback = 'You are leaning forward, keep chest up'
                    else:
                        feedback = 'goodform'
                else:
                    feedback = ''
                cv2.putText(image, str(feedback), (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
            except:
                pass
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
            cv2.imshow('Mediapipe Feed', image)
            if cv2.waitKey(10) & 0xFF == ord('q'):
                break
        cap.release()
        cv2.destroyAllWindows()

# Function to open file dialog
def open_file_dialog():
    file_path = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4;*.avi")])
    if file_path:
        process_video(file_path)

#from landmarks import landmarks
window = tk.Tk()
window.geometry("800x900")
window.title("Squat form Analyzer") 
ck.set_appearance_mode("dark")


upload_button = ck.CTkButton(window, text="Upload Video", command=open_file_dialog)
upload_button.place(x=10, y=100)

window.mainloop()