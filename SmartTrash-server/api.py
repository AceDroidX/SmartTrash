import sys
import json
import traceback
import urllib.parse
import string
import APIKey,database,main
thkey = APIKey.th_key
typelist = ['可回收', '有害', '厨余(湿)', '其他(干)']
type_url='https://api.tianapi.com/txapi/lajifenlei?num=5&key=%s&word=' % (thkey)

def getType(name,mode=0):
    name=urllib.parse.unquote(name)
    if main.usedb:
        dbresult=database.getType(name)
        if dbresult!=None:
            result=dbresult[0]
            if mode!=2:
                database.addHistory(name,result)
            print('api.getType.result:'+typelist[result])
            return typelist[result]
    url = urllib.parse.quote(type_url+name, safe=string.printable)
    print('api.getType.fullurl:'+url)
    req = urllib.request.Request(url)
    req.add_header(
        'User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.35 Safari/537.36')
    r = urllib.request.urlopen(req)
    result = getResponse(name,r.read().decode('utf-8'),mode)
    if type(result)==int:
        if main.usedb:
            database.addHistory(name,result)
        result=typelist[result]
    print('api.getType.result:'+result)
    return result

def getType_multi(namelist):
    tmp=[]
    for name in namelist:
        tmp.append(getType(name,2))
    print("api.getType_multi:"+str(tmp))
    return tmp

def getResponse(name, content,mode):
    try:
        jsoncon = json.loads(content)
        response = ''
        if content.find('250')!=-1:
            if mode==2:
                return '很抱歉，您当前搜索的[%s]暂无分类结果，请您提交错误'%(name)
            return '很抱歉，您当前搜索的[%s]暂无分类结果，请您通过“垃圾图鉴”查询'%(name)
        if jsoncon['msg'] != 'success':
            return '[%s]err:分类检索失败-not success' % (name)
        #typelist = {'0': '可回收', '1': '有害', '2': '厨余(湿)', '3': '其他(干)'}
        #typelist = ['可回收', '有害', '厨余(湿)', '其他(干)']
        if mode==0:
            return jsoncon['newslist'][0]['type']
        elif mode==1:
            trashtype=typelist[jsoncon['newslist'][0]['type']]
            explain=jsoncon['newslist'][0]['explain']
            contain=jsoncon['newslist'][0]['contain']
            tip=jsoncon['newslist'][0]['tip']
            return '您当前搜索的是[%s]，属于[%s]垃圾\n\n分类解释:%s\n\n包含类型:%s\n\n投放提示:%s'%(name,trashtype,explain,contain,tip)
        else:
            return 'err:mode'
    except KeyError as e:
        return 'err:[%s]分类检索失败-is not a trash' % (name)
    except Exception as e:
        exc_type, exc_value, exc_traceback_obj = sys.exc_info()
        traceback.print_exception(
            exc_type, exc_value, exc_traceback_obj, file=sys.stdout)
        print(content)
        return str(e)
