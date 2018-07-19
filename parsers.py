import json
import csv
import xml.etree.ElementTree as ET


def parseJson(file):
    file = open(file)
    data = []
    line = file.readline()
    while line:
        jsonLine = json.loads(line)
        dataLine = {'photos': []}
        dataLine['name'] = jsonLine['en']['name']
        dataLine['address'] = jsonLine['en']['address']
        dataLine['city'] = jsonLine['en']['city']
        dataLine['country'] = jsonLine['en']['country']
        dataLine['countryCode'] = jsonLine['country_code']
        dataLine['rating'] = jsonLine['star_rating']
        dataLine['longitude'] = jsonLine['longitude']
        dataLine['latitude'] = jsonLine['latitude']
        dataLine['description'] = jsonLine['en']['description']
        for image in jsonLine['images']:
            dataLine['photos'].append(image['orig_url'])
        data.append(dataLine)
        line = file.readline()
    file.close()

    return data


def parseCsv(file):
    file = open(file)
    data = []
    reader = csv.DictReader(file, delimiter=',')
    for csvLine in reader:
        dataLine = {'photos': []}
        dataLine['name'] = csvLine['hotel_name']
        dataLine['address'] = csvLine['addressline1']
        dataLine['city'] = csvLine['city']
        dataLine['country'] = csvLine['country']
        dataLine['countryCode'] = csvLine['countryisocode']
        dataLine['rating'] = csvLine['star_rating']
        dataLine['longitude'] = csvLine['longitude']
        dataLine['latitude'] = csvLine['latitude']
        dataLine['description'] = csvLine['overview']
        for i in range(5):
            dataLine['photos'].append(csvLine['photo%s'%(i+1)])
        data.append(dataLine)
    file.close()

    return data


def parseXml(file):
    data = []
    tree = ET.parse(file)
    root = tree.getroot()
    for hotel in root.findall('hotel'):
        dataLine = {'photos': []}
        dataLine['name'] = hotel.find('name').text
        dataLine['address'] = hotel.find('address').text
        dataLine['city'] = hotel.find('city').findtext('en')
        dataLine['country'] = hotel.find('country').findtext('en')
        dataLine['countryCode'] = hotel.find('countrytwocharcode').text
        dataLine['rating'] = hotel.find('stars').text
        dataLine['longitude'] = hotel.find('longitude').text
        dataLine['latitude'] = hotel.find('latitude').text
        dataLine['description'] = hotel.find('descriptions').findtext('en')

        photos = hotel.find('photos').findall('photo')
        for photo in photos:
            dataLine['photos'].append(photo.findtext('url'))
        data.append(dataLine)

    return data
