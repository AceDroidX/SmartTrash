import tkinter as tk
import main
import image
import hardware
import threading
typelist = ['可回收', '有害', '厨余(湿)', '其他(干)']

def startui():
    serverThread = threading.Thread(target=start)
    serverThread.start()


window = None
l = None
b1 = None

    #l = tk.Label(window, textvariable=var, bg='white', fg='black', font=('Arial', 12), width=30, height=2)
    # l.pack()
    #b1 = tk.Button(window, text='hit me', font=('Arial', 12), width=10, height=1, command=hit_me)
    # b1.pack()
    #b2 = tk.Button(window, text='hit me', font=('Arial', 12), width=10, height=1, command=hit_me)
    # b2.pack()
    # window.mainloop()


def ontake(path):
    if window == None:
        init()

def updateui():
    global w2
    w2 = tk.Tk()
    w2.title('SmartTrash')
    w2.geometry('1280x720')
    l = tk.Label(w2,text='您觉得这应该是什么垃圾', bg='white', fg='black', font=('Arial', 24), width=40, height=4).pack()
    tk.Button(w2, text=typelist[0]+'垃圾', font=('Arial', 24), width=20, height=2, command=lambda:updatetype(name,0)).pack()
    tk.Button(w2, text=typelist[1]+'垃圾', font=('Arial', 24), width=20, height=2, command=lambda:updatetype(name,1)).pack()
    tk.Button(w2, text=typelist[2]+'垃圾', font=('Arial', 24), width=20, height=2, command=lambda:updatetype(name,2)).pack()
    tk.Button(w2, text=typelist[3]+'垃圾', font=('Arial', 24), width=20, height=2, command=lambda:updatetype(name,3)).pack()
    w2.mainloop()

def updatetype(name,ttype):
    global trashtype
    image.updatetype(name,ttype)
    w2.destroy()
    if trashtype.find('无分类')!=-1:
        hardware.run(ttype)
        trashtype='已提交错误'

def run():
    global l
    global name
    global trashtype
    global window
    # result=main.run()
    # l.config(text=result[0]+'\n'+result[1])
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


def start():
    global window
    global l
    global wrong
    global b1
    window = tk.Tk()
    window.title('SmartTrash')
    window.geometry('1280x720')
    var = tk.StringVar()
    # b1.destroy()
    l = tk.Label(window, bg='white', fg='black', font=('Arial', 24), width=60, height=4)
    l.pack()
    take = tk.Button(window, text='拍摄并识别', font=('Arial', 24), width=20, height=2, command=run)
    take.pack()
    if main.usedist:
        take.config(text='自动识别已开启')
        take.config(state='disabled')
    wrong = tk.Button(window, text='觉得分类有问题？点击提交错误', font=('Arial', 24), width=25, height=2, command=updateui,state='disabled')
    wrong.pack()
    window.mainloop()


if __name__ == '__main__':
    start()
