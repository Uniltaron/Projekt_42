from sqlalchemy import Column, Boolean, Integer, Text, Date, ForeignKey
from sqlalchemy.orm import relationship, backref
from database import Base
from flask.ext.login import UserMixin
from hash_passwords import check_hash, make_hash

class User(UserMixin, Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(Text, nullable=False, unique=True)
    password = Column(Text, nullable=False)
   # diary = Column(Text, nullable=False, default="")
    active = Column(Boolean, nullable=False, default=True)

    def __init__(self, username=None, password=None, active=False):
        self.username = username
        self.password = password
        self.active = active

    def is_active(self):
        return self.active

    def get(id):
        if self.id == id:
            return self
        else:
            return None

    def valid_password(self, password):
        """Check if provided password is valid."""
        return check_hash(password, self.password)

    def __repr__(self):
        return '<%s(%r, %r)>' % (self.__class__.__name__, self.id, self.username)

class Contact(Base):
    __tablename__ = 'contacts'
    id = Column(Integer, primary_key=True)
    lastname = Column(Text, nullable=False)
    firstname = Column(Text, nullable=False)
    title = Column(Text, nullable=True)
    street = Column(Text, nullable=True)
    zip = Column(Text, nullable=True)
    city = Column(Text, nullable=True)
    birthdate = Column(Text, nullable=True)
    landline = Column(Text, nullable=True)
    mobile_phone = Column(Text, nullable=True)
    email = Column(Text, nullable=True)
    homepage = Column(Text, nullable=True)
    twitter = Column(Text, nullable=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', backref = backref('contacts', lazy = 'dynamic'))

    def __init__(self, lastname, firstname, user_id, title=None, street=None, zip=None, city=None, birthdate=None, landline=None, mobile_phone=None, email=None, homepage=None, twitter=None):

        self.lastname = lastname
        self.firstname = firstname
        self.user_id = user_id
        self.title = title
        self.street = street
        self.zip = zip
        self.city = city
        self.birthdate = birthdate
        self.landline = landline
        self.mobile_phone = mobile_phone
        self.email = email
        self.homepage = homepage
        self.twitter = twitter

    def __repr__(self):
        return '<%s(%r, %r)>' % (self.__class__.__name__, self.lastname, self.firstname)

class Diary(Base):
    __tablename__ = 'diaries'
    id = Column(Integer, primary_key=True)
    date = Column(Text, nullable=False)
    text = Column(Text, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', backref = backref('diaries', lazy = 'dynamic'))

    def __init__(self, date=None, text=None, user_id=None):
        self.user_id = user_id
        self.date = date
        self.text = text

    def __repr__(self):
        return '<%s(%r, %r)>' % (self.__class__.__name__, self.date, self.user_id)