DROP TABLE IF EXISTS user;
CREATE TABLE user (
    Userid DOUBLE NOT NULL,
    Username varchar(255) NOT NULL,
    PRIMARY KEY (Userid)
);

--@block
DROP TABLE IF EXISTS diary;
CREATE TABLE diary (
    Diaryid int NOT NULL AUTO_INCREMENT,
    Userid DOUBLE NOT NULL,
    Diarydate date NOT NULL,
    Entrydate date DEFAULT (CURDATE()),
    Entrytype varchar(10) check (Entrytype IN ('Food','Workout')),
    Entryname varchar(50) NOT NULL,
    Calories int NOT NULL,
    PRIMARY KEY (Diaryid),
    FOREIGN KEY (Userid) REFERENCES user(userid)
);

--@block 
DESC user;
DESC diary;

--@block
INSERT INTO user
VALUES(128342056262303744, 'zaphiraf')

--@block
SELECT * FROM user

--@block
SELECT * FROM diary