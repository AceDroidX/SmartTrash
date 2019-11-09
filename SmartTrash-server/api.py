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
            if mode!=2 or mode!=3:
                database.addHistory(name,result)
            #print('api.getType.result:'+typelist[result])
            if mode==3:
                return getmore(name,result)
            else:
                return typelist[result]
    url = urllib.parse.quote(type_url+name, safe=string.printable)
    #print('api.getType.fullurl:'+url)
    req = urllib.request.Request(url)
    req.add_header(
        'User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.35 Safari/537.36')
    r = urllib.request.urlopen(req)
    result = getResponse(name,r.read().decode('utf-8'),mode)
    if type(result)==int:
        if main.usedb and (mode!=2 or mode!=3):
            database.addHistory(name,result)
        result=typelist[result]
    #print('api.getType.result:'+result)
    return result

def getType_multi(namelist,mode=2):
    tmp=[]
    for name in namelist:
        tmp.append(getType(name,mode))
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
        elif mode==1 or mode==3:
            trashtype=typelist[jsoncon['newslist'][0]['type']]
            explain=jsoncon['newslist'][0]['explain']
            contain=jsoncon['newslist'][0]['contain']
            tip=jsoncon['newslist'][0]['tip']
            return getmore(name,trashtype,explain,contain,tip)
        else:
            return jsoncon['newslist'][0]['type']
    except KeyError as e:
        return 'err:[%s]分类检索失败-is not a trash' % (name)
    except Exception as e:
        exc_type, exc_value, exc_traceback_obj = sys.exc_info()
        traceback.print_exception(
            exc_type, exc_value, exc_traceback_obj, file=sys.stdout)
        print(content)
        return str(e)


def getmore(name,trashtype,explain='',contain='',tip=''):
    if explain=='' or contain=='' or tip=='':
        explains = ['可回收垃圾是指适宜回收、可循环利用的生活废弃物。','有毒有害垃圾是指存有对人体健康有害的重金属、有毒的物质或者对环境造成现实危害或者潜在危害的废弃物。','厨余垃圾是指居民日常生活及食品加工、饮食服务、单位供餐等活动中产生的垃圾。','干垃圾即其它垃圾，指除可回收物、有害垃圾、厨余垃圾（湿垃圾）以外的其它生活废弃物。']
        contains = ['常见包括各类废金属、玻璃瓶、易拉罐、饮料瓶、塑料玩具、书本、报纸、广告单、纸板箱、衣服、床上用品、电子产品等','常见包括废电池、废荧光灯管、废灯泡、废水银温度计、废油漆桶、过期药品、农药、杀虫剂等。','常见包括菜叶、剩菜、剩饭、果皮、蛋壳、茶渣、骨头等','常见包括砖瓦陶瓷、渣土、卫生间废纸、猫砂、污损塑料、毛发、硬壳、一次性制品、灰土、瓷器碎片等难以回收的废弃物']
        tips = ['轻投轻放；清洁干燥，避免污染，费纸尽量平整；立体包装物请清空内容物，清洁后压扁投放；有尖锐边角的、应包裹后投放','分类投放有害垃圾时，应注意轻放。其中：废灯管等易破损的有害垃圾应连带包装或包裹后投放；废弃药品宜连带包装一并投放；杀虫剂等压力罐装容器，应排空内容物后投放；在公共场所产生有害垃圾且未发现对应收集容器时，应携带至有害垃圾投放点妥善投放。','纯流质的食物垃圾、如牛奶等，应直接倒进下水口。有包装物的湿垃圾应将包装物去除后分类投放、包装物请投放到对应的可回收物或干垃圾容器','尽量沥干水分；难以辨识类别的生活垃圾都可以投入干垃圾容器内']
        explain=explains[trashtype]
        contain=contains[trashtype]
        tip=tips[trashtype]
        trashtype=typelist[trashtype]
    print('api.getmore:'+'您当前搜索的是[%s]，属于[%s]垃圾\n\n分类解释:%s\n\n包含类型:%s\n\n投放提示:%s'%(name,trashtype,explain,contain,tip))
    return '您当前搜索的是[%s]，属于[%s]垃圾\n\n分类解释:%s\n\n包含类型:%s\n\n投放提示:%s'%(name,trashtype,explain,contain,tip)