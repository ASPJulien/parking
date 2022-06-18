import json
from os.path import exists

config_placeholder = {
    'apikey': 'qsdf',
    'token': 'qsdf'
}


def readconfig():
    if exists("config.json"):
        print("réattribution")
        return json.loads(open("config.json").read())
    else:
        print("Config file does not exist, creating a new one to ./config.json.")
        with open('config.json', 'w') as outfile:
            json.dump(config_placeholder, outfile)
        return readconfig()


def get_config():
    global config
    print(config)
    if not config:
        config = readconfig()
    return config
