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
        #prev_width_ = 1200
        #prev_height = 1000
        #curr_width_laptop = 1700
        #curr_height_laptop = 960
        #curr_width_desktop = 2560
        #curr_height_desktop = 1440
        self.resizable(False, False)

        self.screen_height = self.winfo_screenheight()
        self.screen_width = self.winfo_screenwidth()
        
        print("height", self.screen_height)
        print("width", self.screen_width)
        
        self.gui_width = int(self.screen_width/(3/2))
        self.gui_height = int(self.screen_height/(2.5/2))
        self.geometry(str(self.gui_width) + "x" + str(self.gui_height))
        
        recs_loc = self.get_recipes_location()
        if recs_loc is None:
            quit()
            
        curr_dir = os.path.dirname(os.path.realpath(__file__))
        img_dir = os.path.join(curr_dir, "images")
        
        cat_img = os.path.join(img_dir, "treeview_category.png")
        cat_img_obj = Image.open(cat_img)
        #cat_img_obj = cat_img_obj.resize((int(self.screen_height/100), int(self.screen_height/100)))
        cat_img_obj = cat_img_obj.resize((15, 15))
        self.cat_img = ImageTk.PhotoImage(cat_img_obj)
        
        rec_img = os.path.join(img_dir, "treeview_recipe.png")
        rec_img_obj = Image.open(rec_img)
        rec_img_obj = rec_img_obj.resize((15, 15))
        self.rec_img = ImageTk.PhotoImage(rec_img_obj)
            
        self.cat_frame = ttk.Frame(master=self, width=20)
        #self.cat_frame.grid(column=0, row=0)
        self.cat_frame.pack(side=tk.LEFT)
        self.cat_tree = None
        self.update_cat_tree()
        
        self.viewer_frame = ttk.Frame(master=self, width=1000)
        
        self.drink_label_frame = ttk.Frame(master=self.viewer_frame)
        self.drink_label = ttk.Label(master=self.drink_label_frame, text="", font=20)
        self.drink_label.bind("<Button-1>", self.user_edit_drink_name)
        self.drink_label.pack()
        self.drink_label_frame.pack(fill=tk.NONE, pady=(100, 10))
        
        self.drink_subtitle_frame = ttk.Frame(master=self.viewer_frame)
        self.drink_subtitle = ttk.Label(master=self.drink_subtitle_frame, text="")
        self.drink_subtitle.bind("<Button-1>", self.user_edit_drink_subtitle)
        self.drink_subtitle.pack()
        self.drink_subtitle_frame.pack(fill=tk.NONE, pady=10)
        
        self.opinion_frame = ttk.Frame(master=self.viewer_frame)
        self.rating_label = ttk.Label(master=self.opinion_frame, text="")
        self.rating_label.grid(column=0, row=0, padx=50)
        self.favorite_label = ttk.Label(master=self.opinion_frame, text="")
        self.favorite_label.grid(column=1, row=0, padx=50)
        self.userrating_frame = ttk.Frame(master=self.opinion_frame)
        self.userrating_decbut = tk.Button(master=self.userrating_frame, text="-", width=3, command=self.decrease_rating)
        self.userrating_value = ttk.Label(master=self.userrating_frame, width=4, anchor=tk.CENTER, text="")
        #self.userrating_decbut.grid(column=0, row=0)
        self.userrating_value.grid(column=1, row=0)
        self.userrating_incbut = tk.Button(master=self.userrating_frame, text="+", width=3, command=self.increase_rating)
        self.userrating_frame.grid(column=0, row=1)
        self.favorite_button = tk.Button(master=self.opinion_frame, text="Favorites", command=self.toggle_favorite)
        self.opinion_frame.pack(fill=tk.NONE)
        
        self.ingredient_frame = ttk.Frame(master=self.viewer_frame)
        self.ingredient_frame.pack(pady=(50, 5))
        
        self.add_ingredient_frame = ttk.Frame(master=self.viewer_frame)
        self.add_ingredient_button = tk.Button(master=self.add_ingredient_frame, text="Add Ingredient")
        self.add_ingredient_frame.pack(pady=5)
        
        self.viewer_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        self.editing_stringvar = tk.StringVar()
        
    def update_recipe_field(self, tk_label, recipe_attr, pack_style, pack_arg_dict=None):
        
        #label_dict = {} if label_arg_dict == None else {**label_arg_dict}
        #label_dict["master"] = tk_label.master
        self.edit_entry.destroy()
        self.edit_button.destroy()
        new_text = self.editing_stringvar.get()
        tk_label.config(text=new_text)
        #tk_label = ttk.Label(**label_dict)
        if pack_style == "pack":
            tk_label.pack()
        elif pack_style == "grid":
            tk_label.grid(**pack_arg_dict)
        setattr(self.current_recipe, recipe_attr, new_text)
        self.current_recipe.save()
        
    def user_edit_label(self, tk_label, recipe_attr, pack_style, entry_type="entry", font_size=12):
    
        label_master = tk_label.master
        label_text = tk_label.cget("text")
        
        if pack_style == "pack":
            tk_label.pack_forget()
        elif pack_style == "grid":
            tk_label.grid_forget()
        else:
            raise Exception("Invalid pack method given")
            
        self.editing_stringvar.set(label_text)
        
        if entry_type == "entry":
            self.edit_entry = ttk.Entry(master=label_master, width=25, textvariable=self.editing_stringvar, font=font_size)
            self.edit_entry.grid(column=0, row=0, padx=(0, 10))
            self.edit_button = tk.Button(master=label_master, text="Save", command=lambda:self.update_recipe_field(tk_label, recipe_attr, pack_style))
            self.edit_button.grid(column=1, row=0)
        
    def user_edit_drink_name(self, *args):
        self.user_edit_label(self.drink_label, "title", "pack", entry_type="entry", font_size=20)
        
    def user_edit_drink_subtitle(self, *args):
        self.user_edit_label(self.drink_subtitle, "subtitle", "pack", entry_type="entry")
        
    def display_favorite_status(self):
        new_text = "Remove from favorites" if self.current_recipe.favorite else "Add to Favorites"
        new_color = "#D93D44" if self.current_recipe.favorite else "#CCC4C4"
        self.favorite_button["text"] = new_text
        self.favorite_button.configure(bg=new_color)
        
    def toggle_favorite(self, *args):
        self.current_recipe.favorite = False if self.current_recipe.favorite else True
        self.display_favorite_status()
        self.current_recipe.save()
        
    def display_rating_status(self):
        new_text = "N/A" if self.current_recipe.rating == None else str(self.current_recipe.rating)
        self.userrating_value.config(text=new_text)
        
    def decrease_rating(self, *args):
        if self.current_recipe.rating != None:
            if self.current_recipe.rating == 0:
                self.current_recipe.rating = None
            else:
                self.current_recipe.rating -= 0.5
        self.display_rating_status()
        self.current_recipe.save()
        
    def increase_rating(self, *args):
        if self.current_recipe.rating != None:
            if self.current_recipe.rating < 5:
                self.current_recipe.rating += 0.5
        else:
            self.current_recipe.rating = 0
        self.display_rating_status()
        self.current_recipe.save()
        
    def display_ingredients(self):
    
        self.ingredient_grid_refs = []
        ingredient_index = 0
        
        for ingredient in self.current_recipe.ingredients:
            amount_label = ttk.Label(master=self.ingredient_frame, text=ingredient.name)
            amount_label.grid(col=0, row=ingredient_index)
            msmt_label = ttk.Label(master=self.ingredient_frame, text="\u0188")
            msmt_label.grid(col=1, row=ingredient_index)
    
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
        if self.cat_tree.focus() == "":
            return
        
        is_recipe = False
        for recipe_obj, recipe_iid in self.recipe_dict.items():
            if int(self.cat_tree.focus()) == recipe_iid:
                curr_recipe = recipe_obj
                is_recipe = True
                break
        if is_recipe:
            self.drink_label.config(text=curr_recipe.title)
            self.drink_subtitle.config(text=curr_recipe.subtitle)
            self.rating_label.config(text="Rating")
            self.favorite_label.config(text="Favorite")
            self.userrating_value.config(text=curr_recipe.rating)
            self.userrating_decbut.grid(column=0, row=0)
            rating = curr_recipe.rating if curr_recipe.rating != None else "N/A"
            self.userrating_value.config(text=rating)
            self.userrating_incbut.grid(column=2, row=0)
            self.favorite_button.grid(column=1, row=1)
            self.current_recipe = curr_recipe
            
            self.display_favorite_status()
            self.display_rating_status()
            self.display_ingredients()
            
            self.add_ingredient_button.pack()
            
        
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
        s.configure("Treeview", rowheight=25)
        
        if self.cat_tree is not None:
            self.cat_tree.destroy()
        self.cat_tree = ttk.Treeview(master=self.cat_frame, height=1000)
        self.cat_tree.heading("#0", text="Categories", anchor="w")
        self.cat_tree.bind("<ButtonRelease-1>", self.show_recipe)
        
        self.category_dict = {}
        self.recipe_dict = {}
        tree_iid = 0
        
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

        self.cat_tree.column("#0", width=200)
        self.cat_tree.pack(fill=tk.NONE)
        
mixpy = MixoloPy()
mixpy.mainloop()
