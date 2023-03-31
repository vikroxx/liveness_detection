import os
from os import environ
from pathlib import Path
from gunicorn.app.wsgiapp import run
import cv2
import numpy as np
from dotenv import load_dotenv
from facetools import FaceDetection, IdentityVerification, LivenessDetection
from flask import Flask, Response, request, jsonify
import time
from io import BytesIO
import base64

root = Path(os.path.abspath(__file__)).parent.absolute()

load_dotenv((root / ".env").as_posix())  # take environment variables from .env.

data_folder = environ.get("DATA_FOLDER")
resnet_name = environ.get("RESNET")
deeppix_name = environ.get("DEEPPIX")
facebank_name = environ.get("FACEBANK")


data_folder = root.parent / data_folder

resNet_checkpoint_path = data_folder / "checkpoints" / resnet_name
facebank_path = data_folder / facebank_name

deepPix_checkpoint_path = data_folder / "checkpoints" / deeppix_name

faceDetector = FaceDetection()
identityChecker = IdentityVerification(
    checkpoint_path=resNet_checkpoint_path.as_posix(),
    facebank_path=facebank_path.as_posix(),
)
livenessDetector = LivenessDetection(checkpoint_path=deepPix_checkpoint_path.as_posix())

app = Flask(__name__)




@app.route("/liveness", methods=["POST"])
def liveness():
    t1 = time.time()

    data = request.get_json()
    base64_data = data['image']
    decoded_image = base64.b64decode(base64_data)
    nparr = np.frombuffer(decoded_image, np.uint8)


    LIVENESS_TRESHOLD = 0.8


    # decode image
    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    faces, boxes = faceDetector(frame)

    if not len(faces):
        response = {
            'status' :3,
            'data' : 'No face detected!'
        }
        status_code = 200

    elif len(faces) > 1:
        response = {
            'status' : 2,
            'data' : 'Multiple face detected!'
        }
        status_code = 200

    else:
        face_arr = faces[0]
        liveness_score = livenessDetector(face_arr)
        liveness = float(liveness_score.item())
        if liveness > LIVENESS_TRESHOLD:
            response = {'status' : 0}

        else:
            response = {'status' : 1}
           
        status_code = 200
    
    print({'response' : response, 'status_code' : status_code, 'time' : time.time() - t1})
    return jsonify(response), status_code

if __name__ == "__main__":
    run()
