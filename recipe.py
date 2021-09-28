import os.path
import json
import datetime
from dateutil.parser import parse as duparse

class RecipeFileStructure:

    FORBIDDDEN_NAMES = []
    
    def __init__(self, rel_path):
        
        file_split = rel_path.split("\\")
        if file_split[-1] in self.FORBIDDDEN_NAMES:
            raise Exception("Cannot use this name")
        else:
            self.name = file_split[-1]
        self.relative_path = rel_path
        self.nest_level = len(file_split) - 1
        self.parent_path = '\\'.join(file_split[0:-1]) if self.nest_level !=0 else None
        
    def is_child(self, pot_parent):
        return self.parent_path == pot_parent.relative_path
        
class EnsurableDict:
    
    REQUIRED_FIELDS = []
    
    def _check_required_attrs(self):
        for field in self.REQUIRED_FIELDS:
            try:
                getattr(self, field)
            except AttributeError:
                setattr(self, field, self.REQUIRED_FIELDS[field])

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
    
    def __init__(self, abs_path, base_folder):
        super().__init__(os.path.relpath(abs_path, start=base_folder))
        #self.title = self.name[:-5]
        with open(abs_path, 'r') as recipe_file:
            recipe_dict = json.load(recipe_file)
            for key, value in recipe_dict.items():
                if key != "ingredients":
                    setattr(self, key, value)
                else:
                    self.ingredients = []
                    for ingredient_map in value:
                        self.ingredients.append(Ingredient(ingredient_map))
            self._check_required_attrs()
                
class Ingredient(EnsurableDict):

    REQUIRED_FIELDS = {
        "name": "Magic",
        "amount": "1",
        "msmt": "oz",
        "type": "main"
    }
    
    def __init__(self, ingredient_dict):
        for key, value in ingredient_dict.items():
            setattr(self, key, value)
        self._check_required_attrs()