# -*- coding: utf-8 -*-

import sys
import os
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

# Local
SQLALCHEMY_DATABASE_URI = 'sqlite:///accounts.db'

# Heroku
# SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']

Base = declarative_base()


def db_connect():
    """
    Performs database connection using database settings from settings.py.
    Returns sqlalchemy engine instance
    """
    return create_engine(SQLALCHEMY_DATABASE_URI)


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    username = Column(String(200), unique=True)
    password = Column(String(512))
    email = Column(String(200),unique=True)
    def __repr__(self):
        return '<User %r>' % self.username


class Catalog(Base):
    __tablename__ = "catalog"
    id = Column(Integer, primary_key=True)
    catalog_name = Column(String(50), unique=True)

    def __repr__(self):
        return '<Catalog %r>' % self.catalog_name


class Item(Base):
    __tablename__ = "item"
    id = Column(Integer, primary_key=True)
    item_name = Column(String(50), unique=True)
    description = Column('content', String(100000))
    catalog_id = Column(Integer, ForeignKey('catalog.id'))
    user_id = Column(Integer, ForeignKey('user.id'))

    # created_date = Column(DateTime(timezone=True), server_default=func.now())
    def __repr__(self):
        return '<Catalog %r>' % self.item_name

engine = db_connect()  # Connect to database
Base.metadata.create_all(engine)  # Create models
if __name__ == '__main__':
    manager.run()