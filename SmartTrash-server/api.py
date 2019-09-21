import sys
import json
import traceback
gets = [
    "https://laji.lr3800.com/api.php?name=",
    'http://api.choviwu.top/garbage/getGarbage?garbageName=',
    'https://www.lajiflw.cn/rubbish/search?q=',
    'https://quark.sm.cn/api/quark_sug?q='
]
posts = [

]
num = 3


def getURL(name):
    if name == '':
        raise 'name cant be blank'
    if num < len(gets):
        return gets[num]+name
    else:
        print('err:api.num:%ilen:%i' % (num, len(gets)))
        return gets[3]+name


def getResponse(content):
    try:
        jsoncon = json.loads(content)
        response = ''
        if num == 0:
            if jsoncon['msg'] != 'success':
                return 'err:num %i not success' % (num)
            tmplist = {'0': '可回收', '1': '有害', '2': '厨余(湿)', '3': '其他(干)'}
            return tmplist[jsoncon['newslist'][0]['type']]
        elif num == 1:
            if jsoncon['msg'] != 'success':
                return 'err:num %i not success' % (num)
            return jsoncon['data'][0]['gType']
        elif num == 2:
            if jsoncon['msg'] != '获取成功！':
                return 'err:num %i not success' % (num)
            return jsoncon['data'][0]['itemCategory']
        elif num == 3:
            if jsoncon['msg'] != 'succ':
                return 'err:num %i not success' % (num)
            return jsoncon['data']['value'][0]['style']['answer']
        else:
            return 'num %i not exist' % (num)
    except KeyError as e:
        if num == 3:
            return 'err:num %i is not a trash' % (num)
        else:
            raise
    except Exception as e:
        exc_type, exc_value, exc_traceback_obj = sys.exc_info()
        traceback.print_exception(
            exc_type, exc_value, exc_traceback_obj, file=sys.stdout)
        print(content)
        return str(e)
