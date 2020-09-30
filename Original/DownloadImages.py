from PIL import Image
import os
import json
import requests
import io
import re
import argparse
from google_images_download import google_images_download

parser = argparse.ArgumentParser()
parser.add_argument('keywords_from_file', help='Text file with search terms', type=str)
parser.add_argument('--limit', help='Number of images per term', type=str, required=True)
args = parser.parse_args()

keywords_from_file = os.path.join(os.getcwd(),args.keywords_from_file)
limit = int(args.limit)

## A. Download Images and put them in Downloaded_images

if not os.path.exists("Downloaded_images"):
    os.makedirs("Downloaded_images")

# Note: we can use prefix/suffix keywords
response = google_images_download.googleimagesdownload()
arguments = {"keywords_from_file":keywords_from_file, "limit":limit,"print_urls":True, "extract_metadata":True, "output_directory": os.path.join(os.getcwd(),"Downloaded_images"), "chromedriver": os.path.join(os.getcwd(),"chromedriver.exe")}

absolute_image_paths = response.download(arguments)

## B. Apply corrector

with open(keywords_from_file) as f:
    content = f.readlines()
content = [x.strip() for x in content]

for searchterm in content:
    logs = os.path.join(os.getcwd(),"logs", searchterm+".json")
    folder = os.path.join(os.getcwd(),"Downloaded_images",searchterm)

    with open(logs, encoding='utf-8') as data_file:
        data = json.loads(data_file.read())

    files = sorted(os.listdir(folder), key=lambda y: (int(re.sub('\..*','',y)),y))

    os.chdir(folder)

    for indx, i in enumerate(files):
        try:
            Image.open(i)
        except:
            try:
                os.remove(i)
                response = requests.get(data[indx]["image_link"], timeout=5)
                img = Image.open(io.BytesIO(response.content))
                if img.format=='JPEG':
                    with open(str(indx+1) +".jpg", 'wb') as f:
                        for chunk in response.iter_content(1024):
                          f.write(chunk)
                    print("JPG image corrected: " + indx+1)
                elif img.format=='PNG':
                    with open(str(indx+1) +".png", 'wb') as f:
                        for chunk in response.iter_content(1024):
                            f.write(chunk)
                    print("PNG image corrected: " + indx+1)
                else:
                    print("")
            except:
                print("")
    
    files_c = os.listdir(folder)
    
    for item in files_c:
        if not item.endswith(".jpg") and not item.endswith(".png"):
            os.remove(item)

    os.chdir(os.path.abspath('..'))
    os.chdir(os.path.abspath('..'))