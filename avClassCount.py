# This script is designed to iterate through a given directory of JSON log files
# generated from the VirusTotal API v2 and use the AVclass python script to find
# the respective malware label. 

import os
from subprocess import Popen, PIPE

def main():
  labels = []
  total = 0

  for file in os.listdir('.'):
    if file != "jsonErrors.txt" and file != "avClassCount.py":
      pipe = Popen("python3 /avclass-master/avclass/avclass_labeler.py -vt "+file, shell=True, stdout=PIPE)
      total += 1

      for line in pipe.stdout:
        current = str(line).split('\\')
        labels.append(current[1][1:])

  # print(labels)

  # Get unique values from labels
  unique_list = []
  for x in labels:
    if x not in unique_list:
      unique_list.append(x)
      unique_list.append(0)

  # convert the unique_list to a dictionary for counting the files
  # print(unique_list)
  it = iter(unique_list)
  res_dct = dict(zip(it, it))
  #print(res_dct)

  # Find the counts
  for i in unique_list:
    for j in labels:
      if i == j:
        # print("i was equal to j!")
        res_dct[i] = res_dct[i] + 1

  print(res_dct)
  print("Total files checked:", total)

if __name__ == "__main__":
  main()
