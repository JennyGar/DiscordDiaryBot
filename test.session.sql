DROP TABLE IF EXISTS user;
CREATE TABLE user (
    Userid DECIMAL(20,0) NOT NULL,
    Username varchar(255) NOT NULL,
    PRIMARY KEY (Userid)
);

--@block
DROP TABLE IF EXISTS diary;
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

--@block
SELECT Diaryid, Userid, Diarydate, Entrytype, Entryname, Calories FROM diary WHERE Diaryid=30

--@block
DELETE FROM diary WHERE Diaryid=10

--@block
SELECT * FROM diary WHERE MONTH(diarydate) = 09