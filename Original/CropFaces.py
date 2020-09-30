import cv2
import face_recognition
from face_recognition.api import _raw_face_landmarks
import argparse
import os
from tqdm import tqdm

parser = argparse.ArgumentParser()
parser.add_argument('keywords_from_file', help='Text file with search terms', type=str)
args = parser.parse_args()

keywords_from_file = os.path.join(os.getcwd(),args.keywords_from_file)

with open(keywords_from_file) as f:
    content = f.readlines()
content = [x.strip() for x in content]

for searchterm in tqdm(content):
    imagefolder = os.path.join(os.getcwd(),"Downloaded_images",searchterm)
    targetfolder = os.path.join(imagefolder, "Cropped_faces")

    if not os.path.exists(targetfolder):
            os.mkdir(targetfolder)

    for image_path in tqdm(os.listdir(imagefolder)):
        try:
            image = face_recognition.load_image_file(os.path.join(imagefolder, image_path))
            face_locations = face_recognition.face_locations(image)
            img = cv2.imread(os.path.join(imagefolder, image_path))
            height, width, channels = img.shape

            for index in range(0,len(face_locations)):
                x = face_locations[index][0]-50
                y = face_locations[index][1]+30
                w = face_locations[index][2]+30
                h = face_locations[index][3]-30
                if x < 0:
                    x = 0
                if w > height:
                    w = height
                if h < 0:
                    h = 0
                if y > width:
                    y = width
        
                sub_face = img[x:w, h:y]

                targetfile = targetfolder + "/" + image_path[:-4] + "_" + str(index) + ".jpg"
                cv2.imwrite(targetfile, sub_face)
                try:
                    face_landmarks = _raw_face_landmarks(sub_face)
                    landmarks_as_tuples = [[(p.x, p.y) for p in face_landmarks.parts()] for face_landmarks in face_landmarks]
                    fh = open(targetfile[:-4] + ".txt","w")
                    for p in landmarks_as_tuples[0]:
                        fh.write(str(p[0]) + " " + str(p[1]) + "\n")
                    fh.close()
                except:
                    #print("")
                    pass
        except:
            #print("Error; image not cropped:" + image_path)
            pass
    #print("Succesfully croped" + image_path)

