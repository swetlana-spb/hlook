import argparse
import getpass
from parsers import ParserManager
from database import WorkingWithMySQL


class Password(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        if values is None:
            values = getpass.getpass()
        setattr(namespace, self.dest, values)


def createArgsParser():
    parser = argparse.ArgumentParser(description='Loading data from files .json, .xml or .csv into mysql database.')
    parser.add_argument('-f', '--fileName', help='path to a file', required=True)
    parser.add_argument('-H', '--host', help='ip-address of the mysql database for uploading data', required=True)
    parser.add_argument('-p', '--port', help='port of the mysql database for uploading data', required=False, default=3306)
    parser.add_argument('-u', '--username', help='username of the mysql database', required=True)
    parser.add_argument('-P', '--password', action=Password, nargs='?', help='password of the mysql database user', required=True)
    return parser


if __name__ == '__main__':
    argsParser = createArgsParser()
    args = argsParser.parse_args()
    data = ParserManager(args).getData()

    if data:
        mysqlWorker = WorkingWithMySQL(args, data)
        try:
            mysqlWorker.uploadDataToMysql()
            print('Data successfully uploaded. Thank you. Bye! :)')
        except:
            print('Sorry, something go wrong. :(')
    else:
        print('There is no data to upload. :(')
