import json
import os

DATA_FILE = "activities.json"

class Activity:
    def __init__(self, id, name, size=None, distance_from_origin=None, cost=None, category=None):
        self.id = id
        self.name = name
        self.size = size
        self.distance_from_origin = distance_from_origin
        self.cost = cost
        self.category = category

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "size": self.size,
            "distance_from_origin": self.distance_from_origin,
            "cost": self.cost,
            "category": self.category
        }
    def load_all():
        with open(DATA_FILE, "") as f:

    def save_all(activities):
        with open(DATA_FILE, "") as f:
  

	def __str__(self):
    return f"<Activity {self.id} {self.name}>"