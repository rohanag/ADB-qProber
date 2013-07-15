from __future__ import division #For eliminating round off while dividing integers
import urllib2
import urllib
import base64
import json
import sys
import math
import re
from collections import Counter  #for content summaries
import os

key=sys.argv[1]
tes=float(sys.argv[2])
tec=int(sys.argv[3])
host=sys.argv[4]

#This custom append function appends a path to a list and removes all paths that are prefixes of that new path 
def my_append(classif, classification):
    for c in classif:
        if c in classification:
            classif[classif.index(c)]=""
    classif.append(classification)
    return classif

#Takes a query and returns the total number of matches as well as the results of the bing search 
def search_bing(query):
    
    bingUrl = 'https://api.datamarket.azure.com/Data.ashx/Bing/SearchWeb/v1/Composite?Query=%27site%3a'+host+'%20'+query.replace(' ', '%20')+'%27&$top=4&$format=json'
    accountKey = str(key)#'qhoA3ZNi3uIxUpjHcHBedrnxJ9O2LQ1QyzWJ2+Bmddg='
    accountKeyEnc = base64.b64encode(accountKey + ':' + accountKey)
    headers = {'Authorization': 'Basic ' + accountKeyEnc}
    req = urllib2.Request(bingUrl, headers = headers)
    response = urllib2.urlopen(req)
    content = response.read()
    result=json.loads(content)  #The extracted content is in JSON format.It needs to be converted into a nested dictionary type
    
    return result['d']['results'][0]['WebTotal'], [i['Url'] for i in result['d']['results'][0]['Web']]

rules={}
rules['Computers']=[]
rules['Health']=[]
rules['Sports']=[]


#Reading all query probes from the text files##################################################################
file=open('root.txt','r')
for f in file.xreadlines():
    s=f.split()
    #print s
    if s==[]:
        continue
    if s[0]=='Computers':
        rules['Computers'].append(" ".join(s[1:]))
    if s[0]=='Health':
        rules['Health'].append(" ".join(s[1:]))
    if s[0]=='Sports':
        rules['Sports'].append(" ".join(s[1:]))
file.close()

rules['Hardware']=[]
rules['Programming']=[]
file=open('computers.txt','r')
for f in file.xreadlines():
    s=f.split()
    
    if s==[]:
        continue
    if s[0]=='Hardware':
        rules['Hardware'].append(" ".join(s[1:]))
    if s[0]=='Programming':
        rules['Programming'].append(" ".join(s[1:]))
file.close() 

rules['Diseases']=[]
rules['Fitness']=[]
file=open('health.txt','r')
for f in file.xreadlines():
    s=f.split()
    
    if s==[]:
        continue
    if s[0]=='Diseases':
        rules['Diseases'].append(" ".join(s[1:]))
    if s[0]=='Fitness':
        rules['Fitness'].append(" ".join(s[1:])) 

file.close()

rules['Soccer']=[]
rules['Basketball']=[]
file=open('sports.txt','r')
for f in file.xreadlines():
    s=f.split()
   
    if s==[]:
        continue
    if s[0]=='Soccer':
        rules['Soccer'].append(" ".join(s[1:]))
    if s[0]=='Basketball':
        rules['Basketball'].append(" ".join(s[1:]))
file.close()


#Storing the parent child relation of the categories as a dictionary#########################################################

categories={}
categories['Root']=['Computers', 'Health', 'Sports']
categories['Computers']=['Hardware', 'Programming']
categories['Health']=['Fitness', 'Diseases']
categories['Sports']=['Basketball', 'Soccer']

#Storing the coverage and specificity of each category in a dictionary called covspec.The value of each key is a list whose first element is the coverage and second element is the specificity############################################################## 

covspec={}
covspec['Root']=[0, 1]
covspec['Computers']=[0, 0]
covspec['Hardware']=[0, 0]
covspec['Programming']=[0, 0]
covspec['Health']=[0, 0]
covspec['Fitness']=[0, 0]
covspec['Diseases']=[0, 0]
covspec['Sports']=[0, 0]
covspec['Basketball']=[0, 0]
covspec['Soccer']=[0, 0]

#Storing the URLs of each category in a dictionary (for content summaries)###############################################
cat_urls={}
cat_urls['Root']=[]
cat_urls['Computers']=[]
cat_urls['Health']=[]
cat_urls['Sports']=[]


#The classification algorithm :qprober.For details refer to README###############################################3
print "Classifying......"

classif=["Root"]
for d in classif:
    
    c=d.split('/')[-1] 
    if c not in categories :
        break
        
    total=0
    
    for items in categories[c]:
        for query in rules[items]:
            
            res=search_bing(query)
            temp=int(res[0])
            cat_urls[c]=list(set(cat_urls[c]+res[1]))
            
            total+=temp
            covspec[items][0]+=temp
        
    for items in categories[c]:
        covspec[items][1]=covspec[c][1]*(covspec[items][0]/total)
        print "Specificity for category "+items+ " is", covspec[items][1]
        print "Coverage for category "+items+ " is", covspec[items][0]
        
    for items in categories[c]:
        
        if covspec[items][0]>=tec and covspec[items][1]>=tes:
            
            
            classif=my_append(classif, d+'/'+items)
            
                
    
classif=[c for c in classif if c]
print "\n \n Classification:"
for c in classif:
    print c


#Part b.Generating content summaries and printing to file###############################################3
print "\n \n Extracting topic content summaries"


for classification in classif:
    path=classification.split('/')
    if len(path)>1:
        cat_urls[path[0]]=list(set(cat_urls[path[0]]+cat_urls[path[1]]))
    
    
for c in cat_urls:
    
    content_summary=Counter()
    for url in cat_urls[c]:
        print "Creating content summary for ", c
        words=[]
        print "\nGetting page: ", url
        f=os.popen('lynx -dump "'+url+'"') #Scraping the web page through lynx
        for l in f.xreadlines():
            if l.strip():
                
                if l.split()[0]=="References":
                    
                    break
            l=re.sub(r'\[[^)]*\]', '', l)
            words=words+re.split("\W+|\d|_", l) #Tokenizing
            
            words = [x.lower() for x in words if x]
            words=list(set(words))
        for w in words:
            content_summary[w]+=1
    
    if cat_urls[c]:
        
        consumm=open(c+'-'+host+'.txt', 'w')
        for c in content_summary:
            consumm.write(c+"#"+str(content_summary[c])+"\n")
        consumm.close()
    


