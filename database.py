from peewee import MySQLDatabase
from models import databaseProxy, Information, Photos


class DatabaseManager(object):
    def __init__(self, args):
        self.args = args
        self.db = None

    def openConnection(self):
        dbase = self.getDatabase()
        self.db = dbase.connectToDatabase()

    def getDatabase(self):
        if self.args.database == 'mysql':
            return MySQL(self.args)
        else:
            return print('Sorry, not implemented yet :(')

    def closeConnection(self):
        self.db.close()
        print('Connection closed.')

    def uploadData(self, data):
        print('Uploading data into {0}.'.format(self.args.database))
        for row in self.db.batch_commit(data, 100):
            id = Information.create(**row)
            photos = []
            for photo in row['photos']:
                photos.append((id, photo))
            Photos.insert_many(photos, fields=[Photos.master_id, Photos.link]).execute()

    def connectToDatabase(self):
        raise Exception('You need to override function in child class!')


class MySQL(DatabaseManager):
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
