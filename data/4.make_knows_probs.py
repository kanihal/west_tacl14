'''
Usage : python3 make_knows_probs.py <trust_file> <sent_results>
'''
import sys,os
import random
in_file=sys.argv[1]
senti_results=sys.argv[2]
nr=sys.argv[3]


file=open(in_file,'r')
name = os.path.splitext(os.path.basename(in_file))[0]
in_dir = os.path.splitext(os.path.dirname(in_file))[0]

in_dir=in_dir+"/train/"
trusts=open(in_dir+"wiki_trusts.txt."+nr,'w')
trusts_l=open(in_dir+"wiki_trusts.txt."+nr+".l",'w')
visualize=open(in_dir+"wiki_vis.txt."+nr,'w')
knows=open(in_dir+"wiki_knows.txt."+nr,'w')
probs=open(in_dir+"wiki_lexicon_probs.txt."+nr,'w')

senti_file=open(senti_results,"r")
d={}
for line in senti_file:
    line = line.strip('\n')
    words = line.split("\t")
    if len(words)<=1:
        continue
    else:
        src=words[0]
        dst=words[1]
        p=words[2]
        d[src+":::"+dst]=float(p)
print("dictionary length",len(d))

for line in file:
    line = line.strip('\n')
    words = line.split("\t")
    if len(words)<=1:
        continue
    else:
        src=words[0]
        dst=words[1]
        trust=float(words[2])
        if(random.random()<0.3):
            trusts_l.write(src + '\t' + dst + '\t' + str(trust) + '\n')
        else:
            trusts.write(src+'\t'+dst+'\t'+str(trust)+'\n')
        knows.write(src+'\t'+dst+'\t'+'1'+'\n') 
        probs.write(src+'\t'+dst+'\t'+str(d[src+":::"+dst])+'\n')
        visualize.write(src+" -> "+dst+"\n")
