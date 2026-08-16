from dataclasses import dataclass

@dataclass
class Category:
    category_id: int
    category_name: str

    def __hash__(self):
        return hash(self.category_id)

    def __eq__(self, other):
        return self.category_id == other.category_id

    def __str__(self):
        return f"{self.category_name} ({self.category_id})"
