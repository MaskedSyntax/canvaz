from tkinter import *
from tkinter import ttk

root = Tk()

frame = ttk.Frame(root, padding=10)
frame.grid()
ttk.Label(frame, text = "Zenith: Background Broswer").grid(column=0, row=0)
ttk.Button(frame, text = "Quit!", command = root.destroy).grid(column=0, row=1)

root.mainloop()
