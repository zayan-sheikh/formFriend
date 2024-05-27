from flask import Flask, request, jsonify, send_file
import cv2
import mediapipe as mp
import numpy as np
import os
from flask_cors import CORS
import cv2
import pandas as pd
import pickle
import sklearn


import warnings

# Suppress specific sklearn warning
warnings.filterwarnings("ignore", message="X does not have valid feature names, but StandardScaler was fitted with feature names")

# Suppress the protobuf deprecation warning
warnings.filterwarnings("ignore", message="SymbolDatabase.GetPrototype() is deprecated. Please use message_factory.GetMessageClass() instead.")

# Your imports and code
# Example imports
from sklearn.preprocessing import StandardScaler
import numpy as np
import warnings
warnings.filterwarnings("ignore", category=UserWarning, message='SymbolDatabase.GetPrototype() is deprecated')

# Example code
scaler = StandardScaler()



app = Flask(__name__)
CORS(app)
CORS(app, resources={r"/*": {"origins": "*"}})

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
def process2_side_squat_video(file_path):
    print('processing vid')
    cap = cv2.VideoCapture(file_path)
    feedback = 'hi'
    filename, extension = os.path.splitext(os.path.basename(file_path))
    output_path = os.path.join('static', 'videos', f'{filename}_output{extension}')
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
                print('processing landmarks')
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
                print('still processing')
                cv2.rectangle(image, (0,0), (400,60), (245,117,16), -1)
                cv2.putText(image, "FEEDBACK", (15,12), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1, cv2.LINE_AA)
                cv2.putText(image, str(feedback), (15,30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1, cv2.LINE_AA)
            except:
                pass

            cv2.imshow('Mediapipe Feed', image)
            if cv2.waitKey(10) & 0xFF == ord('q'):
                break
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
            out.write(image)
        cap.release()
        out.release()
        print(output_path)
        return output_path

def process_side_squat_video(file_path):
    # Implement side squat video processing logic here
    cap = cv2.VideoCapture(file_path)
    print('processing vid')
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
                print('processing still')
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
            cv2.imshow('Video with Landmarks', image)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            out.write(image)
        cap.release()
        out.release()
        return output_path

def count_reps_side(file_path):
    

def count_reps_front(file_path):
    print('got req to count front reps')

    return 1
    pass

import cv2

# Suppress specific warnings
import warnings
warnings.filterwarnings("ignore", category=UserWarning, message='SymbolDatabase.GetPrototype() is deprecated')

def process_front_squat_video(video_path):
    # Load models
    cap = cv2.VideoCapture(video_path)
    filename, extension = os.path.splitext(os.path.basename(video_path))
    output_path = os.path.join('static', 'videos', f'{filename}_output{extension}')
    #output_path = os.path.join('static', 'videos', 'output.mp4')
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, 20.0, (int(cap.get(3)), int(cap.get(4))))

    front_up_down_model = pickle.load(open('FrontUpDownData.pkl', 'rb'))
    knees_caving_model = pickle.load(open('kneesCaving.pkl', 'rb'))
    mp_drawing = mp.solutions.drawing_utils 
    mp_pose = mp.solutions.pose
    
    current_stage = ''
    counter = 0
    stage = ''
    feedback = ''
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False  # Save memory

            # Make detections from the pose
            results = pose.process(image)  # Get detections
            
            # Convert back to BGR
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            if results.pose_landmarks:
                mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
                
                try:
                    landmarks = results.pose_landmarks.landmark
                    row = np.array([[res.x, res.y, res.z, res.visibility] for res in landmarks]).flatten()
                    X = pd.DataFrame([row])

                    # Predict using front up/down model
                    front_up_down_class = front_up_down_model.predict(X)[0]
                    front_up_down_prob = front_up_down_model.predict_proba(X)[0]

                    if front_up_down_class == 2 and front_up_down_prob.max() >= 0.7:
                        current_stage = 'down'
                        # Predict using knees caving model
                        knees_caving_class = knees_caving_model.predict(X)[0]
                        knees_caving_prob = knees_caving_model.predict_proba(X)[0]
                        if knees_caving_class == 1:
                            feedback = "knees in"
                        else:
                            feedback = "knees out"
                    elif current_stage == 'down' and front_up_down_class == 1 and front_up_down_prob.max() >= 0.7:
                        current_stage = 'up'
                        counter += 1
                        feedback = ''

                    if front_up_down_class == 1:
                        stage = "up"
                    elif front_up_down_class == 2:
                        stage = "down"
                            # Display the frame with landmarks and connections
                    # Drawing rectangles and text on the image
                    cv2.rectangle(image, (0, 0), (400, 60), (245, 117, 16), -1)

                    # Drawing predicted class
                    cv2.putText(image, "CLASS", (95, 12), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
                    cv2.putText(image, str(stage), (90, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)

                    # Drawing predicted probability
                    cv2.putText(image, "PROB", (15, 12), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
                    cv2.putText(image, str(round(front_up_down_prob.max(), 2)), (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)

                    # Drawing counter
                    cv2.putText(image, "COUNTER", (180, 12), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
                    cv2.putText(image, str(counter), (175, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)

                    # Drawing feedback
                    cv2.putText(image, "FEEDBACK", (250, 12), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
                    cv2.putText(image, str(feedback), (245, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)

                except Exception as e:
                    print(e)
                    break
            
            cv2.imshow('Video with Landmarks', image)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            out.write(image)

    cap.release()
    cv2.destroyAllWindows()
    return output_path




from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/uploadRepCount', methods=['post'])
def upload_repcount_file():
    print('got a post request')
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
            counter = count_reps_side(video_path)
        elif squat_type == 'front':
            counter = 1
        

       # output_path = process_video(video_path)
        return str(10)
    

@app.route('/upload', methods=['post'])
@app.route('/upload', methods=['post'])
def upload_file():
    print('Got a POST request')
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
            output_path = process_front_squat_video(video_path)

        return send_file(output_path, as_attachment=True, download_name='output.mp4')


@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    response.headers['Access-Control-Allow-Methods'] = 'OPTIONS, HEAD, GET, POST, PUT, DELETE'
    return response

if __name__ == '__main__':
    app.run(debug=True)
