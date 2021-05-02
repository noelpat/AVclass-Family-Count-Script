# This program is designed to iterate through files in the working directory and
# scan the executable files and check for matching ELF hashes to get malware family pairs
# that can be used to create YARA Rules with a tool such as AutoYara.
# This script will write the sha256 hash for a file next to its respective TLSH hash 
# in a text file named: tlshPairs.txt
# Reference: https://stackoverflow.com/questions/10377998/how-can-i-iterate-over-files-in-a-given-directory
# Reference: https://cmdlinetips.com/2014/03/how-to-run-a-shell-command-from-python-and-get-the-output/

import subprocess
import os
from subprocess import Popen, PIPE
import time
import shutil
import hashlib

# Possible additional features could be added to this script matching elf hashes...
def get_tlsh(directory):
	tlshData = open("tlshPairs.txt", "a")
	for file in os.listdir(directory):
		elfHash = ""
		# total = total + 1
		filename = os.fsdecode(file)
		# print("Value of file:", file)
		# print("Value of filename:", filename)
		# print("Value of directory:", directory)

		realLocation = directory+filename
		out = subprocess.Popen(['file', realLocation],
			stdout=subprocess.PIPE,
			stderr=subprocess.STDOUT)

		stdout,stderr = out.communicate()

		# query the Virus Total API to find matching elf pairs
		if b'executable' in stdout:
			print("Executable found:", filename)
			# print("Value of realLocation:", realLocation)
			sha256_returned = hashlib.sha256(open(realLocation,'rb').read()).hexdigest()
			#print("Value of sha256_returned:", sha256_returned)

			pipe = Popen("curl --request GET --url https://www.virustotal.com/api/v3/files/"+sha256_returned+" --header 'x-apikey: your-v3-api-key-here' | grep tlsh", shell=True, stdout=PIPE)

			for line in pipe.stdout:
				current = str(line).split() # split string value by spaces
				# print("Value of current:", current)
				tlshHash = current[2][:-4] # get the TLSH hash from VT response
				# print("Value of tlshHash:", tlshHash)
				# strip the quotes before writing
				tlshHash = tlshHash.strip('"')
				tlshData.write(sha256_returned+":"+tlshHash+"\n")
	tlshData.close()

def main():
	# newDir = ["Cowrie-2021-03-15"] # DEBUG 
	# newDir = [] # Keep track of new directories created for extraction/scanning
	"""
	for file in os.listdir('.'):
		# totalFiles = totalFiles + 1
		if os.path.isdir(file) and file != "Malware.Backups":
			newDir.append(str(file))
	"""
	# print("Value of newDir:", newDir) # DEBUG
	# Set directory/locations for extracted files and new malware samples
	# directory = "/data/cowrie/downloads/" # This is usually where Cowrie archives extrac
	# destination = '/newSamples/' # This folder was created for malware samples not in the VT database.
	# yaraDir = '/YARA.unid/'
	get_tlsh("./Malware.Backups/300.days/") # Set your target directory containing malware samples to compare here.

if __name__ == "__main__":
	main()
