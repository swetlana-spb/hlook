import sys
import os
from parsers import CParseJson, CParseCsv, CParseXml
from database import connectToMysql, uploadDataToMysql


def parseFile(file):
    extensionName = os.path.splitext(file)[1]
    if extensionName == u'.json':
        parser = CParseJson(file)
    elif extensionName == u'.csv':
        parser = CParseCsv(file)
    elif extensionName == u'.xml':
        parser = CParseXml(file)
    else:
        print(u'Not supported file extension "%s". Supported file extensions are: ".json", ".csv" and ".xml".'%extensionName)
        return None
    data = parser.parse()
    return data


def main(file):
    data = parseFile(file)
    if data:
        host, user, passwd = connectToMysql()
        if uploadDataToMysql(host, user, passwd, data):
            print(u'Data successfully uploaded. Thank you. Bye! :)')
    elif data is not None:
        print(u'Sorry, there is no data to upload. :(')


if __name__ == '__main__':
    if len(sys.argv) > 3:
        print(u'Too much arguments. Use "--file" or "-f" to specify a path to a file.')
    elif len(sys.argv) == 1:
        print(u'Use "--file" or "-f" to specify a path to a file.')
    else:
        if sys.argv[1] == '--file' or sys.argv[1] == '-f':
            if os.path.isfile(sys.argv[2]):
                main(sys.argv[2])
            else:
                print(u'"%s" is not a file.' % sys.argv[2])
        else:
            print(u'Unknown param "%s". Use --file or -f.' % sys.argv[1])
