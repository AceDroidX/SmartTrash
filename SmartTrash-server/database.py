import mysql.connector
import APIKey
'''
CREATE DATABASE smarttrash

CREATE TABLE typelist(
  -> id INT NOT NULL AUTO_INCREMENT,
  -> name VARCHAR(200) NOT NULL,
  -> type TINYINT NOT NULL,
  -> time DATETIME,
  -> PRIMARY KEY ( id )
  -> )ENGINE=InnoDB DEFAULT CHARSET=utf8;

INSERT INTO typelist 
(name, type, time)
VALUES
("丝绸家纺", 0, NOW());

SELECT *
FROM typelist
WHERE name="丝绸家纺"

UPDATE typelist SET type=0
WHERE name="丝绸家纺"

#tmplist = {'0': '可回收', '1': '有害', '2': '厨余(湿)', '3': '其他(干)'}
'''
mydb = mysql.connector.connect(
  host=APIKey.mysql_host,
  user=APIKey.mysql_user,
  passwd=APIKey.mysql_password
)

def getType(name):
    print(name)
    mycursor = mydb.cursor()
    mycursor.execute('use smarttrash')
    mycursor.execute('SELECT type FROM typelist WHERE name="%s"'%(name))
    result = mycursor.fetchone()     # fetchall() 获取所有记录
    print('getType:'+str(result))
    return result

def dbUpdate(name,trashtype):
    dbresult=getType(name)
    if dbresult==None:
        return addType(name,trashtype)
    else:
        return updateType(name,trashtype)

def addType(name,trashtype):
    print('addType:name:%strashtype:%s'%(name,trashtype))
    mycursor = mydb.cursor()
    mycursor.execute('use smarttrash')
    mycursor.execute('INSERT INTO typelist (name, type, time) VALUES ("%s", %s, NOW());'%(name,trashtype))
    mydb.commit()
    return mycursor.rowcount

def updateType(name,trashtype):
    print('updateType:name:%strashtype:%s'%(name,trashtype))
    mycursor = mydb.cursor()
    mycursor.execute('use smarttrash')
    mycursor.execute('UPDATE typelist SET type=%s WHERE name="%s"'%(trashtype,name))
    mydb.commit()
    return mycursor.rowcount