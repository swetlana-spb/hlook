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
        self.photosList = []


    def constructData(self, fileName):
        raise Exception('You need to override function in child class!')


    def constructDataLine(self, dataLine):
        dataDict = {'photos': []}
        (dataDict['name'],
        dataDict['address'],
        dataDict['city'],
        dataDict['country'],
        dataDict['countryCode'],
        dataDict['rating'],
        dataDict['longitude'],
        dataDict['latitude'],
        dataDict['description'],
        dataDict['photos']) = dataLine
        return dataDict


    def parse(self):
        fileName = open(self.fileName)
        self.constructData(fileName)
        fileName.close()
        return self.data


class ParseJson(Parser):
    def constructData(self, fileName):
        for line in fileName:
            jsonLine = json.loads(line)
            self.photosList = []
            for image in jsonLine['images']:
                self.photosList.append(image['orig_url'])
            dataList = [jsonLine['en']['name'],
                        jsonLine['en']['address'],
                        jsonLine['en']['city'],
                        jsonLine['en']['country'],
                        jsonLine['country_code'],
                        jsonLine['star_rating'],
                        jsonLine['longitude'],
                        jsonLine['latitude'],
                        jsonLine['en']['description'],
                        self.photosList]
            dataDict = self.constructDataLine(dataList)
            self.data.append(dataDict)


class ParseCsv(Parser):
    def constructData(self, fileName):
        reader = csv.DictReader(fileName, delimiter=',')
        for csvLine in reader:
            self.photosList = []
            photoCount = 0
            for key in csvLine:
                if key.startswith('photo'):
                    photoCount += 1
            for i in range(photoCount):
                self.photosList.append(csvLine['photo%s'%(i+1)])
            dataList = [csvLine['hotel_name'],
                        csvLine['addressline1'],
                        csvLine['city'],
                        csvLine['country'],
                        csvLine['countryisocode'],
                        csvLine['star_rating'],
                        csvLine['longitude'],
                        csvLine['latitude'],
                        csvLine['overview'],
                        self.photosList]
            dataDict = self.constructDataLine(dataList)
            self.data.append(dataDict)


class ParseXml(Parser):
    def constructData(self, fileName):
        tree = ET.parse(fileName)
        root = tree.getroot()
        for hotel in root.findall('hotel'):
            photos = hotel.find('photos').findall('photo')
            self.photosList = []
            for photo in photos:
                self.photosList.append(photo.findtext('url'))
            dataList = [hotel.find('name').text,
                        hotel.find('address').text,
                        hotel.find('city').findtext('en'),
                        hotel.find('country').findtext('en'),
                        hotel.find('countrytwocharcode').text,
                        hotel.find('stars').text,
                        hotel.find('longitude').text,
                        hotel.find('latitude').text,
                        hotel.find('descriptions').findtext('en'),
                        self.photosList]
            dataDict = self.constructDataLine(dataList)
            self.data.append(dataDict)
