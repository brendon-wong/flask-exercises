# Create class Snack to represent data
class Snack():
    id = 1
    def __init__(self, name, kind):
        # Assign incrementing snack ID
        self.id = Snack.id
        Snack.id += 1
        # Assign snack name and kind
        self.name = name
        self.kind = kind