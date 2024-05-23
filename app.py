from flask import Flask, request, render_template, send_file
import cv2
import mediapipe as mp
import numpy as np
import os

app = Flask(__name__)

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
 #def process_video(file_path):
    

    return output_path
def process_side_squat_video(file_path):
    # Implement side squat video processing logic here
    cap = cv2.VideoCapture(file_path)
    feedback = 'hi'
    filename, extension = os.path.splitext(os.path.basename(file_path))
    output_path = os.path.join('static', 'videos', f'{filename}_output{extension}')
    #output_path = os.path.join('static', 'videos', 'output.mp4')
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, 20.0, (int(cap.get(3)), int(cap.get(4))))

    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
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
                 # Drawing rectangles and text on the image
                cv2.rectangle(image, (0,0), (400,60), (245,117,16), -1)
                
                # Drawing predicted class
                cv2.putText(image, "FEEDBACK", (15,12), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1, cv2.LINE_AA)
                cv2.putText(image, str(feedback), (15,30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1, cv2.LINE_AA)
                #cv2.putText(image, str(feedback), (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
            except:
                pass
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
            out.write(image)
        cap.release()
        out.release()
        return output_path

# Function to process front squat video and provide feedback
def process_front_squat_video(file_path):
    # Implement front squat video processing logic here
    pass

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part'
    file = request.files['file']
    squat_type = request.form['squat_type']

    if file.filename == '':
        return 'No selected file'
    if file:
        video_path = os.path.join('static', 'videos', file.filename)
        file.save(video_path)

        if squat_type == 'side':
            output_path = process_side_squat_video(video_path)
        elif squat_type == 'front':
            output_path= process_front_squat_video(video_path)

        #output_path = process_video(video_path)
        return send_file(output_path, as_attachment=True, download_name='output.mp4')
    
if __name__ == "__main__":
    if not os.path.exists('static/videos'):
        os.makedirs('static/videos')
    app.run(debug=True)
