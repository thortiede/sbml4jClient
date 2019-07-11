import requests
import sys
import os
import json
import time

def do_deleteAll(url_base):
    delete_response = requests.delete(url_base + "/allEntities")
    print(delete_response.text)

# files
path = ""
url_base = ""
type = ""
organism = ""
option = ""
cleardb = ""
if (len(sys.argv) < 7):
    print("Usage: python sbml4jClient.py <pathWithSBMLFiles> <http://host:port/sbml4j> <type:metabolic/non-metabolic/both> <organism-three-letter-code> <list/persist> <clear/keep>")
    sys.exit
else:
    path = sys.argv[1]
    url_base = sys.argv[2]
    type = sys.argv[3]
    organism = sys.argv[4]
    option = sys.argv[5]
    cleardb = sys.argv[6]



    print('Processing directory' + path)
    print('using base url: ' + url_base)
    #respond = requests.get('http://localhost:8080/sbml4j/allEntities')
    upload_url = url_base + "/sbml"
    #print(respond.text)
    get_response = requests.get(url_base + "/allEntities")
    #print(get_response.text)
    print("There are " + str(len(json.loads(get_response.text))) + " entities in the database")
    if(cleardb == "clear"):
        do_deleteAll(url_base)

    # 1. Persisting Pathways

    headersDict = {'user': 'Thor', 'Accept':'application/json'}
    paramDict = {'organism': 'hsa', 'matchingAttribute': 'sBaseId', 'source': 'KEGG', 'version': '2018-latest'}

    numEntitiesDict = {}
    start_all = time.time()
    listFileList = []
    if (type == "both"):
        listFileList.append("metabolic")
        listFileList.append("non-metabolic")
    else:
        listFileList.append(type)

    for typeOfPathway in listFileList:
        filePath = path + "/" + typeOfPathway + "/organisms/" + organism
        print(filePath)
        filelist = os.listdir(filePath)

        for f in filelist:
            if(f.endswith(".xml")):
                if(option == "list"):
                    print(f)
                elif(option == "persist"):
                    start = time.time()
                    fullFilePath = filePath+"/"+f
                    print(fullFilePath)
                    # read contents of files
                    file = open(fullFilePath, "rb")
                    post_response = requests.post(upload_url, params = paramDict, headers=headersDict, files = {'file' : (f, file, 'application/xml')})
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
                    print("Persisting file " + f + " took " + str(end - start))

    print (numEntitiesDict)
    end_all = time.time()
    print("Persisting of all files took " + str(end_all - start_all) + " seconds")

    if (option == "persist"):
        # 2. building pathwayCollection
        # get all pathway UUIDs
        uuidList = list()
        pathwayUUIDs = requests.get(url_base + "/pathwayUUIDs")
        for pathwayUUID in json.loads(pathwayUUIDs.text):
            uuidList.append(pathwayUUID)

        #get databaseUUID
        databaseParamDict = {'source': 'KEGG', 'version': '2018-latest', 'organism': 'hsa', 'matchingAttribute': 'sBaseId'}
        databaseUUID = requests.get(url_base + "/databaseUUID", params=databaseParamDict)
        print ("Using database with entityUUID: " + databaseUUID.text)

        pathwayCollectionDict = {'name': 'TestPC', 'pathwayNodeIdString': 'TestPCIdString', 'sourcePathwayEntityUUIDs': uuidList, 'databaseEntityUUID': databaseUUID.text}
        #print(pathwayCollectionDict)

        pathwayCollectionCreated = requests.post(url_base + "/pathwayCollection", headers=headersDict, json=pathwayCollectionDict)
        print(pathwayCollectionCreated.text)

        # 3. create all pathway mappings
        # get all pathway UUIDs
        responseList = list()
        # refresh the pathwayList to include the collection pathway
        pathwayUUIDs = requests.get(url_base + "/pathwayUUIDs")
        for pathwayUUID in json.loads(pathwayUUIDs.text):
            start = time.time()
            mappingParams = {'pathwayEntityUUID': pathwayUUID, 'mappingType': 'PATHWAYMAPPING', 'externalResource': 'KEGGGENES'}
            response = requests.post(url_base + "/mapping", headers = headersDict, params=mappingParams)
            responseList.append(response.text)
            end = time.time()
            print("Creating mapping for " + pathwayUUID + " took " + str(end - start) + " seconds")

        for resp in responseList:
            print(resp)
