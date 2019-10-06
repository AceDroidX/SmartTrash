import sys
import json
import traceback
import urllib.parse
import string
import APIKey
try:
    thkey = APIKey.th_key
except:
    thkey = "null"
    print('th:null')
gets = [
    "https://laji.lr3800.com/api.php?name=",
    'http://api.choviwu.top/garbage/getGarbage?garbageName=',
    'https://www.lajiflw.cn/rubbish/search?q=',
    'https://quark.sm.cn/api/quark_sug?q=',
    'https://nodeapi.yunser.com/waste/search?name=',
    'https://api.tianapi.com/txapi/lajifenlei?num=5&key=%s&word=' % (thkey)
]
posts = [

]
num = 5


def getURL(name):
    if name == '':
        raise 'name cant be blank'
    if num < len(gets):
        return urllib.parse.quote(gets[num]+name, safe=string.printable)
    else:
        print('err:api.num:%ilen:%i' % (num, len(gets)))
        return urllib.parse.quote(gets[3]+name, safe=string.printable)


def getResponse(name, content):
    try:
        jsoncon = json.loads(content)
        response = ''
        with open('response.txt', 'w') as f:
            f.write(content)
            f.write("\n-------------\n")
        if num == 0 or num == 5:
            if jsoncon['msg'] != 'success':
                return {'type': 1, 'name': name, 'num': num}
            #tmplist = {'0': '可回收', '1': '有害', '2': '厨余(湿)', '3': '其他(干)'}
            tmplist = ['可回收', '有害', '厨余(湿)', '其他(干)']
            return tmplist[jsoncon['newslist'][0]['type']]
        elif num == 1:
            if jsoncon['msg'] != 'success':
                return {'type': 1, 'name': name, 'num': num}
            return jsoncon['data'][0]['gType']
        elif num == 2:
            if jsoncon['msg'] != '获取成功！':
                return {'type': 1, 'name': name, 'num': num}
            return jsoncon['data'][0]['itemCategory']
        elif num == 3:
            if jsoncon['msg'] != 'succ':
                return {'type': 1, 'name': name, 'num': num}
            return jsoncon['data']['value'][0]['style']['answer']
        elif num == 4:
            return jsoncon['type']
        else:
            return {'type': 3, 'name': name, 'num': num}
    except KeyError as e:
        if num == 3:
            return {'type': 2, 'name': name, 'num': num}
        elif num == 4:
            return {'type': 2, 'name': name, 'num': num}
        else:
            raise
    except Exception as e:
        exc_type, exc_value, exc_traceback_obj = sys.exc_info()
        traceback.print_exception(
            exc_type, exc_value, exc_traceback_obj, file=sys.stdout)
        print(content)
        return str(e)


def getType(name, content, root):#todo:需要添加物品类别判断
    response = getResponse(name, content)
    result = ''
    if type(response) == dict:
        if response['type'] == 1:
            result = 'err:[%s]分类检索失败-num %i not success' % (
                response['name'], response['num'])
        elif response['type'] == 2:
            result = 'err:[%s]分类检索失败-num %i is not a trash' % (
                response['name'], response['num'])
        elif response['type'] == 3:
            result = 'err:[%s]分类检索失败-num %i not exist' % (
                response['name'], response['num'])
    elif type(response) == str:
        result = response
    else:
        result = 'err:unknown var type'
    return result
