import mysql.connector
import APIKey

mydb = mysql.connector.connect(
    host=APIKey.mysql_host,
    user=APIKey.mysql_user,
    passwd=APIKey.mysql_password
)


def getType(name):
    mycursor = mydb.cursor()
    mycursor.execute('use smarttrash')
    mycursor.execute('SELECT type FROM typelist WHERE name="%s"' % (name))
    result = mycursor.fetchone()     # fetchall() 获取所有记录
    print('getType:'+str(result))
    mycursor.close()
    return result


def dbUpdate(name, trashtype):
    dbresult = getType(name)
    if dbresult == None:
        return addType(name, trashtype)
    else:
        return updateType(name, trashtype)


def addType(name, trashtype):
    print('addType:name:%strashtype:%s' % (name, trashtype))
    mycursor = mydb.cursor()
    mycursor.execute('use smarttrash')
    mycursor.execute(
        'INSERT INTO typelist (name, type, time) VALUES ("%s", %s, NOW());' % (name, trashtype))
    mydb.commit()
    mycursor.close()
    return mycursor.rowcount


def updateType(name, trashtype):
    print('updateType:name:%strashtype:%s' % (name, trashtype))
    mycursor = mydb.cursor()
    mycursor.execute('use smarttrash')
    mycursor.execute(
        'UPDATE typelist SET type=%s WHERE name="%s"' % (trashtype, name))
    mydb.commit()
    mycursor.close()
    return mycursor.rowcount


def addHistory(name, trashtype):
    if type(trashtype) == int:
        trashtype = str(trashtype)
    print('addHistory:name:%strashtype:%s' % (name, trashtype))
    mycursor = mydb.cursor()
    mycursor.execute('use smarttrash')
    mycursor.execute(
        'INSERT INTO history (name, type, time) VALUES ("%s", %s, NOW());' % (name, trashtype))
    mydb.commit()
    mycursor.close()
    return mycursor.rowcount


def getHistory():
    mycursor = mydb.cursor()
    mycursor.execute('use smarttrash')
    mycursor.execute('SELECT * FROM history ORDER BY time DESC LIMIT 100')
    result = mycursor.fetchall()     # fetchall() 获取所有记录
    print('getType:'+str(result))
    mycursor.close()
    return result
