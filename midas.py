# midas.py 
# By Chris Clark 9/10/2012
# This is a early version of a program to automatically export to DB and scan
# the metadata from all incoming files. Also compute and tag each with MD5 hash
# for tracking and association.
import exiftool
import os
import sys
import pymongo 
import hashlib
import datetime
import threading
import time

from pymongo import Connection
connection = Connection('localhost', 27017)
db = connection.test
metadatacollection = db.metadata

now = datetime.datetime.now()

if len(sys.argv)<2:
    pathtofiles = os.getcwd()
else:
    pathtofiles = sys.argv[1]

print "Path to be scanned: " +  pathtofiles 

def md5sum(filename):
	md5 = hashlib.md5()
        with open(filename, 'rb') as f:
        	for chunk in iter(lambda: f.read(8192), b''):
 			md5.update(chunk)
	return md5.hexdigest()

def main():
	for root, dirs, files in os.walk(pathtofiles):
    		for name in files: 
       			filename = os.path.join(root, name)
			with exiftool.ExifTool() as et:
		    		metadata = et.get_metadata(filename)

		metadata[u'md5'] = md5sum(filename)
       		metadata[u'DateTimeRecieved'] = now.strftime("%Y:%m:%d %H:%M:%S")
	#   	print metadata.keys()
       		print  metadata
	#	metadatacollection.insert(metadata)
	#       os.remove(filename)

if __name__ == "__main__":
	main()  
