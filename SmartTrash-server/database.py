import mysql.connector
import APIKey
typelist = ['可回收', '有害', '厨余(湿)', '其他(干)']

def connect():
    global mydb
    global mycursor
    mydb = mysql.connector.connect(
    host=APIKey.mysql_host,
    user=APIKey.mysql_user,
    passwd=APIKey.mysql_password)
    mycursor = mydb.cursor()
    return mycursor

def close():
    global mydb
    global mycursor
    mycursor.close()
    mydb.close()
    
def getType(name):
    global mydb
    global mycursor
    connect()
    mycursor.execute('use smarttrash')
    mycursor.execute('SELECT type FROM typelist WHERE name="%s"' % (name))
    result = mycursor.fetchone()     # fetchall() 获取所有记录
    print('database.getType:'+str(result))
    close()
    return result


def dbUpdate(name, trashtype):
    dbresult = getType(name)
    if dbresult == None:
        return addType(name, trashtype)
    else:
        return updateType(name, trashtype)


def addType(name, trashtype):
    global mydb
    global mycursor
    connect()
    print('database.addType:name:%strashtype:%s' % (name, trashtype))
    mycursor = mydb.cursor()
    mycursor.execute('use smarttrash')
    mycursor.execute(
        'INSERT INTO typelist (name, type, time) VALUES ("%s", %s, NOW());' % (name, trashtype))
    mydb.commit()
    close()
    return mycursor.rowcount


def updateType(name, trashtype):
    global mydb
    global mycursor
    connect()
    print('database.updateType:name:%strashtype:%s' % (name, trashtype))
    mycursor = mydb.cursor()
    mycursor.execute('use smarttrash')
    mycursor.execute(
        'UPDATE typelist SET type=%s WHERE name="%s"' % (trashtype, name))
    mydb.commit()
    close()
    return mycursor.rowcount


def addHistory(name, trashtype):
    global mydb
    global mycursor
    connect()
    if type(trashtype) == int:
        trashtype = str(trashtype)
    print('database.addHistory:[name:%strashtype:%s]' % (name, trashtype))
    mycursor = mydb.cursor()
    mycursor.execute('use smarttrash')
    mycursor.execute(
        'INSERT INTO history (name, type, time) VALUES ("%s", %s, NOW());' % (name, trashtype))
    mydb.commit()
    close()
    return mycursor.rowcount


def getHistory(mode=0):
    global mydb
    global mycursor
    connect()
    mycursor = mydb.cursor()
    mycursor.execute('use smarttrash')
    if mode==3:
        mycursor.execute('SELECT * FROM history ORDER BY time DESC LIMIT 10')
    else:
        mycursor.execute('SELECT * FROM history ORDER BY time DESC LIMIT 100')
    result = mycursor.fetchall()     # fetchall() 获取所有记录
    #print('getType:'+str(result))
    close()
    if mode==3:
        tmp=[]
        tmp.append('垃圾识别历史记录:')
        for item in result:
            oneresult='垃圾名:%s  类型:%s  识别时间:%s'%(item[1],typelist[int(item[2])],item[3])
            tmp.append(oneresult)
        result=tmp
    return result
