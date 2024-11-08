import face_recognition
import os
import cv2
import json
import numpy as np
import math
import threading
import requests
import time
import multiprocessing
import datetime
import shutil
import paho.mqtt.client as mqtt
from music_player import alert

# 1 is for facecam, 0 is for iphone
CAMERA = 1

class FaceRecognition:
    face_locations = []
    face_encodings = []
    face_names = []
    known_face_encodings = []
    known_face_names = []
    process_current_frame = True

    def __init__(self):
        pass
    
    def move_photos(self):
        for image in os.listdir("tmp"):
            source = f"./tmp/{image}" 
            destination = f"./faces/{image}"
            shutil.move(source, destination)
    
    def start_process(self):
        self.move_photos()
        self.process = multiprocessing.Process(target=self.run_recognition)
        self.process.start()
        
    def end_process(self):
        if not self.process:
            return
        try: 
            self.process.terminate()
        except Exception as e:
            print(f"{str(self.__class__.__name__)} {str(e)}")
    
    def face_confidence(self, face_distance, face_match_threshold=0.8):
        range = (1.0 - face_match_threshold)
        linear_val = (1.0 - face_distance) / (range * 2.0)

        if face_distance > face_match_threshold:
            return str(round(linear_val * 100, 2)) + "%"
        else:
            value = (linear_val + ((1.0 - linear_val) *
                    math.pow((linear_val - 0.5) * 2, 0.2))) * 100
            return str(round(value, 2)) + "%"    

    def notify_camera(self):
        now = datetime.datetime.now()
        formatted_datetime = now.strftime("%Y-%m-%d %H:%M:%S") 
        body = {
            "message": f"Home Shield has started with {len(os.listdir("faces"))} faces registered!\nThe current time is {formatted_datetime}"
        } 
        with requests.post(f"http://localhost:1880/start", data=json.dumps(body)) as response:
            pass
        
    def take_photo(self, cap):
        _, frame = cap.read()
        time.sleep(1)
        _, frame = cap.read()
        cv2.imwrite('./image.jpg', frame)  # Change the filename as needed
    
    def send_photo(self, reason="take_photo"):
        with requests.post(f"http://localhost:1880/{reason}") as response:
            pass
    
    def request_photo(self):
        new_camera = cv2.VideoCapture(CAMERA)
        self.take_photo(new_camera)
        self.send_photo()
        new_camera.release()
    
    def face_recognised(self):
        with requests.post(f"http://localhost:1880/face_recognised") as response:
            pass
        
    def intruder_detected(self):
        cap = cv2.VideoCapture(CAMERA)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        cap.set(cv2.CAP_PROP_FPS, 20)
        
        self.take_photo(cap)
        self.send_photo("intruder")
        cap.release()
        alert_thread = threading.Thread(target=alert)
        alert_thread.start()
    
    def countdown(self, duration=5):
        send_to_telegram = True
        self.stop_event.clear()
        for i in range(duration, -1, -1):
            print(i)
            time.sleep(1)
            if self.stop_event.is_set():
                send_to_telegram = False
                self.motion_detected_flag = False
                self.face_recognised()
                break
        if not send_to_telegram:
            return 
        self.intruder_detected()
        self.motion_detected_flag = False
        

    def encode_faces(self):
        for image in os.listdir("faces"):
            face_image = face_recognition.load_image_file(f"faces/{image}")
            face_encoding = face_recognition.face_encodings(face_image)[0]

            self.known_face_encodings.append(face_encoding)
            self.known_face_names.append(image)

        print(self.known_face_names)
    
    def start_countdown(self):
        if self.countdown_thread is None or not self.countdown_thread.is_alive():
            self.countdown_thread = threading.Thread(
                target=self.countdown)
            self.countdown_thread.start()
            
    def motion(self):
        # with requests.post(f"http://localhost:1880/motion_detected") as response:
        #     pass
        print("MOTION HAS BEEN CALLED") 
        self.motion_detected_flag = True
        
    def start_mqtt_subscriber(self):
        broker = "localhost" 
        port = 1883
        
        client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

        def on_connect(client, userdata, flags, reason_code, properties):
            client.subscribe("motion")
        
        def on_message(client, userdata, msg):
            with requests.post(f"http://localhost:1880/motion_detected") as response:
                pass
            self.motion_detected_flag = True
        
        client.on_connect = on_connect 
        client.on_message = on_message 
        
        client.connect(broker, port) 
        
        test = threading.Thread(
            target=client.loop_forever
        )
        
        test.start()
        

    def run_recognition(self):
        cap = cv2.VideoCapture(CAMERA)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        cap.set(cv2.CAP_PROP_FPS, 20)
        
        self.start_mqtt_subscriber()
        
        self.notify_camera() 
        self.encode_faces()
        self.stop_event = threading.Event()
        self.countdown_thread = None
        self.motion_detected_flag = False
    
        while True:
            ret, frame = cap.read()
    
            if self.process_current_frame:
                small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
                rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
                self.face_locations = face_recognition.face_locations(
                    rgb_small_frame)
                self.face_encodings = face_recognition.face_encodings(
                    rgb_small_frame, self.face_locations)

                self.face_names = [] 
                registered_faces = False
                
                for face_encoding in self.face_encodings:
                    matches = face_recognition.compare_faces(
                        self.known_face_encodings, face_encoding)
                    name = "Unknown"
                    confidence = "Unknown"

                    face_distance = face_recognition.face_distance(
                        self.known_face_encodings, face_encoding)
                    best_match_index = np.argmin(face_distance)

                    if matches[best_match_index]:
                        name = self.known_face_names[best_match_index]
                        confidence = self.face_confidence(face_distance[best_match_index])
                        registered_faces = True
                    self.face_names.append(f"{name} ({confidence})")
                
                if registered_faces:
                    if self.countdown_thread and self.countdown_thread.is_alive():
                        self.stop_event.set()
                     
            self.process_current_frame = not self.process_current_frame

            for (top, right, bottom, left), name in zip(self.face_locations, self.face_names):
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4

                cv2.rectangle(frame, (left, top),
                              (right, bottom), (0, 0, 255), 2)
                cv2.rectangle(frame, (left, bottom - 35),
                              (right, bottom), (0, 0, 255), -1)
                cv2.putText(frame, name, (left + 6, bottom - 6),
                            cv2.FONT_HERSHEY_DUPLEX, 0.8, (255, 255, 255), 1)

            cv2.imshow("Face recognition", frame)

            key = cv2.waitKey(1) & 0xFF
            
            # print(f"motion detected {self.motion_detected_flag}")
            
            if self.motion_detected_flag:
                if self.countdown_thread is None or not self.countdown_thread.is_alive():
                    self.countdown_thread = threading.Thread(
                        target=self.countdown)
                    self.countdown_thread.start()

            if key == ord("q"):
                self.stop_event.set()
                break
            elif key == ord("a"):
                self.motion()
            elif key == ord("b"):
                self.stop_event.set()

        cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    fr = FaceRecognition()
    fr.run_recognition()
