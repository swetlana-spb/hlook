from peewee import *
from models import databaseProxy, Information, Photos


class DatabaseManager(object):
    def __init__(self, args, data):
        self.args = args
        self.data = data
        self.dbase = None

    def openConnection(self):
        dbConnection = self.getDatabase()
        self.dbase = dbConnection.connectToDatabase()

    def getDatabase(self):
        if self.args.database == 'mysql':
            return MySQLWorker(self.args, self.data)
        else:
            return print('Sorry, not implemented yet :(')

    def closeConnection(self):
        self.dbase.close()
        print('Connection closed.')

    def uploadData(self):
        print('Uploading data into {0}.'.format(self.args.database))
        for row in self.dbase.batch_commit(self.data, 100):
            id = Information.create(**row)
            photos = []
            for photo in row['photos']:
                photos.append((id, photo))
            Photos.insert_many(photos, fields=[Photos.master_id, Photos.link]).execute()

    def connectToDatabase(self):
        raise Exception('You need to override function in child class!')


class MySQLWorker(DatabaseManager):
    def connectToDatabase(self):
        db = MySQLDatabase('hlook',
                           host=self.args.host,
                           port=self.args.port,
                           user=self.args.username,
                           passwd=self.args.password)
        db.connect()
        databaseProxy.initialize(db)
        print('Connection opened.')
        return db
