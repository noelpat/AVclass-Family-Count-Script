# AVclass-Family-Count-Scripts

The AVclass tool is useful for making
the best guess possible at labeling a set of malware (Github
page: https://github.com/malicialab/avclass). Firstly, it is
necessary to generate and/or retrieve the JSON data that
contains the labels from each virus engine on VirusTotal. A
script that generates the reports from VirusTotal would work for this.
By using the generateJSON.py script here you can dump the JSON data 
into a JSON file. There is a useful python library for this called 
JSON. See the following line of code:
```
json.dump(json response, fileObject)
```
We simply iterate through the directory containing our
similar malware samples and generate a JSON file based upon
the response from the VirusTotal API (version 2) for each
of them (See generateJSON.py). At this point, it is a simple matter
to analyze each of these generated JSON files to verify that
they do indeed all belong to the same family (or have the
same malware label). However, it seems the AVclass tool can
only check multiple JSON reports at the same time was if all
of the JSON files were combined. I tried to combine JSON
files automatically with my python script and the AVclass
tool/script did not want to work with the combined JSON file
generated. To work around this, I made another short python
script (avClassCount.py) that could run the AVclass tool individually against every
JSON file in a given directory using the following command:
```
python3 avclass labeler.py -vt file
```
The -vt option indicates that the input file is a JSON
response from VirusTotal v2. If the AVclass tool agrees that all
the malware samples in the given directory (submitted more
than 300 days) are the same, then we can use that as a label
for generating a YARA rule with a tool such as AutoYara.

# Organize by VirusTotal Submission Date

You may want to organize the malware samples between those submitted more than 300 days to the VirusTotal database and those that were not due to label stability (See: https://www.usenix.org/conference/usenixsecurity20/presentation/zhu). This script creates a directory called "Malware.Backups" in the same directory where it is ran. This python script relies upon the following command to check the submission date via the VirusTotal API v3:

```
curl --request GET --url 
https://www.virustotal.com/api/v3/files/"+sha256+" --header 'x-apikey: your-api-key' | grep first_submission_date
```

When using this command, VirusTotal returns the first submission date in UTC time format. So it is necessary to either convert that time or interpret it within the python script while sorting by the date. Since I stopped data collection on April 10th, 2021 for this study I used June 14, 2020 as the benchmark for whether or not a file was submitted more than 300 days ago. I retrieved the UTC timestamp for June 14th, 2020 from the website epochconvert.com, and I used that to find out if files were submitted before that date. To demonstrate this, see the code below:

```
# Check if it is a negative number or not
if tStamp - day300 < 0:
	# File submitted more than 300 days ago
	# Copy file to 300 day old directory
	shutil.copy2(realLocation, "./Malware.Backups/300.days/"+str(filename))
else:
	# Add to the young files dir
	shutil.copy2(realLocation, "./Malware.Backups/young.samples/"+str(filename))
```

The script will iterate through sub directories for each individual day and check each executable file with the VirusTotal API and the logic above to separate/copy the files to organized directories for further analysis with the other scripts.
