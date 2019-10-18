import sys
import json
import traceback
import urllib.parse
import string
import APIKey
thkey = APIKey.th_key
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


def getResponse(name, content,mode):
    try:
        jsoncon = json.loads(content)
        response = ''
        with open('response-api.json', 'w',encoding='utf-8') as f:
            f.write(content)
            f.write("\n")
        if num == 0 or num == 5:
            if content.find('250')!=-1:
                return '很抱歉，您当前搜索的[%s]暂无分类结果，请您通过“垃圾图鉴”查询'%(name)
            if jsoncon['msg'] != 'success':
                return '[%s]err:分类检索失败-num %i not success' % (name, num)
            #tmplist = {'0': '可回收', '1': '有害', '2': '厨余(湿)', '3': '其他(干)'}
            tmplist = ['可回收', '有害', '厨余(湿)', '其他(干)']
            if mode==0:
                return tmplist[jsoncon['newslist'][0]['type']]
            elif mode==1:
                trashtype=tmplist[jsoncon['newslist'][0]['type']]
                explain=jsoncon['newslist'][0]['explain']
                contain=jsoncon['newslist'][0]['contain']
                tip=jsoncon['newslist'][0]['tip']
                return '您当前搜索的是[%s]，属于[%s]垃圾\n\n分类解释:%s\n\n包含类型:%s\n\n投放提示:%s'%(name,trashtype,explain,contain,tip)
            else:
                return 'err:mode'
        elif num == 1:
            if jsoncon['msg'] != 'success':
                return '[%s]分类检索失败-num %i not success' % (name, num)
            return jsoncon['data'][0]['gType']
        elif num == 2:
            if jsoncon['msg'] != '获取成功！':
                return '[%s]分类检索失败-num %i not success' % (name, num)
            return jsoncon['data'][0]['itemCategory']
        elif num == 3:
            if jsoncon['msg'] != 'succ':
                return '[%s]分类检索失败-num %i not success' % (name, num)
            return jsoncon['data']['value'][0]['style']['answer']
        elif num == 4:
            return jsoncon['type']
        else:
            return '[%s]分类检索失败-num %i not exist' % (name, num)
    except KeyError as e:
        if num == 3:
            return 'err:[%s]分类检索失败-num %i is not a trash' % (name, num)
        elif num == 4:
            return 'err:[%s]分类检索失败-num %i is not a trash' % (name, num)
        else:
            raise
    except Exception as e:
        exc_type, exc_value, exc_traceback_obj = sys.exc_info()
        traceback.print_exception(
            exc_type, exc_value, exc_traceback_obj, file=sys.stdout)
        print(content)
        return str(e)
