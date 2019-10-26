CREATE DATABASE smarttrash

------------typelist--------------

CREATE TABLE typelist(
id INT NOT NULL AUTO_INCREMENT,
name VARCHAR(200) NOT NULL,
type TINYINT NOT NULL,
time DATETIME,
PRIMARY KEY ( id )
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

INSERT INTO typelist 
(name, type, time)
VALUES
("丝绸家纺", 0, NOW());

SELECT *
FROM typelist
WHERE name="丝绸家纺"

UPDATE typelist SET type=0
WHERE name="丝绸家纺"

----tmplist = {'0': '可回收', '1': '有害', '2': '厨余(湿)', '3': '其他(干)'}


----------history-------------


CREATE TABLE history(
id INT NOT NULL AUTO_INCREMENT,
name VARCHAR(200) NOT NULL,
type TINYINT NOT NULL,
time DATETIME,
PRIMARY KEY ( id )
)ENGINE=InnoDB DEFAULT CHARSET=utf8;