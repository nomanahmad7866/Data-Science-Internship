import os
import cv2

from architecture import *
import os
import cv2
import mtcnn
import pickle
import numpy as np
from sklearn.preprocessing import Normalizer
from tensorflow.keras.models import load_model

######paths and vairables#########
face_data = 'Faces/'
required_shape = (160, 160)
face_encoder = InceptionResNetV2()
path = "facenet_keras_weights.h5"
face_encoder.load_weights(path)
face_detector = mtcnn.MTCNN()
encodes = []
encoding_dict = dict()
l2_normalizer = Normalizer('l2')
#############################################################################################
"""This module will train new employee pictures and will  save encoding in pickle file"""
##############################################################################################


def normalize(img):
    mean, std = img.mean(), img.std()
    return (img - mean) / std


def train_me(id, name):
    for face_names in os.listdir("Faces"):
        person_dir = os.path.join("Faces", face_names)
        if str(id) + "_" + name in person_dir:
            direc = person_dir
            print(f"directory of intended person images is {person_dir}")
        else:
            continue

        for image_name in os.listdir(direc):
            image_path = os.path.join(person_dir, image_name)
            #print(f"Here is the person images path {image_path}")
            #print("converting images here to RGB..")
            img_BGR = cv2.imread(image_path)
            img_RGB = cv2.cvtColor(img_BGR, cv2.COLOR_BGR2RGB)
            #print("Detecting faces...")
            x = face_detector.detect_faces(img_RGB)
            x1, y1, width, height = x[0]['box']
            x1, y1 = abs(x1), abs(y1)
            x2, y2 = x1 + width, y1 + height
            face = img_RGB[y1:y2, x1:x2]

            #print("Normalizing faces...")
            face = normalize(face)
            face = cv2.resize(face, required_shape)
            face_d = np.expand_dims(face, axis=0)
            encode = face_encoder.predict(face_d)[0]
            encodes.append(encode)
        #print("lets find encodings here...")
        if encodes:
            encode = np.sum(encodes, axis=0)
            encode = l2_normalizer.transform(np.expand_dims(encode, axis=0))[0]
            #print(f"encodings are {encode}")
            encoding_dict[face_names] = encode

    #print("Saving encoding into pickle file....")
    path = 'encodings/encodings.pkl'
    with open(path, 'wb') as file:
        pickle.dump(encoding_dict, file)
    print("encoding saved")


print("Please wait...your image is being trained")

###################################################################################
#uncomment below lines to train yourself

# before train yourself make sure to take images by running capture images
# id = 11
# name = "Waleed Saleem"
# train_me(id, name)









