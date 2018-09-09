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

            with db.atomic():
                for row in self.data:
                    id = Information.create(**row)
                    photos = []
                    for photo in row['photos']:
                        photos.append((id, photo))
                    Photos.insert_many(photos, fields=[Photos.master_id, Photos.link]).execute()

            db.close()
            print(u'Connection closed.')
        except:
            print(u'Connection failed.')