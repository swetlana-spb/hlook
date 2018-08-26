import json
import csv
import xml.etree.ElementTree as ET


class CParser(object):
    def __init__(self, file):
        self.file = file
        self.data = []
        self.photoTag = ''
        self.photosList = []


    def setData(self, file):
        pass


    def setDataLine(self, dataLine):
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
        file = open(self.file)
        self.setData(file)
        file.close()
        return self.data


class CParseJson(CParser):
    def setData(self, file):
        line = file.readline()
        while line:
            jsonLine = json.loads(line)
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
            dataDict = self.setDataLine(dataList)
            self.data.append(dataDict)
            line = file.readline()


class CParseCsv(CParser):
    def setData(self, file):
        reader = csv.DictReader(file, delimiter=',')
        for csvLine in reader:
            for i in range(5):
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
            dataDict = self.setDataLine(dataList)
            self.data.append(dataDict)


class CParseXml(CParser):
    def setData(self, file):
        tree = ET.parse(file)
        root = tree.getroot()
        for hotel in root.findall('hotel'):
            photos = hotel.find('photos').findall('photo')
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
            dataDict = self.setDataLine(dataList)
            self.data.append(dataDict)