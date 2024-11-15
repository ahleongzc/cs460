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
from pyzbar.pyzbar import decode
import paho.mqtt.client as mqtt
from music_player import alert, motion, cancel, notify

# 1 is for facecam, 0 is for iphone
CAMERA = 0
BROKER = "broker.hivemq.com"
MQTT_TOPIC = "g1g5.homeshield.levis.shopee"


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
            "message": f"🛡️ Home Shield 🛡️ has started with {len(os.listdir("faces"))} faces registered!The current time is {formatted_datetime}"
        } 
        with requests.post(f"http://localhost:1880/start", data=json.dumps(body)) as response:
            pass
        
    def take_photo(self, cap):
        time.sleep(1)
        _, frame = cap.read()
        cv2.imwrite('./image.jpg', frame)  # Change the filename as needed
    
    def send_photo(self, reason):
        with requests.post(f"http://localhost:1880/{reason}") as response:
            pass
    
    def get_camera(self):
        return self.camera
    
    def face_recognised(self):
        cancel_thread = threading.Thread(target=cancel)
        cancel_thread.start()
        with requests.post(f"http://localhost:1880/face_recognised") as response:
            pass
        
    def intruder_detected(self):
        self.send_photo("intruder")
        
        countdown_thread = threading.Thread(target=notify)
        countdown_thread.start()
         
        self.alarm = True
        
        for i in range(10):
            print(f"Counting down towards the end to sound off alarm {i}")
            time.sleep(1)
            if not self.alarm:
                self.face_recognised()
                print("don't need to sound off alarm")
                break
       
        if self.alarm: 
            alert_thread = threading.Thread(target=alert)
            alert_thread.start()
    
    def countdown(self, duration=5):
        send_to_telegram = True
        self.stop_event.clear()
        for i in range(duration, -1, -1):
            print(f"This is the countdown for recognising, time left is {i}")
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
        if self.recognise_countdown_thread is None or not self.recognise_countdown_thread.is_alive():
            self.recognise_countdown_thread = threading.Thread(target=self.countdown)
            self.recognise_countdown_thread.start()
            
    def start_mqtt_subscriber(self):
        broker = BROKER
        port = 1883
        client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        
        def on_connect(client, userdata, flags, reason_code, properties): 
            client.subscribe(MQTT_TOPIC)
            self.notify_camera() 
            print("connected to MQTT")
        
        def on_message(client, userdata, msg):
            print("Motion detected")
            message = msg.payload.decode('utf-8')
            if message == "cancel":
                self.alarm = False
                self.motion_detected_flag = False
            elif message == "motion":
                print(f"The motion detected flag is {self.motion_detected_flag}")
                if not self.motion_detected_flag:
                    with requests.post(f"http://localhost:1880/motion_detected") as response:
                        pass
                    self.motion_detected_flag = True
        
        client.on_connect = on_connect 
        client.on_message = on_message 
        client.connect(broker, port) 
        test = threading.Thread(target=client.loop_forever)
        test.start()
        
        
    def run_recognition(self):
        # Subsribe to the MQTT topic first 
        self.start_mqtt_subscriber()
                
        cap = cv2.VideoCapture(CAMERA)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        cap.set(cv2.CAP_PROP_FPS, 20)
        
        self.camera = cap
        
        self.encode_faces()
        
        self.stop_event = threading.Event()
        self.recognise_countdown_thread = None
        self.motion_detected_flag = False
        self.alarm = None
    
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
                    if self.recognise_countdown_thread and self.recognise_countdown_thread.is_alive():    
                        self.stop_event.set()
                    self.alarm = False
                     
            self.process_current_frame = not self.process_current_frame

            for (top, right, bottom, left), name in zip(self.face_locations, self.face_names):
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), -1)
                cv2.putText(frame, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255, 255, 255), 1)
            
            cv2.imshow("Face recognition", frame)

            key = cv2.waitKey(1) & 0xFF
            
            if self.motion_detected_flag:
                for barcode in decode(frame):
                    data = barcode.data.decode("utf8")
                    if data == "cancel":
                        self.motion_detected_flag = False
                        self.alarm = False
                        if self.recognise_countdown_thread and self.recognise_countdown_thread.is_alive():
                            self.stop_event.set()
                        
                if self.motion_detected_flag and (self.recognise_countdown_thread is None or not self.recognise_countdown_thread.is_alive()):
                    self.take_photo(cap)
                    motion_thread = threading.Thread(target=motion)
                    motion_thread.start()
                    self.recognise_countdown_thread = threading.Thread(target=self.countdown)
                    self.recognise_countdown_thread.start()

            if key == ord("q"):
                self.stop_event.set()
                break

        cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    fr = FaceRecognition()
    fr.run_recognition()
