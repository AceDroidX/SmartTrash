import tkinter as tk
import main
import image
import hardware
import threading


def startui():
    serverThread = threading.Thread(target=start)
    serverThread.start()


window = None
l = None
b1 = None


def init():
    global window
    global l
    global b1
    window = tk.Tk()
    window.title('SmartTrash')
    window.geometry('1280x720')
    var = tk.StringVar()
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


def run():
    global l
    # result=main.run()
    # l.config(text=result[0]+'\n'+result[1])
    l.config(text='拍摄照片中')
    image.take()
    l.config(text='识别物品中')
    name = image.image_classify(image.image)['result'][0]['keyword']
    l.config(text='这是[%s]\n获取分类中' % (name))
    trashtype = image.getType(
        image.result['result'][0]['keyword']+'/'+image.result['result'][0]['root'])
    l.config(text='这是[%s]\n属于[%s]' % (name, trashtype))
    hardware.run(trashtype)


def start():
    global window
    global l
    global b1
    if window == None:
        init()
    # b1.destroy()
    l = tk.Label(window, bg='white', fg='black', font=('Arial', 12), width=30, height=2)
    l.pack()
    b1 = tk.Button(window, text='拍摄并识别', font=('Arial', 12), width=10, height=1, command=run)
    b1.pack()
    window.mainloop()


if __name__ == '__main__':
    init()
    start()
