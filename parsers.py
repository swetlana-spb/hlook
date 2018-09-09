import os
import json
import csv
import xml.etree.ElementTree as ET


class ParserManager(object):
    def __init__(self, args):
        self.args = args

    def parserChooser(self, fileName):
        extensionName = os.path.splitext(self.args.fileName)[1]
        if extensionName == u'.json':
            return ParseJson(fileName)
        elif extensionName == u'.csv':
            return ParseCsv(fileName)
        elif extensionName == u'.xml':
            return ParseXml(fileName)

    def getData(self):
        parser = self.parserChooser(self.args.fileName)
        data = parser.parse()
        return data


class Parser(object):
    def __init__(self, fileName):
        self.fileName = fileName
        self.data = []
        self.photoTag = ''

    def constructData(self, fileName):
        raise Exception('You need to override function in child class!')

    def parse(self):
        with open(self.fileName) as fileName:
            self.constructData(fileName)
            return self.data


class ParseJson(Parser):
    def constructData(self, fileName):
        for line in fileName:
            jsonLine = json.loads(line)
            photosList = []
            for image in jsonLine['images']:
                photosList.append(image['orig_url'])
            dataDict = {'name': jsonLine['en']['name'],
                        'address': jsonLine['en']['address'],
                        'city': jsonLine['en']['city'],
                        'country': jsonLine['en']['country'],
                        'countryCode': jsonLine['country_code'],
                        'rating': jsonLine['star_rating'],
                        'longitude': jsonLine['longitude'],
                        'latitude': jsonLine['latitude'],
                        'description': jsonLine['en']['description'],
                        'photos': photosList}
            self.data.append(dataDict)


class ParseCsv(Parser):
    def constructData(self, fileName):
        reader = csv.DictReader(fileName, delimiter=',')
        for csvLine in reader:
            photosList = []
            photoCount = 0
            for key in csvLine:
                if key.startswith('photo'):
                    photoCount += 1
            for i in range(photoCount):
                photosList.append(csvLine['photo%s'%(i+1)])
            dataDict = {'name': csvLine['hotel_name'],
                        'address': csvLine['addressline1'],
                        'city': csvLine['city'],
                        'country': csvLine['country'],
                        'countryCode': csvLine['countryisocode'],
                        'rating': csvLine['star_rating'],
                        'longitude': csvLine['longitude'],
                        'latitude': csvLine['latitude'],
                        'description': csvLine['overview'],
                        'photos': photosList}
            self.data.append(dataDict)


class ParseXml(Parser):
    def constructData(self, fileName):
        tree = ET.parse(fileName)
        root = tree.getroot()
        for hotel in root.findall('hotel'):
            photos = hotel.find('photos').findall('photo')
            photosList = []
            for photo in photos:
                photosList.append(photo.findtext('url'))
            dataDict = {'name': hotel.find('name').text,
                        'address': hotel.find('address').text,
                        'city': hotel.find('city').findtext('en'),
                        'country': hotel.find('country').findtext('en'),
                        'countryCode': hotel.find('countrytwocharcode').text,
                        'rating': hotel.find('stars').text,
                        'longitude': hotel.find('longitude').text,
                        'latitude': hotel.find('latitude').text,
                        'description': hotel.find('descriptions').findtext('en'),
                        'photos': photosList}
            self.data.append(dataDict)
