import tkinter as tk
var = tk.StringVar()
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
    window = tk.Tk()
    window.title('My Window')
    window.geometry('500x300')
    l = tk.Label(window, textvariable=var, bg='white', fg='black', font=('Arial', 12), width=30, height=2)
    l.pack()
    b = tk.Button(window, text='hit me', font=('Arial', 12), width=10, height=1, command=hit_me)
    b.pack()
    window.mainloop()