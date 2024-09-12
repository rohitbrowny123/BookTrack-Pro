from flask_sqlalchemy import *
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.mutable import MutableList
from flask_security import UserMixin, RoleMixin , AsaList
from datetime import datetime
import os


db = SQLAlchemy()

class RolesUsers(db.Model):
    __tablename__ = 'roles_users'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column('user_id', db.Integer(), db.ForeignKey('User.id'))
    role_id = db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))

class Role(db.Model, RoleMixin):
    __tablename__ = 'role'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))
    permissions = db.Column(MutableList.as_mutable(AsaList()), nullable=True)

class User(db.Model, UserMixin):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    is_blacklisted = db.Column(db.Boolean, default=False)
    active = db.Column(db.Boolean())
    roles = db.relationship('Role', secondary='roles_users',
                            backref=db.backref('users', lazy='dynamic'))
    requests = db.relationship('BookRequest', backref='user', lazy=True, cascade='all, delete-orphan')
    ratings = db.relationship('Rating', backref='user', lazy=True, cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'roles': [{'name': role.name} for role in self.roles],
            'is_blacklisted': self.is_blacklisted
        }

class BookRequest(db.Model):
    __tablename__ = 'book_request'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id', ondelete='CASCADE'), nullable=False)
    status = db.Column(db.String(20), nullable=False, default='pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    days_requested = db.Column(db.Integer, nullable=False, default=7)
    due_date = db.Column(db.DateTime, nullable=True)
    book = db.relationship('Book', backref=db.backref('requests', lazy=True, cascade='all, delete-orphan'))

class Book(db.Model):
    __tablename__ = 'book'
    id = db.Column(db.Integer, primary_key=True)
    section_id = db.Column(db.Integer, db.ForeignKey('section.id'))
    name = db.Column(db.String(), nullable=False)
    description = db.Column(db.String(255))
    content = db.Column(db.String(255))
    author = db.Column(db.String(255))
    status = db.Column(db.String(20), default='available')
    section = db.relationship('Section', backref='books')
    ratings = db.relationship('Rating', backref='book', lazy=True, cascade='all, delete-orphan')
    
    
    def average_rating(self):
        ratings = [r.rating for r in self.ratings]
        return sum(ratings) / len(ratings) if ratings else 0


    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'author': self.author,
            'section': str(self.section_id),  
            'status': self.status,
            'description': self.description,
            'rating': self.average_rating()
        }

class Section(db.Model):
    __tablename__ = 'section'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    image = db.Column(db.String(255))
    description = db.Column(db.Text, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'date_created': self.date_created.isoformat() if self.date_created else None,
            'image': self.image,
            'description': self.description
        }

class Rating(db.Model):
    __tablename__ = 'rating'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Feedback(db.Model):
    __tablename__ = 'feedback'
    id = db.Column(db.Integer, primary_key=True)
    rating_id = db.Column(db.Integer, db.ForeignKey('rating.id'), nullable=False)
    feedback = db.Column(db.String(500))
    rating = db.relationship('Rating', backref=db.backref('feedback', uselist=False))