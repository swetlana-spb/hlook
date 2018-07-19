from peewee import *

databaseProxy = Proxy()


class Information(Model):
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
    master_id = IntegerField()
    link = TextField()

    class Meta:
        db_table = 'photos'
        database = databaseProxy