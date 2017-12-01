'''
map the raw data into wiki_trusts.txt (src,tgt,sign) and wiki_comments.txt(src,tgt,comment)
'''
import json
import re
import random

positive_sample_ratio=0.3 # make 1.0 for complete
max_node_id=500 #max is about 12000
wiki_dir="wiki/"

suffix="_"+str(max_node_id)+"_"+str(positive_sample_ratio)

# suffix=""

wikirfa_file=wiki_dir+"wiki-rfa-original.txt"
name2id_file=wiki_dir+"name2uniq_id.json"

knows_file=wiki_dir+"wiki_knows"+suffix+".txt"
trusts_file=wiki_dir+"wiki_trusts"+suffix+".txt"
senti_train_file=wiki_dir+"senti_train"+suffix+".txt"
senti_train_no_id_file=wiki_dir+"senti_train_no_ids"+suffix+".txt"


original=open(wikirfa_file,"r")
knows=open(knows_file, 'w')
trusts=open(trusts_file, 'w')
senti_train=open(senti_train_file, 'w')
senti_train_no_id=open(senti_train_no_id_file, 'w')

d = json.load(open(name2id_file))

src = ""
tgt = ""
vote = ""
txt=""
record_ready=False

records_seen=0
pos=0
neg=0

visited=set()
for line in original:
    line = line.strip('\n')
    words = line.split(":")
    if len(words)<=1:
        continue
    if words[0]=="SRC":
        # if words[1]:
        src=d[words[1]]
        # else:
        #     print("in else")
        #     src=d[""] #394
        # src=str(d[words[1].decode('utf-8')])
    elif words[0]=="TGT":
        tgt=d[words[1]]
        # tgt=str(d[words[1].decode('utf-8')])
    elif words[0]=="VOT":
        vote=words[1]
    elif words[0]=="TXT":
        txt=words[1]
        matchObj = re.search(r'\'\'\'(.*)\'\'\'(.*)', txt, flags=0)  # remove "support/oppose" word in comments
        if matchObj:
            senti_text=matchObj.group(2)
        else:
            senti_text=txt
        record_ready=True
    #only chose first obtained relation sentiment?? | ignore
    if record_ready and src and tgt and ((str(src)+':::'+str(tgt)) not in visited):
        if vote!='0':    # remove neutral signs
            # print (src," - ",tgt, " : ",senti_text)
            if int(src)<max_node_id and int(tgt)<max_node_id:    # sample only 1000 users from all users
                src=str(src)
                tgt=str(tgt)
                if vote=='1': #knows and trusts
                    if random.random() < positive_sample_ratio:   # sample a certain number of postive labels
                        trusts.write(src+'\t'+tgt+'\t'+'1'+'\n')
                        knows.write(src+'\t'+tgt+'\t'+'1'+'\n')
                        senti_train.write(src+':::'+tgt+':::'+vote+':::'+senti_text+'\n')
                        senti_train_no_id.write(vote+':::'+senti_text+'\n')
                        visited.add( src+':::'+tgt)
                        pos=pos+1
                else: # neg opinions = knows and doesn't trust
                    trusts.write(src+'\t'+tgt+'\t'+'0'+'\n')
                    knows.write(src+'\t'+tgt+'\t'+'1'+'\n')
                    senti_train.write(src+':::'+tgt+':::'+vote+':::'+senti_text+'\n')
                    senti_train_no_id.write(vote+':::'+senti_text+'\n')
                    visited.add( src+':::'+tgt)
                    neg=neg+1
        src = ""
        tgt = ""
        vote = ""
        txt=""
        record_ready=False
        records_seen=records_seen+1
        if records_seen%5000==0:
            print ("processed - ",records_seen," records")

total=pos+neg
print ("-------------------------------------")
print("Records seen:{}".format(records_seen))
print("total(pos+neg):{}".format(total))
print("positive labels:{}".format(pos))
print("negative labels:{}".format(neg))
print("N/P ratio:{}".format(neg/float(total)))