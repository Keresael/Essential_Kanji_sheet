from tkinter import *
from tkinter import ttk

gui = Tk()
gui.title("Essential Kanji sheet")

gui.geometry("800x400")
mainframe = ttk.Frame(gui, padding=(3, 3, 12, 12))
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))

Kanji = StringVar()
Kanji = ttk.Entry(mainframe, width=7, textvariable=Kanji)
Kanji.grid(column=2, row=1, sticky=(W, E))
ttk.Label(mainframe, text="Kanji").grid(column=3, row=1, sticky=W)

gui.mainloop()