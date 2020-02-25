import requests
import sys
import os
import json
import time

url_base = ""

if (len(sys.argv) < 2):
    print("Usage: python testNetworkInventory.py <http://host:port/sbml4j>")
    sys.exit
else:
    url_base = sys.argv[1]

    print('using base url: ' + url_base)
    #respond = requests.get('http://localhost:8080/sbml4j/allEntities')

    #print(respond.text)
    headersDict = {'user': 'openMTB', 'Accept':'application/json'}
    networkInventoryURL = url_base + "/networkInventory"
    get_response = requests.get(networkInventoryURL, headers=headersDict)
    print(get_response.text)
