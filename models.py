# # models.py
# from flask_sqlalchemy import SQLAlchemy

# db = SQLAlchemy()

# class User(db.Model):
#     __tablename__ = 'users'
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(255), nullable=False)
#     email = db.Column(db.String(255), unique=True, nullable=False)
#     password = db.Column(db.String(255), nullable=False)

#     def __repr__(self):
#         return f'<User {self.email}>'

# class Bike(db.Model):
#     __tablename__ = 'bikes'
#     id = db.Column(db.Integer, primary_key=True)
#     type = db.Column(db.String(50), nullable=False)
#     rate_per_hour = db.Column(db.Integer, nullable=False)
#     available_quantity = db.Column(db.Integer, nullable=False)

#     def __repr__(self):
#         return f'<Bike {self.type}>'
