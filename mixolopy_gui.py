import tkinter as tk
from tkinter import ttk
import tkinter.scrolledtext as scrolledtext
import json

class MixoloPy(tk.Tk):

    super()
    self.title("MixoloPy")
    
    cat_frame = ttk.Frame(master=self)
    tree = ttk.Treeview(master=self)
    tree