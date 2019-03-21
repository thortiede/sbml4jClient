import requests
import sys
import os
import json


# files
path = ""
if (len(sys.argv) > 1):
    path = sys.argv[1]

filelist = os.listdir(path)


#respond = requests.get('http://localhost:8080/sbml4j/allEntities')
upload_url = "http://localhost:8080/sbml4j/uploadSBMLSimple"
#print(respond.text)
delete_response = requests.delete('http://localhost:8080/sbml4j/allEntities')
print(delete_response.text)

numEntitiesDict = {}

for f in filelist:
    if(f.endswith(".xml")):
        fullFilePath = path+"/"+f
        print(fullFilePath)
        # read contents of files
        file = open(fullFilePath, "rb")
        post_response = requests.post(upload_url, files = {'file' : file})
        if(post_response.status_code == requests.codes.ok):
            persisted_entities = post_response.text
            json_persisted = json.loads(persisted_entities)
            numPersisted = len(json_persisted)
            numEntitiesDict[f] = numPersisted
        else :
            print(f + " failed to presist")
            print(post_response.status_code)
            print(post_response.text)
            
print (numEntitiesDict)
