__author__ = 'mpasek'

from Tkinter import *

class MyEntry(object):

    counter = 0

    def __init__(self):
        MyEntry.counter += 1

class TextEntry(MyEntry):

    def __init__(self, parent, title):
        MyEntry.__init__(self)
        Label(parent, text=title, anchor = W, width = 1).grid(column=0, row=(MyEntry.counter-1), sticky='NESW')
        self.var = StringVar()

        entry = Entry(parent, width=1, textvariable=self.var)
        entry.grid(column=1, row=(MyEntry.counter-1), sticky='NESW')

    def get_value(self):
        return self.var.get()

    def set_value(self, value):
        self.var.set(value)

class CheckEntry(MyEntry):

    def __init__(self, parent, title):
        MyEntry.__init__(self)
        self.var = IntVar()
        Checkbutton(parent, text=title, anchor=W, variable=self.var, width=0).grid(sticky='NESW', columnspan=2, row=(MyEntry.counter-1))

    def get_value(self):
        return self.var.get()

    def set_value(self, value):
        return self.var.set(value)
