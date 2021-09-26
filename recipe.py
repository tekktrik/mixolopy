import os.path

class RecipeCategory:

    FORBIDDDEN_NAMES = ["Uncategorized", "Corrupted"]

    def __init__(self, cat_relpath):
        
        cat_split = cat_relpath.split("\\")
        if cat_split[-1] in self.FORBIDDDEN_NAMES:
            raise Exception("Cannot use this name for a category")
        else:
            self.name = cat_split[-1]
        self._cat_relpath = cat_relpath
        self.nest_level = len(cat_split) - 1
        self.parent_path = ''.join(cat_split[0:-1]) if self.nest_level !=0 else None
        
    def getRelativePath(self):
        return self._cat_relpath