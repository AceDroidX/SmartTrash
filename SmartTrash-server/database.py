import mysql.connector
import APIKey

def getType(name):
    mydb = mysql.connector.connect(
    host=APIKey.mysql_host,
    user=APIKey.mysql_user,
    passwd=APIKey.mysql_password)
    mycursor = mydb.cursor()
    mycursor.execute('use smarttrash')
    mycursor.execute('SELECT type FROM typelist WHERE name="%s"' % (name))
    result = mycursor.fetchone()     # fetchall() 获取所有记录
    print('getType:'+str(result))
    mycursor.close()
    mydb.close()
    return result


def dbUpdate(name, trashtype):
    dbresult = getType(name)
    if dbresult == None:
        return addType(name, trashtype)
    else:
        return updateType(name, trashtype)


def addType(name, trashtype):
    mydb = mysql.connector.connect(
    host=APIKey.mysql_host,
    user=APIKey.mysql_user,
    passwd=APIKey.mysql_password)
    print('addType:name:%strashtype:%s' % (name, trashtype))
    mycursor = mydb.cursor()
    mycursor.execute('use smarttrash')
    mycursor.execute(
        'INSERT INTO typelist (name, type, time) VALUES ("%s", %s, NOW());' % (name, trashtype))
    mydb.commit()
    mycursor.close()
    mydb.close()
    return mycursor.rowcount


def updateType(name, trashtype):
    mydb = mysql.connector.connect(
    host=APIKey.mysql_host,
    user=APIKey.mysql_user,
    passwd=APIKey.mysql_password)
    print('updateType:name:%strashtype:%s' % (name, trashtype))
    mycursor = mydb.cursor()
    mycursor.execute('use smarttrash')
    mycursor.execute(
        'UPDATE typelist SET type=%s WHERE name="%s"' % (trashtype, name))
    mydb.commit()
    mycursor.close()
    mydb.close()
    return mycursor.rowcount


def addHistory(name, trashtype):
    mydb = mysql.connector.connect(
    host=APIKey.mysql_host,
    user=APIKey.mysql_user,
    passwd=APIKey.mysql_password)
    if type(trashtype) == int:
        trashtype = str(trashtype)
    print('addHistory:name:%strashtype:%s' % (name, trashtype))
    mycursor = mydb.cursor()
    mycursor.execute('use smarttrash')
    mycursor.execute(
        'INSERT INTO history (name, type, time) VALUES ("%s", %s, NOW());' % (name, trashtype))
    mydb.commit()
    mycursor.close()
    mydb.close()
    return mycursor.rowcount


def getHistory():
    mydb = mysql.connector.connect(
    host=APIKey.mysql_host,
    user=APIKey.mysql_user,
    passwd=APIKey.mysql_password)
    mycursor = mydb.cursor()
    mycursor.execute('use smarttrash')
    mycursor.execute('SELECT * FROM history ORDER BY time DESC LIMIT 100')
    result = mycursor.fetchall()     # fetchall() 获取所有记录
    print('getType:'+str(result))
    mycursor.close()
    return result
