import tkinter as tk
from tkinter import ttk
import tkinter.scrolledtext as scrolledtext
from tkinter import filedialog as fd
from dotenv import load_dotenv, find_dotenv
import os
import json

class MixoloPy(tk.Tk):

    def __init__(self):
    
        super().__init__()
        self.title("MixoloPy")
        
        self.cat_frame = ttk.Frame(master=self)
        self.cat_tree = ttk.Treeview(master=self.cat_frame)
        self.cat_tree.heading("#0", text="Categories", anchor="w")
        
        recs_loc = self.getRecipesLocation()
        self.updateCatTree()
        
    def getRecipesLocation(self):
        pot_recloc = os.path.join(os.path.dirname(__file__), ".env")
        pot_rec = find_dotenv(pot_recloc)
        if pot_rec == "":
            self.selectRecipesLocation()
        load_dotenv(pot_rec)
                
    def selectRecipesLocation(self):
        recloc = fd.askdirectory(title="Select folder to store recipes...")
        if recloc != '' and recloc != None:
            with open('.env', 'w') as new_recloc_file:
                new_recloc_file.write("RECLOC="+recloc)
        
    def updateCatTree(self):
        pass
        
mixpy = MixoloPy()
mixpy.mainloop()