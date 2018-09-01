from peewee import *
from models import databaseProxy, Information, Photos


class WorkingWithMySQL(object):
    def __init__(self, args, data):
        self.args = args
        self.data = data


    def uploadDataToMysql(self):
        try:
            db = MySQLDatabase(u'hlook',
                               host=self.args.host,
                               port=self.args.port,
                               user=self.args.username,
                               passwd=self.args.password)
            db.connect()
            print(u'Connection opened.')
            databaseProxy.initialize(db)
            print(u'Uploading data to Mysql.')

            for row in self.data:
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