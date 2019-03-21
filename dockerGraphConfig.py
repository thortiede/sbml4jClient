import csv
import sys

configFile = ""
if (len(sys.argv) > 1):
    configFile = sys.argv[1]
    print (configFile)


def getMaxId(configfile):
    


def read_config(configfile):
    with open(configfile, "r", newline='') as config:
        config_reader = csv.reader(config, delimiter=",")
        for row in config_reader:
            print(row)

def register_database(configfile, name, version, path):
    new_database_id = getMaxId(configFile) + 1
    with open(configfile, 'w', newline = '') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow([name] + [version] + [path])

    return new_database_id


id_is_one = register_database(configFile, "Test", 1, "somepath")
print(id_is_one)

read_config(configFile)
