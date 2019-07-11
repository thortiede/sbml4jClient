import requests
import sys
import os
import json
import time


url_base = ""
option = ""

if (len(sys.argv) < 3):
    print("Usage: python createPathwayCollection.py <http://host:port/sbml4j> <list/persist>")
    sys.exit
else:
    url_base = sys.argv[1]
    option = sys.argv[2]


    print('using base url: ' + url_base)
    #respond = requests.get('http://localhost:8080/sbml4j/allEntities')

    #print(respond.text)
    #get_response = requests.get(url_base + "/allEntities")
    #print(get_response.text)
    #print("There are " + str(len(json.loads(get_response.text))) + " entities in the database")

    headersDict = {'user': 'Thor', 'Accept':'application/json'}
    paramDict = {'organism': 'hsa', 'matchingAttribute': 'sBaseId', 'source': 'KEGG', 'version': '2018-latest'}

    #{
	#"name": "TestKG",
	#"pathwayNodeIdString": "TestKGIdString",
	#"sourcePathwayEntityUUIDs": [
	#	"d9c6eb87-3fa7-40e1-9188-2747519f38b4",
	#	"ca09b3b6-1999-4f70-a14d-4b36e222d1d5"
	#	],
	#"databaseEntityUUID": "add06395-6e3a-4a23-b275-d9838a698f99"
    #}
    # localhost:8080/sbml4j/databaseUUID?source=KEGG&version=2018-latest&organism=hsa&matchingAttribute=sBaseId

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
