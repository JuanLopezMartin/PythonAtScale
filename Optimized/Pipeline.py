import os
import sys

keywords_from_file = str(sys.argv[1])

os.system("python DownloadImages.py " + keywords_from_file)
os.system("python -W ignore CropFaces.py " + keywords_from_file)
os.system("python -W ignore DetectGender.py " + keywords_from_file)
