import tkinter as tk
import main
import threading

def startui():
    serverThread = threading.Thread(target=start)
    serverThread.start()

window=None
l=None
b1=None

def init():
    global window
    global l
    global b1
    global var
    window = tk.Tk()
    window.title('My Window')
    window.geometry('500x300')
    var = tk.StringVar()
    #l = tk.Label(window, textvariable=var, bg='white', fg='black', font=('Arial', 12), width=30, height=2)
    #l.pack()
    #b1 = tk.Button(window, text='hit me', font=('Arial', 12), width=10, height=1, command=hit_me)
    #b1.pack()
    #b2 = tk.Button(window, text='hit me', font=('Arial', 12), width=10, height=1, command=hit_me)
    #b2.pack()
    #window.mainloop()
def ontake(path):
    if window==None:
        init()
def run():
    global var
    global l
    result=main.run()
    l.text=result[0]+'\n'+result[1]
def yes():
    pass
def no():
    pass
def start():
    global window
    global l
    global b1
    global var
    if window==None:
        init()
    #b1.destroy()
    l = tk.Label(window, bg='white', fg='black', font=('Arial', 12), width=30, height=2)
    l.pack()
    b1 = tk.Button(window, text='拍摄并识别', font=('Arial', 12), width=10, height=1, command=run)
    b1.pack()
    window.mainloop()
if __name__ == '__main__':
    init()
    start()
    