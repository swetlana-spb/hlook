import getpass
from ipaddress import ip_address
from peewee import *
from models import databaseProxy, Information, Photos


def connectToMysql():
    correctHost = False
    while not correctHost:
        hostInput = input(u'Enter ip-address of the mysql database to upload data: ')
        try:
            host = ip_address(hostInput.split()[0])
            correctHost = True
        except ValueError:
            print(u'Incorrect ip-address')
        except IndexError:
            print(u'Input is empty :(')
    user, passwd = enterConnectionData()
    return host, user, passwd


def enterConnectionData():
    usernameInput = input(u'Username: ')
    passwdInput = getpass.getpass(u'Password: ')
    return usernameInput, passwdInput


def uploadDataToMysql(host, user, passwd, data):
    try:
        db = MySQLDatabase(u'hlook',
                           host=str(host),
                           port=3306,
                           user=user,
                           passwd=passwd)
        db.connect()
        print(u'Connection opened.')
        databaseProxy.initialize(db)
        print(u'Uploading data to Mysql.')

        for row in data:
            id = Information.create(name = row['name'],
                               address = row['address'],
                               city = row['city'],
                               country = row['country'],
                               countryCode = row['countryCode'],
                               rating=row['rating'],
                               longitude = row['longitude'],
                               latitude = row['latitude'],
                               description = row['description'])

            for photo in row['photos']:
                Photos.create(master_id = id,
                              link = photo)


        db.close()
        print(u'Connection closed.')

    except:

        print(u'Connection failed.')



