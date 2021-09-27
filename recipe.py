import os.path

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

class RecipeCategory(RecipeFileStructure):

    FORBIDDDEN_NAMES = ["Uncategorized", "Corrupted"]
        
    def has_child(self, pot_child):
        return pot_child.relative_path == self.relative_path
        
class Recipe(RecipeFileStructure):
    
    FORBIDDDEN_NAMES = ["MixolopyBrokenRecipe"]
    
    def __init__(self, rel_path):
        super().__init__(rel_path)
        pass