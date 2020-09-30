import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sys
import caffe
import argparse
from tqdm import tqdm

argument_parser = argparse.ArgumentParser()
argument_parser = argparse.ArgumentParser(description='Detect Gender')
argument_parser.add_argument('keywords_from_file', metavar='folder', type=str, help='keywords_from_file')
argument_parser.add_argument('--cnnfolder', metavar='cnn_folder', type=str, help='cnn_folder')
args = argument_parser.parse_args()

if not os.path.exists("Datasets"):
    os.makedirs("Datasets")


cnnfolder = os.path.join(os.getcwd(),args.cnnfolder)

mean_filename =  os.path.join(cnnfolder, 'mean.binaryproto')
proto_data = open(mean_filename, "rb").read()
a = caffe.io.caffe_pb2.BlobProto.FromString(proto_data)
mean  = caffe.io.blobproto_to_array(a)[0]

gender_net_pretrained= os.path.join(cnnfolder, 'gender_net.caffemodel')
gender_net_model_file= os.path.join(cnnfolder, 'deploy_gender.prototxt')
gender_net = caffe.Classifier(gender_net_model_file, gender_net_pretrained,
                       mean=mean,
                       channel_swap=(2,1,0),
                       raw_scale=255,
                       image_dims=(256, 256))

keywords_from_file = os.path.join(os.getcwd(),args.keywords_from_file)

with open(keywords_from_file) as f:
    content = f.readlines()
content = [x.strip() for x in content]

for keyword in tqdm(content):

  images_path = os.path.join("Downloaded_images", keyword, "Cropped_faces")

  # Remove .txt from list of files in directory
  lst = os.listdir(images_path)
  os.listdir(images_path)
  for string in lst:
      if string[-4:] == ".txt":
          lst.remove(string)

  # Empty dataframe
  df = pd.DataFrame([])

  # Populate dataframe
  for image_path in tqdm(lst):
      try:
          image_path = os.path.join(images_path, image_path)
          input_image = caffe.io.load_image(image_path)
          prediction = gender_net.predict([input_image]) 
          #print(input_image.shape)
          df = df.append(pd.DataFrame({'file':image_path, 'PFemale':prediction[0,1], 'EAge':"None", 'height':input_image.shape[0], 'width':input_image.shape[1]}, index=[0]))
      except:
          print("Error for " + image_path)

  df.to_csv('Datasets/' + keyword + ".csv")