import os
from pathlib import Path
import torch
import cv2
from glob import glob
import time
import multiprocessing

from facetools import FaceDetection, IdentityVerification, LivenessDetection
from facetools.utils import visualize_results



def process_file(file, faceDetector, livenessDetector):
    frame = cv2.imread(file)
    canvas  = frame.copy()
    t1 = time.time()
    faces, boxes = faceDetector(frame)
    if len(faces) == 1:
        print(len(faces))
        for face_arr, box in zip(faces, boxes):
            liveness_score = livenessDetector(face_arr)
            print(liveness_score)
            print((time.time() - t1)*1000)
    else:
        print('NO FACE FOUND')

def main():

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

    files =  glob('sample_images/*.jpeg') + glob('sample_images/*.jpg')

    with multiprocessing.Pool() as pool:
        for file in files:
            pool.apply_async(process_file, args=(file, faceDetector, livenessDetector))

        pool.close()
        pool.join()



if __name__ == '__main__':
    main()
    