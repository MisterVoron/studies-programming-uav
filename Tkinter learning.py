import tkinter
from tkinter import ttk


def clicked():
    res = f'Hello {txt.get()}'
    lbl.configure(text=res)


window = tkinter.Tk()
window.title('Welcome in python application')
window.geometry('500x500')
lbl = tkinter.Label(window, text='Hello', font=('Arial Bond', 30))
lbl.grid(column=0, row=0)
txt = tkinter.Entry(window, width=10)
txt.grid(column=1, row=0)
button = tkinter.Button(window, text='Click me!', bg='green', fg='black', command=clicked)
button.grid(column=2, row=0)
combo = ttk.Combobox(window)
combo['value'] = (0, 1, 2, 3, 4, 'Tuturu')
combo.current(1)
combo.grid(column=3, row=0)
chk_state = tkinter.BooleanVar()
chk_state.set(False)
chk = ttk.Checkbutton(window, text='something', variable=chk_state)
chk.grid(column=4, row=0)
rad1 = tkinter.Radiobutton(window, text='One', value=1)
rad2 = tkinter.Radiobutton(window, text='Two', value=2)
rad1.grid(column=0, row=1)
rad2.grid(column=0, row=2)
window.mainloop()
