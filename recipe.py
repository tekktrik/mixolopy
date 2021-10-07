import os
import json
import datetime
from dateutil.parser import parse as duparse

class RecipeFileStructure:

    FORBIDDDEN_NAMES = []
    
    def __init__(self, rel_path):

        print(rel_path)
        #file_split = rel_path.split("\\")
        rel_path = os.path.normpath(rel_path)
        file_split = rel_path.split(os.sep)
        if file_split[-1] in self.FORBIDDDEN_NAMES:
            raise Exception("Cannot use this name")
        else:
            self.name = file_split[-1]
        self.relative_path = rel_path
        self.nest_level = len(file_split) - 1
        self.parent_path = (os.sep).join(file_split[0:-1]) if self.nest_level !=0 else None
        
    def is_child(self, pot_parent):
        return self.parent_path == pot_parent.relative_path
        
class EnsurableDict:
    
    REQUIRED_FIELDS = []
    
    def _check_required_attrs(self):
        must_save = False
        for field in self.REQUIRED_FIELDS.keys():
            try:
                getattr(self, field)
            except AttributeError:
                must_save = True
                setattr(self, field, self.REQUIRED_FIELDS[field])
        if must_save:
            json_dict = {}
            for key, value in self.REQUIRED_FIELDS.items():
                json_dict[key] = getattr(self, key, value)
            with open(self.filepath, 'w') as json_file:
                json.dump(json_dict, json_file, indent=4)

class RecipeCategory(RecipeFileStructure):

    FORBIDDDEN_NAMES = ["Uncategorized", "Corrupted"]
        
    def has_child(self, pot_child):
        return pot_child.relative_path == self.relative_path
        
class Recipe(RecipeFileStructure, EnsurableDict):
    
    FORBIDDDEN_NAMES = ["MixolopyBrokenRecipe"]
    
    REQUIRED_FIELDS = {
        "title": "Blank Recipe",
        "subtitle": "Subtitle",
        "creator": "Mixolopy",
        "date_added": "1970-01-01T00:00:00.000000",
        "servings": 1,
        "favorite": False,
        "rating": None,
        "instructions": [
            "Step1",
            "Step2",
            "Step3"
        ],
        "notes": "Insert notes here",
        "ingredients": []
    }
    
    def __init__(self, filepath, base_folder):
        super().__init__(os.path.relpath(filepath, start=base_folder))
        #self.title = self.name[:-5]
        self.filepath = filepath
        with open(filepath, 'r') as recipe_file:
            recipe_dict = json.load(recipe_file)
            for key, value in recipe_dict.items():
                if key != "ingredients":
                    setattr(self, key, value)
                else:
                    self.ingredients = []
                    for ingredient_map in value:
                        self.ingredients.append(Ingredient(ingredient_map))
            self._check_required_attrs()
            
    def to_dict(self):
        recipe_dict = {}
        for key in self.REQUIRED_FIELDS.keys():
            if key == "ingredients":
                ingredient_list = []
                for ingredient in self.ingredients:
                    ingredient_list.append(ingredient.to_dict())
                recipe_dict["ingredients"] = ingredient_list
            else:
                recipe_dict[key] = getattr(self, key)
        return recipe_dict
            
    def save(self):
        with open(self.filepath, 'w') as recipe_file:
            json.dump(self.to_dict(), recipe_file)
            
    def add_ingredient(self, ingredient):
        self.ingredients.append(ingredient)
        
    def remove_ingredient(self, ingredient):
        self.ingredients.pop(ingredient)
                
class Ingredient(EnsurableDict):

    REQUIRED_FIELDS = {
        "name": "Ingredient",
        "amount": "1",
        "msmt": "oz",
        "type": "main"
    }
    
    FRACTION_STR = {
        0.75: "\u00BE",
        0.5: "\u00BD",
        0.25: "\u00BC",
        0.125: "\u215B"
    }
    
    def __init__(self, ingredient_dict):
        for key, value in ingredient_dict.items():
            setattr(self, key, value)
        self._check_required_attrs()

    def to_dict(self):
        ingredient_dict = {}
        for key in self.REQUIRED_FIELDS.keys():
            ingredient_dict[key] = getattr(self, key)
        return ingredient_dict
        
    @classmethod
    def from_default(cls):
        return cls(cls.REQUIRED_FIELDS)