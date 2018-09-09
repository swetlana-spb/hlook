from peewee import *

databaseProxy = Proxy()


class Information(Model):
    id = PrimaryKeyField(null=False)
    name = CharField()
    address = TextField()
    city = CharField()
    country = CharField()
    countryCode = CharField()
    rating = IntegerField()
    longitude = DoubleField()
    latitude = DoubleField()
    description = TextField()

    class Meta:
        db_table = 'information'
        database = databaseProxy


class Photos(Model):
    id = PrimaryKeyField(null=False)
    master_id = ForeignKeyField(Information)
    link = TextField()

    class Meta:
        db_table = 'photos'
        database = databaseProxy
