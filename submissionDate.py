# This program is designed to iterate through files in the working directory and
# scan the executable files and check if the submission date to VirusTotal was
# more than 300 days ago via the VirusTotal API v3. After doing so, the
# files can be sorted by their submission date.
# This script is designed to work with directories created by CowrieScan.py:
# https://github.com/noelpat/Cowrie-Honeypot-Data-Collection-Scripts/blob/main/CowrieScan.py

# Reference: https://www.youtube.com/watch?v=EgLNmG2LzTI
# Reference: https://stackoverflow.com/questions/10377998/how-can-i-iterate-over-files-in-a-given-directory
# Reference: https://cmdlinetips.com/2014/03/how-to-run-a-shell-command-from-python-and-get-the-output/
# Reference: https://www.geeksforgeeks.org/python-program-to-merge-two-files-into-a-third-file/

import subprocess
import os
from subprocess import Popen, PIPE
import time
import shutil
import hashlib

def backup_malware(directory):
	day300 = int('1592092800') # 300 days ago
	tStamp = int('0') # will be updated with timestamp of current file(s)

	for file in os.listdir(directory):
		# total = total + 1
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
			pipe = Popen("curl --request GET --url https://www.virustotal.com/api/v3/files/"+sha256_returned+" --header 'x-apikey: your-api-key' | grep first_submission_date", shell=True, stdout=PIPE)

			for line in pipe.stdout:
				current = str(line).split() # split string value by spaces
				tStamp = int(current[2][:-4]) # get the UTC timestamp from current array

			# print(tStamp)
			# Compare the files first submission date to day 300
			# Check if it is a negative number or not
			if tStamp - day300 < 0:
				print("File submitted more than 300 days ago:", realLocation)
				# Copy file to the 300 day old back up directory
				shutil.copy2(realLocation, "./Malware.Backups/300.days/"+str(filename))
			else:
				print("Added to young.files directory:", realLocation)
				shutil.copy2(realLocation, "./Malware.Backups/young.samples/"+str(filename))

def sort_by_date(newDir, directory, destination, yaraDir):
	oldDir = directory

	for i in newDir:
		directory = i+oldDir
		dest = i+destination
		yara = i+yaraDir
		
		if os.path.exists(directory):
			backup_malware(directory)
		else:
			print("No cowrie data download data found in", directory)
			
		if os.path.exists(dest):
			backup_malware(dest)
		else:
			print("No path found for newsamples in", i)
			
		if os.path.exists(yara):
			backup_malware(yara)
		else:
			print("No path found for YARA unids in", i)

def main():
  # Create directory for moving the malware samples.
  exist = os.path.isdir("Malware.Backups")
  
  if exist != True:
    try:
      os.mkdir("Malware.Backups")
    except:
      print("Failed to create directory for malware samples")
      print("Check your permissions?")
      print("Exiting...")
      exit()
  
	# newDir = ["Cowrie-2021-03-15"] # DEBUG 
	newDir = [] # Keep track of new directories created for extraction/scanning
	
	for file in os.listdir('.'):
		# totalFiles = totalFiles + 1
		if os.path.isdir(file) and file != "Malware.Backups":
			newDir.append(str(file))
	
	# print("Value of newDir:", newDir) # DEBUG
  # Make sure these directories exist before running the program...
	# Set directory/locations for extracted files and new malware samples
	directory = "/data/cowrie/downloads/" # This is usually where Cowrie archives extract
	destination = '/newSamples/' # This folder was created for malware samples not in the VT database.
	yaraDir = '/YARA.unid/' # Folder created by the CowrieScan.py script
	sort_by_date(newDir, directory, destination, yaraDir)

if __name__ == "__main__":
	main()
