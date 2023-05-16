import cv2 
import numpy as np
import mtcnn
import keras
import os
import pandas as pd
import time
import datetime
import csv
from Mark_Attendance import Mark_attendance_here
from encoding_unknowns import  encode_unknown

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
from architecture import *
from Train_Employees import triplet_loss
#from train_v2 import normalize,l2_normalizer
from scipy.spatial.distance import cosine
from tensorflow.keras.models import load_model
import pickle
from sklearn.preprocessing import Normalizer
l2_normalizer = Normalizer('l2')

from datetime import datetime
now = datetime.now()
current_time = now.strftime("%H:%M:%S")


confidence_t=0.99
recognition_t=0.5
required_size = (160,160)

###########################  Function to Normalize Input Faces###################################
def normalize(img):
    mean, std = img.mean(), img.std()
    return (img - mean) / std

#################################################################################################

"""Function To Extract Face From Image"""
def get_face(img, box):
    x1, y1, width, height = box
    x1, y1 = abs(x1), abs(y1)
    x2, y2 = x1 + width, y1 + height
    face = img[y1:y2, x1:x2]
    return face, (x1, y1), (x2, y2)
##################################################################################################

"""Function to Find Encodings of Images"""

def get_encode(face_encoder, face, size):
    """

    :param face_encoder: inception encoder classifier
    :param face: detected face
    :param size: recquired size
    :return: encodings of image
    """
    face = normalize(face)
    face = cv2.resize(face, size)
    encode = face_encoder.predict_on_batch(np.expand_dims(face, axis=0))[0]
    return encode
########################################################################################################

"""Function To load pickle file of encodings from Disk"""
def load_pickle(path):
    """

    :param path: path to pickle file
    :return: dictionary of encodings
    """
    with open(path, 'rb') as f:
        encoding_dict = pickle.load(f)
    return encoding_dict
#########################################################################################################

# """Function to Find Time Range for Attendance Purpose"""
# def time_in_range(start, end, x):
#     """
#     :param start: starting office time of JMM
#     :param end: Office Leaving time of JMM
#     :param x: current time
#     :return: Return true if x is in the range [start, end]
#     """
#
#     if start <= end:
#         return start <= x <= end
#     else:
#         return start <= x or x <= end
######################################################################################################

"""Main Function to do all stuff for face recognition and marking attendance"""

def Face_Recognition(img ,detector,encoder,encoding_dict):
    """

    :param img: input image from webcam
    :param detector: face detector for detecting faces from an image
    :param encoder: inception model classifier to recognize faces
    :param encoding_dict: encoding dictionary which contain employee images encoding algong with their name
    :return: return predicted image
    """

    #for attendance, initializing columns
    col_names = ['Id', 'Name', 'Time_In', 'Time_Out']
    attendance = pd.DataFrame(columns=col_names)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = detector.detect_faces(img_rgb)
    for res in results:
        if res['confidence'] < confidence_t:
            continue
        face, pt_1, pt_2 = get_face(img_rgb, res['box'])
        encode = get_encode(encoder, face, required_size)
        encode = l2_normalizer.transform(encode.reshape(1, -1))[0]
        name = 'unknown'
        count = 0
        distance = float("inf")

        for db_name, db_encode in encoding_dict.items():
            dist = cosine(db_encode, encode)
            #print(f"what cosine distance does is here: {dist}")

            if dist < recognition_t and dist < distance:
                nam = db_name
                temp = nam.split("_")
                id = temp[0]
                id = str(id)
                name = temp[1]
                bb = str(name)
                #print(f"id of {name} is {id}")
                distance = dist
                id_name = str(id) + "_" + name
                #marking attendance here
                Mark_attendance_here(id, name)
                print("Attendance marked successfully..")

        if name == 'unknown':
            Id = "Unknown"
            bb = str(Id)
            unknown_encodings = encode_unknown(img)
            #will complete this later for saving unknown

        else:
            cv2.rectangle(img, pt_1, pt_2, (0, 255, 0), 2)
            cv2.putText(img, name + f'{"__weocome here"}', (pt_1[0], pt_1[1] - 5), cv2.FONT_HERSHEY_SIMPLEX, 1,
                        (0, 200, 200), 2)
           # cv2.imwrite("Known Employees/" + "Known" + "_" + name +   ".jpg",img)

    return img

###################################################################################################
######################
"""Main Function"""  #
######################

if __name__ == "__main__":
    required_shape = (160,160)
    face_encoder = InceptionResNetV2()
    path_m = "facenet_keras_weights.h5"
    face_encoder.load_weights(path_m)
    print("start execution...")
    encodings_path = 'encodings/encodings.pkl'
    face_detector = mtcnn.MTCNN()
    print("loading encoding pickle file...")
    encoding_dict = load_pickle(encodings_path)

    #face_encoder.save("model_inception.h5")
    # print("model saved on disk")
    #print("loading model from disk...")
    #face_encoder = keras.models.load_model("model_inception.h5")
    #print(f"model loaded successfully")
    print("compiling model....")
    face_encoder.compile(optimizer='adam', loss=triplet_loss, metrics=['accuracy'])
    print("Model has been Compiled....")
    #print(face_encoder.summary())

    print("starting webcam...")
    cap = cv2.VideoCapture(0)

    while cap.isOpened():
        ret,frame = cap.read()
        
        frame= Face_Recognition(frame , face_detector , face_encoder , encoding_dict)

        cv2.imshow('camera', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break