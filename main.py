import argparse
import getpass
from parsers import ParserManager
from database import DatabaseManager


class Password(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        if values is None:
            values = getpass.getpass()
        setattr(namespace, self.dest, values)


def getArgs():
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
    return parser.parse_args()


if __name__ == '__main__':
    args = getArgs()
    db = DatabaseManager(args)
    db.openConnection()
    data = ParserManager(args).getData()

    if data:
        try:
            db.uploadData(data)
            print('Data successfully uploaded! :)')
        except:
            print('Oops, something went wrong. :(')
    else:
        print('There is no data to upload. :(')
    db.closeConnection()
    print('Bye!')
