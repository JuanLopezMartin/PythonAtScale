import multiprocessing
import argparse
import os
import DetectGenderFunction

if __name__ == '__main__':

  argument_parser = argparse.ArgumentParser()
  argument_parser = argparse.ArgumentParser(description='Detect Gender')
  argument_parser.add_argument('keywords_from_file', metavar='folder', type=str, help='keywords_from_file')
  args = argument_parser.parse_args()

  if not os.path.exists("Datasets"):
      os.makedirs("Datasets")

  keywords_from_file = os.path.join(os.getcwd(),args.keywords_from_file)

  with open(keywords_from_file) as f:
      content = f.readlines()
  content = [x.strip() for x in content]
  chunks = [content[x:x+4] for x in range(0, len(content), 4)]
  pool = multiprocessing.Pool(4)

  for i in range(len(chunks)):
      pool.map(DetectGenderFunction.DetectGenderFunction, chunks[i])
