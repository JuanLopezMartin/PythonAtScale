from google_images_download import google_images_download
import os
from PIL import Image
import imghdr



def DownloadImagesFunction(term):
    response = google_images_download.googleimagesdownload()
    arguments = {"keywords":term, "limit":500,"print_urls":True, "extract_metadata":True, "output_directory": os.path.join(os.getcwd(),"Downloaded_images"), "chromedriver": os.path.join(os.getcwd(),"chromedriver.exe")}
    response.download(arguments)
    
    ##B. Apply corrector

    # folder = os.path.join(os.getcwd(),"Downloaded_images",term)   
    # files_c = os.listdir(folder)
    # files_c = [folder + '\\' + s for s in files_c]
    
    # for item in files_c:
    #     try:
    #         if not imghdr.what(item) in ["jpg", "jpeg", "png"]:
    #             im = Image.open(item)
    #             filename, extension = os.path.splitext(item)
    #             im.save(folder + '\\' + filename + 'corrected' + '.jpg')
    #     except:
    #         os.remove(item)