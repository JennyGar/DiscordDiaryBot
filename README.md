# pybot2

This is an informal bot I've created for my own personal use and am still expanding on. The intent of it is for me to be able to use discord as my food journal. The bot will process commands in discord and add the food entries into a database for easy processing and tracking. Currently the bot and database are being stored on an aws ec2, but if I decide to expand further and keep using the bot I will move to using an aws database.  
Feel free to message me on discord (zaphiraf) for a link to add the bot to your server if you're interested or use the code to host the bot yourself. I do plan on adding a csv command so anybody interested can keep their own information as a backup. 

# Hosting the bot yourself:

You first need to create a bot on discord through the application portal and create a login key. After your bot is set up and ready pull the code from here and

create a .env file:
```
TEST_TOKEN=[Your discord token here]
DB_PASS=[Your database password here]
```

Pip installs:
dotenv
datetime
mysql-connector-python
tabulate

**If you accidentally just install mysql-connector you need to uninstall it before installing mysql-connector-python. If you've installed both you need to uninstall both before reinstalling the correct one. 

# Database stuff
By default it needs mysql installed for the database. You can use another database option of your choice if you want to modify some of the code. If using mysql, the current default database name is just 'mydb'. These are the commands I used in mysql shell to get started:

```
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
```
