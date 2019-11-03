import tkinter as tk
import main
import image
import hardware
import threading,json,time
typelist = ['可回收', '有害', '厨余(湿)', '其他(干)']

def startui():
    serverThread = threading.Thread(target=start)
    serverThread.start()

window = None
l = None
b1 = None

sleeptime=10

def ontake(path):
    if window == None:
        init()

def updateui():
    global w2
    global name
    w2 = tk.Tk()
    w2.title('SmartTrash')
    w2.geometry('1280x720')
    l = tk.Label(w2,text='您觉得[%s]应该是什么垃圾'%(name), bg='white', fg='black', font=('Arial', 24), width=40, height=4).pack()
    for i in range(4):
        tk.Button(w2, text=typelist[i]+'垃圾', font=('Arial', 24), width=20, height=2, command=lambda arg2=i,arg1=name:updatetype(arg1,arg2)).pack()
    w2.mainloop()

def historyui():
    global history
    history.delete(0,history.size()-1)
    history.insert("end", '垃圾投入历史记录')
    result=json.loads(image.getHistory())
    for item in result:
        oneresult='垃圾名:%s  类型:%s  投入时间:%s'%(item[1],typelist[int(item[2])],item[3])
        history.insert("end", oneresult)
        
def updatetype(name,ttype):
    global trashtype
    image.updatetype(name,ttype)
    print('ui.updatetype:name=%s type=%s'%(name,ttype))
    if main.usemulti:
        image.addHistory(name,trashtype)
        historyui()
    w2.destroy()
    if trashtype.find('无分类')!=-1:
        hardware.run(ttype)
        trashtype='已提交错误'

def selectname(num):
    global selectnum
    global resttime
    selectnum=num
    resttime=0
    print("ui.selectname.num="+str(num))

def run():
    global l
    global name
    global trashtype
    global window
    l.config(text='拍摄照片中')
    image.take()
    l.config(text='识别物品中')
    name = image.image_classify(image.image)['result'][0]['keyword']
    l.config(text='您识别的垃圾是[%s]\n获取分类中' % (name))
    trashtype = image.getType(
        image.result['result'][0]['keyword']+'/'+image.result['result'][0]['root'])
    if trashtype.find('无分类')==-1:
        l.config(text='您识别的垃圾是[%s]\n您识别的垃圾属于[%s]' % (name, trashtype))
        wrong.config(state='normal')
        hardware.run(trashtype)
    else:
        l.config(text='这是[%s]\n%s' % (name, trashtype))
        wrong.config(state='normal')
    historyui()

def run_multi():
    global l
    global name
    global trashtype
    global window
    global selectbtn
    global selectnum
    global resttime
    wrong.config(state='disabled')
    l.config(text='拍摄照片中')
    image.take()
    l.config(text='识别物品中')
    ic=image.image_classify(image.image)
    if str(ic).find('err')!=-1:
        l.config(text='物品识别错误')
        print(str(ic))
        return
    ic=json.loads(json.dumps(ic).replace('/',','))
    namelist=[]
    for i in range(ic['result_num']):
        namelist.append(ic['result'][i]['keyword'])
    print('ui.run_multi.namelist:'+str(namelist))
    finalname=[]
    for i in range(4):
        if i==0 or ic['result'][i]['score']>=0.05:
            finalname.append(namelist[i])
            selectbtn[i].config(state='disabled',text='这是[%s]\n获取分类中' % (namelist[i]))
        else:
            selectbtn[i].config(state='disabled',text='')
    print('ui.run_multi.finalname:'+str(finalname))
    typelist=json.loads(image.getType_multi(finalname))
    print('ui.run_multi.typelist:'+str(typelist))
    for i in range(len(typelist)):
        if typelist[i].find('无分类')==-1:
            selectbtn[i].config(state='normal',text='这是[%s]\n属于[%s]' % (finalname[i], typelist[i]))
        else:
            selectbtn[i].config(state='normal',text='这是[%s]\n%s' % (finalname[i], '暂无分类结果'))
    selectnum=0
    resttime=sleeptime
    l.config(text='请选出相对正确的结果\n%s秒后默认选择第一个结果'%(str(sleeptime)))
    while resttime>0:
        time.sleep(0.1)
        resttime=resttime-0.1
    #wrong.config(state='normal')
    for i in range(4):
        selectbtn[i].config(text='',state='disabled')
    name=finalname[selectnum]
    trashtype=typelist[selectnum]
    if trashtype.find('无分类')==-1:
        l.config(text='您识别的垃圾是[%s]\n您识别的垃圾属于[%s]' % (name, trashtype))
        wrong.config(state='normal')
        hardware.run(trashtype)
        image.addHistory(name,trashtype)
        historyui()
    else:
        l.config(text='这是[%s]\n%s' % (name, trashtype))
        wrong.config(state='normal')
    #hardware.run(trashtype)

def start():
    global window
    global l
    global wrong
    global b1
    global history
    global selectbtn
    window = tk.Tk()
    window.title('SmartTrash')
    window.geometry('1280x720')
    var = tk.StringVar()
    # b1.destroy()
    l = tk.Label(window, bg='white', fg='black', font=('Arial', 24), width=60, height=4)
    l.pack()
    if main.usemulti:
        fm=tk.Frame(window)
        selectbtn=[]
        for i in range(4):
            selectbtn.append(tk.Button(fm, text='', font=('Arial', 24), width=15, height=2, command=lambda arg=i:selectname(arg),state='disabled'))
            selectbtn[i].pack(side='left')
        fm.pack()
    else:
        take = tk.Button(window, text='拍摄并识别', font=('Arial', 24), width=20, height=2, command=run)
        take.pack()
        if main.usedist:
            take.config(text='自动识别已开启')
            take.config(state='disabled')
    wrong = tk.Button(window, text='觉得分类有问题？点击提交错误', font=('Arial', 24), width=25, height=2, command=updateui,state='disabled')
    wrong.pack()
    if main.uihistory:
        fmh=tk.Frame(window)
        history = tk.Listbox(window,font=('Arial', 24),width=60,height=10)
        history.pack()
        #sb = tk.Scrollbar(fmh,command=history.yview)
        #sb.pack(side='right',fill='y')
        #history.config(yscrollcommand=sb.set)
        history.insert("end", '垃圾投入历史记录')
        historyui()
    window.mainloop()

if __name__ == '__main__':
    start()
