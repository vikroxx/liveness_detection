import os
from pathlib import Path
import torch
import cv2
from glob import glob
import time
from tqdm import tqdm
from facetools import FaceDetection, IdentityVerification, LivenessDetection
from facetools.utils import visualize_results

root = Path(os.path.abspath(__file__)).parent.absolute()
data_folder = root / "data"

resNet_checkpoint_path = data_folder / "checkpoints" / "InceptionResnetV1_vggface2.onnx"
facebank_path = data_folder / "reynolds.csv"

deepPix_checkpoint_path = data_folder / "checkpoints" / "OULU_Protocol_2_model_0_0.onnx"

faceDetector = FaceDetection(max_num_faces=1)
identityChecker = IdentityVerification(
    checkpoint_path=resNet_checkpoint_path.as_posix(),
    facebank_path=facebank_path.as_posix(),
)
livenessDetector = LivenessDetection(checkpoint_path=deepPix_checkpoint_path.as_posix())


# files =  glob('sample_images/*.jpeg') + glob('sample_images/*.jpg')
files =  glob('teenagers/*.jpg')

# files =  glob('fake/*.jpeg') + glob('fake/*.jpg')

def show_image(frame):
    cv2.namedWindow("image", cv2.WINDOW_NORMAL)  #  2. use 'normal' flag
    h,w = frame.shape[:2]  #  suits for image containing any amount of channels
    resize_factor = 0.3
    h = int(h / resize_factor)  #  one must compute beforehand
    w = int(w / resize_factor)  #  and convert to INT
    cv2.resizeWindow("image", w, h)
    cv2.imshow("image", frame)
    
    # waits for user to press any key
    # (this is necessary to avoid Python kernel form crashing)
    cv2.waitKey(0)
    
    # closing all open windows
    cv2.destroyAllWindows()
    # cap.release()

def detect_liveliness(file):
    frame = cv2.imread(file)
    canvas  = frame.copy()
    t1 = time.time()
    faces, boxes = faceDetector(frame)
    if len(faces) == 1:
        # print(len(faces))
        # print((faces[0]))
            # print(len(faces))
        for face_arr, box in zip(faces, boxes):
            # min_sim_score, mean_sim_score = identityChecker(face_arr)
            liveness_score = livenessDetector(face_arr)
            print(liveness_score)
            # canvas = visualize_results(canvas, box, liveness_score, mean_sim_score)
            print((time.time() - t1)*1000)
    else:
        print('NO FACE FOUND')

# print(files)
for file in tqdm(files):
    frame = cv2.imread(file)
    canvas  = frame.copy()
    t1 = time.time()
    faces, boxes = faceDetector(frame)
    if len(faces) == 1:
        # print(len(faces))
        # print(len(faces))
        # print(type(faces[0]))
        # show_image(faces[0])
        faces[0] = cv2.resize(faces[0], (150,150))
        cv2.imwrite('cropped_images/{}'.format(os.path.basename(file)), faces[0])
        # print(boxes[0])
        # for face_arr, box in zip(faces, boxes):
        #     # min_sim_score, mean_sim_score = identityChecker(face_arr)
        #     liveness_score = livenessDetector(face_arr)
        #     print(liveness_score)
        #     # canvas = visualize_results(canvas, box, liveness_score, mean_sim_score)
        #     print((time.time() - t1)*1000)
    else:
        print('NO FACE FOUND')
    
    
    

