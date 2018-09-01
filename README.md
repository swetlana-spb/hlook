# hlook
A small script for uploading data from files .json, .xml or .csv into mysql database.

To run the script, you need:
 - python 3.x
 - peewee
 - pymysql
 - mysql (script for creating database included)

# Usage
main.py [-h] -f FILENAME -H HOST [-p PORT] -u USERNAME -P [PASSWORD]

optional arguments:

  -h, --help            show this help message and exit
  
  -f FILENAME, --fileName FILENAME                        path to a file
  
  -H HOST, --host HOST  ip-address of the mysql database for uploading data
  
  -p PORT, --port PORT  port of the mysql database for uploading data
  
  -u USERNAME, --username USERNAME username of the mysql database
  
  -P [PASSWORD], --password [PASSWORD] password of the mysql database user