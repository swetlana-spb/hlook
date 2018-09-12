import os
import json
import csv
import xml.etree.ElementTree as ET


class ParserManager(object):
    def __init__(self, args):
        self.args = args

    def parser_chooser(self, fileName):
        extension_name = os.path.splitext(self.args.fileName)[1]
        if extension_name == u'.json':
            return ParseJson(fileName)
        elif extension_name == u'.csv':
            return ParseCsv(fileName)
        elif extension_name == u'.xml':
            return ParseXml(fileName)

    def get_data(self):
        parser = self.parser_chooser(self.args.fileName)
        data = parser.parse()
        return data


class Parser(object):
    def __init__(self, fileName):
        self.fileName = fileName
        self.data = []

    def construct_data(self, fileName):
        raise Exception('You need to override function in child class!')

    def parse(self):
        with open(self.fileName) as fileName:
            self.construct_data(fileName)
            return self.data


class ParseJson(Parser):
    def construct_data(self, fileName):
        for line in fileName:
            json_line = json.loads(line)
            photos_list = []
            for image in json_line['images']:
                photos_list.append(image['orig_url'])
            data_dict = {'name': json_line['en']['name'],
                        'address': json_line['en']['address'],
                        'city': json_line['en']['city'],
                        'country': json_line['en']['country'],
                        'countryCode': json_line['country_code'],
                        'rating': json_line['star_rating'],
                        'longitude': json_line['longitude'],
                        'latitude': json_line['latitude'],
                        'description': json_line['en']['description'],
                        'photos': photos_list}
            self.data.append(data_dict)


class ParseCsv(Parser):
    def construct_data(self, fileName):
        reader = csv.DictReader(fileName, delimiter=',')
        for csv_line in reader:
            photos_list = []
            photo_counter = 0
            for key in csv_line:
                if key.startswith('photo'):
                    photo_counter += 1
            for i in range(photo_counter):
                photos_list.append(csv_line['photo%s'%(i+1)])
            data_dict = {'name': csv_line['hotel_name'],
                        'address': csv_line['addressline1'],
                        'city': csv_line['city'],
                        'country': csv_line['country'],
                        'countryCode': csv_line['countryisocode'],
                        'rating': csv_line['star_rating'],
                        'longitude': csv_line['longitude'],
                        'latitude': csv_line['latitude'],
                        'description': csv_line['overview'],
                        'photos': photos_list}
            self.data.append(data_dict)


class ParseXml(Parser):
    def construct_data(self, fileName):
        tree = ET.parse(fileName)
        root = tree.getroot()
        for hotel in root.findall('hotel'):
            photos = hotel.find('photos').findall('photo')
            photos_list = []
            for photo in photos:
                photos_list.append(photo.findtext('url'))
            data_dict = {'name': hotel.find('name').text,
                        'address': hotel.find('address').text,
                        'city': hotel.find('city').findtext('en'),
                        'country': hotel.find('country').findtext('en'),
                        'countryCode': hotel.find('countrytwocharcode').text,
                        'rating': hotel.find('stars').text,
                        'longitude': hotel.find('longitude').text,
                        'latitude': hotel.find('latitude').text,
                        'description': hotel.find('descriptions').findtext('en'),
                        'photos': photos_list}
            self.data.append(data_dict)
