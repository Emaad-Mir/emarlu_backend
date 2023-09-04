""" database dependencies to support sqliteDB examples """
from flask_sqlalchemy import SQLAlchemy
from random import randrange
from datetime import date
import os, base64
import json
from __init__ import app, db
from sqlalchemy.exc import IntegrityError


''' Tutorial: https://www.sqlalchemy.org/library.html#tutorials, try to get into Python shell and follow along '''

# Define the Post class to manage actions in 'posts' table,  with a relationship to 'users' table
class Posting(db.Model):
    __tablename__ = 'posting'

    # Define the Notes schema
    id = db.Column(db.Integer, primary_key=True)
    note = db.Column(db.Text, nullable=False)
    image = db.Column(db.String)
    # Define a relationship in Notes Schema to userID who originates the note, many-to-one (many notes to one user)
    daterID = db.Column(db.Integer, db.ForeignKey('daters.id'))

    # Constructor of a Notes object, initializes of instance variables within object
    def __init__(self, id, note, image):
        self.daterID = id
        self.note = note
        self.image = image

    # Returns a string representation of the Notes object, similar to java toString()
    # returns string
    def __repr__(self):
        return "Notes(" + str(self.id) + "," + self.note + "," + str(self.daterID) + ")"

    # CRUD create, adds a new record to the Notes table
    # returns the object added or None in case of an error
    def create(self):
        try:
            # creates a Notes object from Notes(db.Model) class, passes initializers
            db.session.add(self)  # add prepares to persist person object to Notes table
            db.session.commit()  # SqlAlchemy "unit of work pattern" requires a manual commit
            return self
        except IntegrityError:
            db.session.remove()
            return None

    # CRUD read, returns dictionary representation of Notes object
    # returns dictionary
    def read(self):
        # encode image
        path = app.config['UPLOAD_FOLDER']
        file_path = os.path.join(path, self.image)
        with open(file_path, 'rb') as file:
            encoded_image = base64.encodebytes(file.read()).decode()
        
        return {
            "id": self.id,
            "daterID": self.daterID,
            "note": self.note,
            "image": self.image,
            "base64": encoded_image
        }


# Define the User class to manage actions in the 'users' table
# -- Object Relational Mapping (ORM) is the key concept of SQLAlchemy
# -- a.) db.Model is like an inner layer of the onion in ORM
# -- b.) User represents data we want to store, something that is built on db.Model
# -- c.) SQLAlchemy ORM is layer on top of SQLAlchemy Core, then SQLAlchemy engine, SQL
class Dater(db.Model):
    __tablename__ = 'daters'  # table name is plural, class name is singular

    # Define the User schema with "vars" from object
    id = db.Column(db.Integer, primary_key=True)
    _name = db.Column(db.String, unique=False, nullable=False)
    _uid = db.Column(db.String(255), unique=True, nullable=False)
    _gender = db.Column(db.String(255), unique=False, nullable=False)
    _age = db.Column(db.Integer, unique=False, nullable=False)
    _interests = db.Column(db.String(255), unique=False, nullable=False)

    # Defines a relationship between User record and Notes table, one-to-many (one user to many notes)
    posts = db.relationship("Posting", cascade='all, delete', backref='daters', lazy=True)

    # constructor of a User object, initializes the instance variables within object (self)
    def __init__(self, name, uid, gender, age, interests):
        self._name = name    # variables with self prefix become part of the object, 
        self._uid = uid
        self._gender = gender
        self._age = age
        self._interests = interests

    # a name getter method, extracts name from object
    @property
    def name(self):
        return self._name
    
    # a setter function, allows name to be updated after initial object creation
    @name.setter
    def name(self, name):
        self._name = name

    
    @property
    def uid(self):
        return self._uid
    
    # a setter function, allows name to be updated after initial object creation
    @uid.setter
    def uid(self, uid):
        self._uid = uid
        
    # check if uid parameter matches user id in object, return boolean
    def is_uid(self, uid):
        return self._uid == uid
    
    # a getter method, extracts email from object
    @property
    def gender(self):
        return self._gender
    
    # a setter function, allows name to be updated after initial object creation
    @gender.setter
    def gender(self, gender):
        self._gender = gender


    @property
    def age(self):
        return self._age
    
    # a setter function, allows name to be updated after initial object creation
    @age.setter
    def age(self, age):
        self._age = age

    @property
    def interests(self):
        return self._interests
    
    # a setter function, allows name to be updated after initial object creation
    @interests.setter
    def interests(self, interests):
        self._interests = interests
            
    # dob property is returned as string, to avoid unfriendly outcomes
    
    # output content using str(object) in human readable form, uses getter
    # output content using json dumps, this is ready for API response
    def __str__(self):
        return json.dumps(self.read())

    # CRUD create/add a new record to the table
    # returns self or None on error
    def create(self):
        try:
            # creates a person object from User(db.Model) class, passes initializers
            db.session.add(self)  # add prepares to persist person object to Users table
            db.session.commit()  # SqlAlchemy "unit of work pattern" requires a manual commit
            return self
        except IntegrityError:
            db.session.remove()
            return None

    # CRUD read converts self to dictionary
    # returns dictionary
    def read(self):
        return {
            "id": self.id,
            "name": self.name,
            "uid": self.uid,
            "gender": self.gender,
            "age": self.age,
            "interests": self.interests
        }

    # CRUD update: updates user name, password, phone
    # returns self
    def update(self, name="", uid="", gender="", age: int=0, interests = []):
        """only updates values with length"""
        if len(name) > 0:
            self.name = name
        if len(uid) > 0:
            self.uid = uid
        if len(gender) > 0:
            self.gender = gender
        if age > 0:
            self.age = age
        if len(interests) > 0:
            self.interests = interests

        
        db.session.commit()
        return self

    # CRUD delete: remove self
    # None
    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return None


"""Database Creation and Testing """


# Builds working data for testing
def initDaters():
    with app.app_context():
        """Create database and tables"""
        db.create_all()
        """Tester data for table"""
        d1 = Dater(name='John Doe', uid='john', gender='male', age=26, interests="Comp Sci and stuff")
        d2 = Dater(name='Jane Doe', uid='jane', gender='female',age=23, interests="Business and Bio")
    

        daters = [d1, d2]

        """Builds sample user/note(s) data"""
        for dater in daters:
            try:
                '''add a few 1 to 4 notes per user'''
                for num in range(randrange(1, 4)):
                    note = f"####  {dater.name} note {num}. \n Generated by test data."
                    dater.posts.append(Posting(id=dater.id, note=note, image='ncs_logo.png'))
                '''add user/post data to table'''
                dater.create()
            except IntegrityError:
                '''fails with bad or duplicate data'''
                db.session.remove()
                print(f"Records exist, duplicate email, or error: {dater.uid}")
            