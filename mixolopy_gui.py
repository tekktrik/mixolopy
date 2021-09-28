import tkinter as tk
from tkinter import ttk
import tkinter.scrolledtext as scrolledtext
from tkinter import filedialog as fd
from dotenv import load_dotenv, find_dotenv
import os
import glob
import json
from PIL import Image, ImageTk
import recipe

class MixoloPy(tk.Tk):

    def __init__(self):
    
        super().__init__()
        self.title("MixoloPy")
        self.resizable(False, False)

        self.screen_height = self.winfo_screenheight()
        self.screen_width = self.winfo_screenwidth()
        
        recs_loc = self.get_recipes_location()
        if recs_loc is None:
            quit()
            
        self.cat_frame = ttk.Frame(master=self, height=100)
        self.cat_frame.grid(column=0, row=0)
        self.cat_tree = None
        self.update_cat_tree()
        
        #self.viewer_frame = ttk.Frame(master=self, width=100, height=100)
        self.viewer_frame = ttk.Frame(master=self, height=100)
        #self.viewer_frame.grid(column=1, row=0, padx=500, pady=500)
        self.viewer_frame.grid(column=1, row=0, ipady=350, ipadx=400)
        self.drink_label = ttk.Label(master=self.viewer_frame, text="")
        self.drink_label.pack()
        self.drink_subtitle = ttk.Label(master=self.viewer_frame, text="")
        self.drink_subtitle.pack()
        #self.drink_label.pack(fill=None, expand=False)
        
    def get_recipes_location(self):
        pot_recloc = os.path.join(os.path.dirname(__file__), ".env")
        pot_rec = find_dotenv(pot_recloc)
        if pot_rec == "":
            self.select_recipes_location()
        load_dotenv(find_dotenv())
        return os.environ.get("RECLOC")
                
    def select_recipes_location(self):
        recloc = fd.askdirectory(title="Select folder to store recipes...")
        if recloc != '' and recloc != None:
            with open('.env', 'w') as new_recloc_file:
                new_recloc_file.write("RECLOC="+recloc)
                
    def show_recipe(self, *args):
        is_recipe = False
        for recipe_obj, recipe_iid in self.recipe_dict.items():
            #print("recipe_obj", type(recipe_obj))
            #print("recipe_iid", type(recipe_iid))
            #print("focus", type(self.cat_tree.focus()))
            if int(self.cat_tree.focus()) == recipe_iid:
                curr_recipe = recipe_obj
                is_recipe = True
                break
        if is_recipe:
            self.drink_label.config(text=curr_recipe.title)
            self.drink_subtitle.config(text=curr_recipe.subtitle)
        
    def update_cat_tree(self):
    
        self.categories = []
        self.recipes = []
        
        rec_folder = os.environ.get("RECLOC")
        rec_glob = glob.glob(rec_folder + "/**/*json", recursive=True)
        cat_glob = glob.glob(rec_folder + "/**/", recursive=True)
        cat_relglob = [os.path.relpath(cat, start=rec_folder) for cat in cat_glob]
        cat_relglob = [cat_name for cat_name in cat_relglob if (cat_name != ".")]
        #rec_relglob = [os.path.relpath(rec, start=rec_folder) for rec in rec_glob]
        rec_relglob = [os.path.abspath(rec) for rec in rec_glob]
        
        for rec in rec_relglob:
            rec_obj = recipe.Recipe(rec, rec_folder)
            self.recipes.append(rec_obj)
        for cat in cat_relglob:
            cat_obj = recipe.RecipeCategory(cat)
            self.categories.append(cat_obj)

        s = ttk.Style(master=self)
        s.configure("Treeview", rowheight=50)
        
        if self.cat_tree is not None:
            self.cat_tree.destroy()
        self.cat_tree = ttk.Treeview(master=self.cat_frame, height=40)
        self.cat_tree.heading("#0", text="Categories", anchor="w")
        self.cat_tree.bind("<ButtonRelease-1>", self.show_recipe)
        
        self.category_dict = {}
        self.recipe_dict = {}
        tree_iid = 0
        
        curr_dir = os.path.dirname(os.path.realpath(__file__))
        img_dir = os.path.join(curr_dir, "images")
        
        cat_img = os.path.join(img_dir, "treeview_category.png")
        cat_img_obj = Image.open(cat_img)
        cat_img_obj = cat_img_obj.resize((int(self.screen_height/50), int(self.screen_width/50)))
        self.cat_img = ImageTk.PhotoImage(cat_img_obj)
        
        rec_img = os.path.join(img_dir, "treeview_recipe.png")
        rec_img_obj = Image.open(rec_img)
        rec_img_obj = rec_img_obj.resize((int(self.screen_height/50), int(self.screen_width/50)))
        self.rec_img = ImageTk.PhotoImage(rec_img_obj)
        
        for cat in self.categories:
            self.cat_tree.insert('', tk.END, text=cat.name, iid=tree_iid, open=False, image=self.cat_img)
            self.category_dict[cat] = tree_iid
            pot_parent = [pot_cat for pot_cat in list(self.category_dict.keys()) if cat.is_child(pot_cat)]
            if len(pot_parent) != 0:
                self.cat_tree.move(self.category_dict[cat], self.category_dict[pot_parent[0]], tk.END)
            tree_iid += 1
            
        for rec in self.recipes:
            self.cat_tree.insert('', tk.END, text=rec.title, iid=tree_iid, open=False, image=self.rec_img)
            self.recipe_dict[rec] = tree_iid
            pot_parent = [pot_cat for pot_cat in list(self.category_dict.keys()) if rec.is_child(pot_cat)]
            if len(pot_parent) != 0:
                self.cat_tree.move(self.recipe_dict[rec], self.category_dict[pot_parent[0]], tk.END)
            tree_iid += 1
        
        self.cat_tree.pack(expand=True)
        
mixpy = MixoloPy()
mixpy.mainloop()
