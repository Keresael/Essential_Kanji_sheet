from tkinter import *
from tkinter import ttk
from pdf_builder import *

def main():
    gui = Tk()
    gui.title("Essential Kanji sheet")

    gui.geometry("800x400")

    mainframe = ttk.Frame(gui, padding=(3, 3, 12, 12))
    mainframe.grid(column=0, row=0, sticky=N)

    kanji = StringVar()
    kanji = ttk.Entry(mainframe, width=7, textvariable=kanji)
    kanji.grid(column=2, row=1, sticky=N)
    ttk.Label(mainframe, text="Kanji").grid(column=3, row=1, sticky=W)
    pdf_builder(kanji)

    gui.mainloop()