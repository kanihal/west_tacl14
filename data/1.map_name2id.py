#  get the map function file from SRC/TGT name to unique id
import json
import csv
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-i","--input_file",
                    default=None,
                    help="/path/to/wikirfa_file")
# parser.add_argument("--output_file",
# 					default=None,
# 					help="/path/to/output_file")

args = parser.parse_args()

print("Reading file -"+args.input_file)
input_file=args.input_file
with open(input_file,"r") as f1 :
    i=0
    count=0
    d=dict()

    for line in f1:
        line = line.strip('\n')
        words = line.split(":")
        if len(words)<=1:
            continue

        if (words[0]=="SRC" or words[0]=="TGT"):

            if words[1] not in d:
                count=count+1
                d[words[1]]=count
            

print("Writing to files...")
json.dump(d, open("./wiki/name2uniq_id.json",'w'))
with open('./wiki/name2uniq_id.csv', 'w') as f:
    w = csv.writer(f)
    for key,value in zip(list(d.keys()),list(d.values())):
        w.writerow([key,value])
print("number of unique user: "+str(count))