# pybot2

This is an informal bot I've created for my own personal use and am still expanding on. The intent of it is for me to be able to use discord as my food journal. The bot will process commands in discord and add the food entries into a database for easy processing and tracking. Currently the bot and database are being stored on an aws ec2, but if I decide to expand further and keep using the bot I will move to using an aws database.  
Feel free to message me on discord (zaphiraf) to add the bot to your server if you're interested but I make no promises on the performance or continuation of service. I do plan on adding a csv command so anybody interested can keep their own information as a backup. 

To run the code yourself:

Needs .env file 
TEST_TOKEN=
DB_PASS=

Pip installs:
dotenv
datetime
mysql-connector-python
tabulate

**If you accidentally just install mysql-connector you need to uninstall it before installing mysql-connector-python. If you've installed both you need to uninstall both before reinstalling the correct one. 

Database stuff
it needs mysql installed for the database, or a another database option of your choice. If using mysql, the current default database name is just 'mydb'. These are the commands I used in mysql shell to get started:

CREATE DATABASE mydb;
USE mydb;
CREATE TABLE user (
    Userid DECIMAL(20,0) NOT NULL,
    Username varchar(255) NOT NULL,
    PRIMARY KEY (Userid)
);

CREATE TABLE diary (
    Diaryid int NOT NULL AUTO_INCREMENT,
    Userid DECIMAL(20,0) NOT NULL,
    Diarydate date NOT NULL,
    Entrydate date DEFAULT (CURDATE()),
    Entrytype varchar(10) check (Entrytype IN ('Food','Workout')),
    Entryname varchar(50) NOT NULL,
    Calories int NOT NULL,
    PRIMARY KEY (Diaryid),
    FOREIGN KEY (Userid) REFERENCES user(userid)
);
