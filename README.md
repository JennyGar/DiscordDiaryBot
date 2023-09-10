# pybot2

This is a bot I've created for my own personal use and am still expanding on. The intent of it is for me to be able to use discord as my food journal. The bot will process commands in discord and add the food entries into a database for easy processing and tracking. Currently the bot and database are being stored on an aws ec2, but if I decide to expand further and keep using the bot I will move to using an aws database.  

To run:
Needs mysql install for database, or dbservice to be modified accordingly. 

Needs .env file 
TEST_TOKEN=
DB_PASS=

Pip installs:
dotenv
datetime
mysql.connector
tabulate

