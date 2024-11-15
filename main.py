import datetime, os, time, textwrap
from flask import Flask, jsonify
from face_rec_process import FaceRecognition

import shutil

app = Flask(__name__)
process = None
start_time = None

PROCESS_NOT_RUNNING = "Home Shield is not running! Please send in /start first"

@app.post("/start_process")
def start_process():
    global process, start_time
    if len(os.listdir("faces")) == 0 and len(os.listdir("tmp")) == 0:
        return jsonify({"message": f"You need to register a photo first my love"}), 201
    
    if process:
        return jsonify(
            {
                "message": "Home Shield is ongoing already!!! You are safe"
            }
        ), 400
        
    process = FaceRecognition()
    process.start_process()
    start_time = time.time()
    
    return jsonify(
        {
            "message": f"🛡️ Home Shield 🛡️ is starting now, a notification will be sent when it's fully operational!!! Be patient love 🥰" 
        }
    ), 201
    
@app.post("/stop_process")
def stop_process():
    global process, start_time
    if not process:
        return jsonify(
            {
                "message": "You already stopped the facial recognition process!!!"
            }
        ), 400
         
    process.end_process()
    process = None
    start_time = None
    
    now = datetime.datetime.now()
    formatted_datetime = now.strftime("%Y-%m-%d %H:%M:%S") 
    
    return jsonify(
        {
            "message": f"🛡️ Home Shield 🛡 has stopped at {formatted_datetime}, be aware that your home is not safeguarded from intruders now 😈😈",
        }
    ), 202
    
@app.post("/list_faces")
def list_faces():
    if len(os.listdir("faces")) == 0:
        return jsonify({"message": f"There are no faces in your database love"}), 201
    
    names = "These faces are in the hall of fame yo 🥵🥵:\n"
    count = 1
    for image in os.listdir("faces"):
        names += f"{count}. {image.split(".")[0]}\n"
        count += 1
        
    return jsonify(
        {
            "message": f"{names}",
        }
    ), 201

@app.post("/list_new_faces")
def list_new_faces():
    if len(os.listdir("tmp")) == 0:
        return jsonify({"message": f"There are no new faces to be registered love"}), 201
    
    names = "Unregistered people:\n"
    count = 1
    for image in os.listdir("tmp"):
        names += f"{count}. {image.split(".")[0]}\n"
        count += 1
        
    return jsonify(
        {
            "message": f"{names}",
        }
    ), 201

@app.post("/delete")
def delete_face():

    
    pass

@app.post("/restart")
def restart():
    global process, start_time
    if not process:
        return jsonify({"message": "You cannot restart if it's not running in the first place love"}), 400
    
    process.end_process() 
    process.start_process()
    start_time = time.time()
    
    return jsonify({"message": "Home Shield has started, will send a notification when it's fully operational!!!"}), 400

@app.post("/status")
def status():
    global process, start_time
    if not process:
        return jsonify(
            {
                "message": PROCESS_NOT_RUNNING
            }
        ), 400
    
    cur_time = time.time() 
    running_time = cur_time - start_time
    
    response = f"Home Shield is up for {int(running_time)} seconds!"
    if len(os.listdir("tmp")) != 0:
        response += f"""\n\nHowever, You have new faces (total of {len(os.listdir("tmp"))}) that is unregistered yet!\nSend in /list_new_faces to see their names or run /restart to apply them now love"""
    
    return jsonify(
        {
            "message": response
        }
    ), 201
    
@app.post("/motion_detected")
def motion_detected():
    global process
    if not process:
        return jsonify(
            {
                "message": PROCESS_NOT_RUNNING
            }
        ), 400
    
    process.motion()
    return jsonify(
        {
            "message": "A motion has been detected"
        }
    ), 201
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=30000)
