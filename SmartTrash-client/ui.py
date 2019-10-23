import tkinter as tk
on_hit = False
def hit_me():
    global on_hit
    if on_hit == False:
        on_hit = True
        var.set('you hit me')
    else:
        on_hit = False
        var.set('')
def init():
    global window
    global l
    global b1
    global var
    window = tk.Tk()
    window.title('My Window')
    window.geometry('500x300')
    var = tk.StringVar()
    l = tk.Label(window, textvariable=var, bg='white', fg='black', font=('Arial', 12), width=30, height=2)
    l.pack()
    b1 = tk.Button(window, text='hit me', font=('Arial', 12), width=10, height=1, command=hit_me)
    b1.pack()
    window.mainloop()
def ontake(path):
    if window==None:
        init()
def yes:
    pass
def no:
    pass
def start:
    pass
if __name__ == '__main__':
    init()
    