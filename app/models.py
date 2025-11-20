from . import db

class Activity:
	__tablename__ = 'activities'

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(100), nullable=False)
	size = db.Column(db.String(50), nullable=True)
	distance_from_origin = db.Column(db.Float, nullable=True)
	cost = db.Column(db.Float, nullable=True)
	category = db.Column(db.String(100), nullable=True)

	def __str__(self):
		return f"<Activity {self.id} {self.name}>"

