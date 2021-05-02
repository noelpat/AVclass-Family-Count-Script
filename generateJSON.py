# This program is designed to iterate through files in the working directory and
# retrieve the JSON response from the VirusTotal API v2. It then dumps the response
# into respective JSON files for further analysis.
# NOTE: You need to add your own VirusTotal API key on Line 44.

# Reference: https://www.youtube.com/watch?v=EgLNmG2LzTI
# Reference: https://stackoverflow.com/questions/10377998/how-can-i-iterate-over-files-in-a-given-directory
# Reference: https://cmdlinetips.com/2014/03/how-to-run-a-shell-command-from-python-and-get-the-output/
# Reference: https://www.geeksforgeeks.org/python-program-to-merge-two-files-into-a-third-file/

import subprocess
import os
import stat
import errno
import sys
from io import StringIO
import shutil
import requests
import hashlib
import time
from time import sleep
import tarfile
from ftplib import FTP
import datetime
from datetime import date
from datetime import timedelta
import csv
from collections import Counter
import json

def Check_malware(directory):
	# Create directory for storing json files
	try:
		os.mkdir(directory+"jsonFiles")
	except:
		print("jsonFiles directory already exists")
	
	jsonDest = directory+"jsonFiles"
	
	# Parameters for checking against virustotal API
	params = {'apikey': 'your-api-key', 'resource': 'hashGoesHere!'}
	headers = {"Accept-Encoding": "gzip, deflate","User-Agent" : "gzip, My Python requests library example client or username"}

	# directory = i+oldDir
	print("Scanning files in directory:", directory)

	# Check file hashes with the virus total API.
	print("Checking the executable files against virus total.")

	with open(jsonDest+'/jsonErrors.txt', 'w') as outfile:
		for file in os.listdir(directory):
			filename = os.fsdecode(file)
			# print("Value of file:", file)
			print("Value of filename:", filename)
			# print("Value of directory:", directory)
			
			realLocation = directory+filename
			out = subprocess.Popen(['file', realLocation],
				stdout=subprocess.PIPE,
				stderr=subprocess.STDOUT)

			stdout,stderr = out.communicate()

			if b'executable' in stdout:
				sha256_returned = hashlib.sha256(open(realLocation,'rb').read()).hexdigest()
				# print(sha256_returned)
				
				params['resource'] = sha256_returned

				#response = requests.get('https://www.virustotal.com/vtapi/v2/file/report', params=params, headers=headers)
				response = requests.get('https://www.virustotal.com/vtapi/v2/file/report', params=params).json()
				
				json_response = ''
				#if 'json' in response.headers.get('Content-Type'):
				json_response = response
				#json_response = response.json()
				# print(json_response)

				if json_response['response_code'] == 0 and b'Python' not in stdout:
					print("File not found in VT db:", filename)
				elif json_response['response_code'] == 1:
					# Write json response to json file
					with open(jsonDest+"/"+filename+".json", "a") as fileObject:
						# fileObject.write(str(json_response))
						json.dump(json_response, fileObject)
					
					# Code below creates 1 minute delay for virus total api
					# Uncomment the code below if using a non-premium API key
					#if exe != 0 and exe % 3 == 0:
						#print("sleeping for 60 seconds...")
						#sleep(65)

def main():
	Check_malware("./Malware.group.dir/")
	# combine_files("./Malware.Backups/300.days/jsonFiles/")

if __name__ == "__main__":
	main()
