
__author__ = "fannie"
__date__ = "$12 Apr 2016 11:50:33 AM$"

'''
This small application is used for finding duplicate files in any given directory
'''

import sys
import os
import hashlib
import logging

def log_data(path_to_files, founddup):
  logging.basicConfig(level=logging.DEBUG, 
  format='\n%(asctime)s \n%(message)s\n', 
  filename='log.txt',
  datefmt='%Y/%m/%d %H:%M',
  filemode='w')
  logging.debug("%s duplicate to %s" % (path_to_files, founddup))
            
def compare_data_in_files(fobj, chunk_size=1024):
    """Generator that reads a file in chunks of bytes"""
    while True:
        chunk = fobj.read(chunk_size)
        if not chunk:
            return
        yield chunk

def perfom_process_check(paths, hash=hashlib.sha1):
    hashes = {}
    for path in paths:
        for dirpath, dirnames, filenames in os.walk(path):
            for filename in filenames:
                path_to_files = os.path.join(dirpath, filename)
                hashobj = hash()
                for chunk in compare_data_in_files(open(path_to_files, 'rb')):
                    hashobj.update(chunk)
                file_id = (hashobj.digest(), os.path.getsize(path_to_files))
                founddup = hashes.get(file_id, None)
                if founddup:
                  log_data(path_to_files,founddup)
                  os.system('clear')
                  os.system('cat log.txt')
                else:
                  hashes[file_id] = path_to_files
                  
if __name__ == "__main__":
  os.system('clear')
  if sys.argv[1:]:
    directory_to_analyse = sys.argv[1:] #Specify either duplicates of nonduplicates as argument
    perfom_process_check(directory_to_analyse)
  else:
    print '''
    Run either by typing: 
    "python analysedirectory nonduplicates" or
    "python analysedirectory duplicates"
    '''
