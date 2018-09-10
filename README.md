# hlook
A small script for uploading data from files .json, .xml or .csv into mysql database.

To run the script, you need:
 - python 3.x
 - peewee >= 3.6.0
 - pymysql
 - mysql (script for creating database included)

# Usage
main.py [-h] -f FILENAME -H HOST [-p PORT] -u USERNAME -P [PASSWORD] [-d DATABASE]

Loading data from files .json, .xml or .csv into mysql database.

optional arguments:

  -h, --help  show this help message and exit
  
  -f FILENAME, --fileName FILENAME path to a file
  
  -H HOST, --host HOST  ip-address of the database for uploading data
  
  -p PORT, --port PORT  port of the database for uploading data (default=3306)
  
  -u USERNAME, --username USERNAME username of the database
  
  -P [PASSWORD], --password [PASSWORD] password for the database user
  
  -d DATABASE, --database DATABASE type of the database: mysql, postgresql (default=mysql)
