# AVclass-Family-Count-Scripts

This is where the AVclass tool becomes useful for making
the best guess possible at labeling this set of malware (Github
page: https://github.com/malicialab/avclass). Firstly, it is
necessary to generate and/or retrieve the JSON data that
contains the labels from each virus engine on VirusTotal. A
script that generates the reports from VirusTotal would work for this.
Instead of generating an organized report in markdown format,
we dump the JSON data into a JSON file. There is a useful
python library for this called JSON. See the following line of
code:
```
json.dump(json response, fileObject)
```
We simply iterate through the directory containing our
similar malware samples and generate a JSON file based upon
the response from the VirusTotal API (version 2) for each
of them. At this point, it is a simple matter
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
