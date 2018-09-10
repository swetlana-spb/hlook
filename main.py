import argparse
import getpass
from parsers import ParserManager
from database import DatabaseManager


class Password(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        if values is None:
            values = getpass.getpass()
        setattr(namespace, self.dest, values)


def createArgsParser():
    parser = argparse.ArgumentParser(description='Loading data from files .json, .xml or .csv into database.')
    parser.add_argument('-f', '--fileName', help='path to a file', required=True)
    parser.add_argument('-H', '--host', help='ip-address of the database for uploading data', required=True)
    parser.add_argument('-p', '--port',
                        help='port of the database for uploading data',
                        required=False,
                        default=3306)
    parser.add_argument('-u', '--username', help='username of the database', required=True)
    parser.add_argument('-P', '--password',
                        action=Password,
                        nargs='?',
                        help='password for the database user',
                        required=True)
    parser.add_argument('-d', '--database',
                        help='type of the database: mysql, postgresql',
                        required=False, default='mysql')
    return parser


if __name__ == '__main__':
    argsParser = createArgsParser()
    args = argsParser.parse_args()
    data = ParserManager(args).getData()

    if data:
        databaseWorker = DatabaseManager(args, data)
        databaseWorker.openConnection()
        try:
            databaseWorker.uploadData()
            print('Data successfully uploaded! :)')
        except:
            print('Oops, something go wrong. :(')
        databaseWorker.closeConnection()
    else:
        print('There is no data to upload. :(')

    print('Bye!')
