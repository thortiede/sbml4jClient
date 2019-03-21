import requests
import sys
import os
import json
import time


# files
path = ""
url_base = ""

if (len(sys.argv) < 3):
    print("Usage: python sbml4jClient.py <pathWithSBMLFiles> <http://host:port/sbml4j>")
    sys.exit
else:
    path = sys.argv[1]
    url_base = sys.argv[2]

    filelist = os.listdir(path)

    print('Processing directory' + path)
    print('using base url: ' + url_base)
    #respond = requests.get('http://localhost:8080/sbml4j/allEntities')
    upload_url = url_base + "/sbml"
    #print(respond.text)
    get_response = requests.get(url_base + "/allEntities")
    #print(get_response.text)
    print("There are " + str(len(json.loads(get_response.text))) + " entities in the database")
    if (not input("Continue ? (y/n): ").lower().strip()[:1] == "y"):
        sys.exit(1)
    else:
        delete_response = requests.delete(url_base + "/allEntities")
        print(delete_response.text)

        numEntitiesDict = {}
        start_all = time.time()
        for f in filelist:
            if(f.endswith(".xml")):
                start = time.time()
                fullFilePath = path+"/"+f
                print(fullFilePath)
                # read contents of files
                file = open(fullFilePath, "rb")
                post_response = requests.post(upload_url, files = {'file' : (f, file, 'application/xml')})
                if(post_response.status_code == requests.codes.ok):
                    persisted_entities = post_response.text
                    json_persisted = json.loads(persisted_entities)
                    numPersisted = len(json_persisted)
                    numEntitiesDict[f] = numPersisted
                else :
                    print(f + " failed to presist")
                    print(post_response.status_code)
                    print(post_response.text)
                end = time.time()
                print("File " + f + " took " + str(end - start))

        print (numEntitiesDict)
        end_all = time.time()
        print("Persisting of all files took " + str(end_all - start_all) + " seconds")
