
# """
# Taking images of  employees and saving in a folder, and training for recognition purpose
# """
import csv
import re
import cv2
import os
import mtcnn

#function to check id is interger
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass

    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass

    return False


# Take image function
def takeImages(Id, name):
    """
    :param Id: Id of employee
    :param name: name of employee
    """
    if (is_number(Id)):
        cam = cv2.VideoCapture(0)
        harcascadePath = "haarcascade_frontalface_default.xml"
        detector = cv2.CascadeClassifier(harcascadePath)
        sampleNum = 0

        while (True):
            ret, img = cam.read()
            #img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = detector.detectMultiScale(gray, 1.3, 5, minSize=(30, 30), flags=cv2.CASCADE_SCALE_IMAGE)
            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x + w, y + h), (10, 159, 255), 2)
                # saving the captured face in the dataset folder Faces
                sampleNum = sampleNum + 1
                if not os.path.isdir("Faces/" + str(Id) + "_" + name):
                    os.mkdir("Faces/" + str(Id) +"_"+ name)
                cv2.imwrite("Faces/" + str(Id) + "_" + name + os.sep + name + "." + str(Id) + "."+ str(sampleNum) + ".jpg",gray[y:y + h, x:x + w])

                # display the frame
                cv2.imshow('frame', img)
            # wait for 100 miliseconds
            if cv2.waitKey(100) & 0xFF == ord('q'):
                break
            # break if the sample number is more than 100
            elif sampleNum > 100:
                break
        cam.release()
        cv2.destroyAllWindows()
    row = [Id, name]
    with open("Employee_Details/Employee_Details.csv", "a+") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(row)
    csv_file.close()

"""#######Testing of Taking pictures, it will save pictures in Face database in new folder#########"""
"""Uncomment below lines and run this for taking you pictures sir"""
# id = 10
# name = "Waleed Saleem"
# takeImages(id, name)

id = 10
name = "Yasir Mehmood"
takeImages(id, name)

