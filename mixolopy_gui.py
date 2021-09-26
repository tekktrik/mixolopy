import tkinter as tk
from tkinter import ttk
import tkinter.scrolledtext as scrolledtext
from tkinter import filedialog as fd
from dotenv import load_dotenv, find_dotenv
import os
import glob
import json
import recipe

class MixoloPy(tk.Tk):

    def __init__(self):
    
        super().__init__()
        self.title("MixoloPy")
        
        recs_loc = self.getRecipesLocation()
        if recs_loc is None:
            quit()
            
        self.cat_frame = ttk.Frame(master=self)
        self.cat_frame.grid(column=0, row=0)
        self.cat_tree = None
        self.updateCatTree()
        
    def getRecipesLocation(self):
        pot_recloc = os.path.join(os.path.dirname(__file__), ".env")
        pot_rec = find_dotenv(pot_recloc)
        if pot_rec == "":
            self.selectRecipesLocation()
        load_dotenv(find_dotenv())
        return os.environ.get("RECLOC")
                
    def selectRecipesLocation(self):
        recloc = fd.askdirectory(title="Select folder to store recipes...")
        if recloc != '' and recloc != None:
            with open('.env', 'w') as new_recloc_file:
                new_recloc_file.write("RECLOC="+recloc)
        
    def updateCatTree(self):
    
        self.categories = []
        rec_folder = os.environ.get("RECLOC")
        rec_glob = glob.glob(rec_folder + "/**/*json", recursive=True)
        cat_glob = glob.glob(rec_folder + "/**/", recursive=True)
        cat_relglob = [os.path.relpath(cat, start=rec_folder) for cat in cat_glob]
        cat_relglob = [cat_name for cat_name in cat_relglob if (cat_name != ".")]
        rec_relglob = [os.path.relpath(rec, start=rec_folder) for rec in rec_glob]
        for rec in rec_relglob:
            print(rec)
        print("-----------")
        for cat in cat_relglob:
            cat_obj = recipe.RecipeCategory(cat)
            print(cat_obj.getRelativePath())
            self.categories.append(cat_obj)
            
        print(self.categories)
        
        if self.cat_tree is not None:
            self.cat_tree.destroy()
        self.cat_tree = ttk.Treeview(master=self.cat_frame)
        self.cat_tree.heading("#0", text="Categories", anchor="w")
        
        self.category_dict = {}
        cat_id = 0
        
        for cat in self.categories:
            self.cat_tree.insert('', tk.END, text=cat.name, id=cat_id, open=False)
        
        self.cat_tree.pack()
        
mixpy = MixoloPy()
mixpy.mainloop()