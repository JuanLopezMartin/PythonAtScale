import multiprocessing
import DownloadImagesFunction
import argparse
import os


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('keywords_from_file', help='Text file with search terms', type=str)
    args = parser.parse_args()

    keywords_from_file = os.path.join(os.getcwd(),args.keywords_from_file)
    with open(keywords_from_file) as f:
        content = f.readlines()
    content = [x.strip() for x in content]

    if not os.path.exists("Downloaded_images"):
        os.makedirs("Downloaded_images")

    chunks = [content[x:x+1] for x in range(0, len(content), 1)]
    pool = multiprocessing.Pool(1)

    for i in range(len(chunks)):
        pool.map(DownloadImagesFunction.DownloadImagesFunction, chunks[i])