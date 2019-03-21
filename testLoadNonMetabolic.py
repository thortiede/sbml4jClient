import requests
import sys
import os
import json

# files
path = ""
if (len(sys.argv) > 1):
    path = sys.argv[1]

#print (os.listdir(path))
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

            getAll_response = requests.get('http://localhost:8080/sbml4j/allEntities')
            if(getAll_response.status_code == requests.codes.ok):
                checkAll_entities = getAll_response.text
                json_allEntities = json.loads(checkAll_entities)
                numAllEntities = len(json_allEntities)

                if(numPersisted == numAllEntities):
                    # all good
                    numEntitiesDict[f] = numPersisted
                    delete_response = requests.delete('http://localhost:8080/sbml4j/allEntities')
                else:
                    numEntitiesDict[f + "_p"] = numPersisted
                    numEntitiesDict[f + "_a"] = numAllEntities
                    delete_response = requests.delete('http://localhost:8080/sbml4j/allEntities')
            else:
                print("Failed to get all Entities for " + f)
                numEntitiesDict[f + "_x"] = numPersisted
                delete_response = requests.delete('http://localhost:8080/sbml4j/allEntities')
        else :
            print(f + " failed to presist")
            delete_response = requests.delete('http://localhost:8080/sbml4j/allEntities')


print (numEntitiesDict)
