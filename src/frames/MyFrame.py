__author__ = 'mariusz'

from Tkinter import *

class MyFrame(Frame):

    def __init__(self, parent, title, minsize):
        self.title = title
        self.minsize = minsize
        parent.root.withdraw()
        self.root = Toplevel()
        Frame.__init__(self, self.root)
        self.parent = parent
        self.init_ui()

        self.root.protocol("WM_DELETE_WINDOW", self.close_window)

    def init_ui(self):
        self.root.resizable(0,0)
        self.root.minsize(*self.minsize)
        self.root.title(self.title)
        self.pack(fill=X)

    def run(self):
        self.root.mainloop()

    def close_window(self):
        self.root.withdraw()
        self.parent.root.deiconify()
        self.parent.root.focus()