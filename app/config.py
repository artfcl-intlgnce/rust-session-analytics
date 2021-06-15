#!/usr/bin/python
from configparser import ConfigParser


#Config = ConfigParser()
#Config.read("keys.ini")

def dbconfig(filename='/app/keys.ini', section='postgresql'):
    parser = ConfigParser()
    parser.read(filename)
    print(parser.sections())

    # get section, default to postgresql
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]

print(dbconfig())


'''
def bmconfig(filename='keys.ini', section='battlemetrics'):
    parser = ConfigParser()
    parser.read(filename)
    result = {}
    
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            result[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))

    return result

print(bmconfig())
'''
