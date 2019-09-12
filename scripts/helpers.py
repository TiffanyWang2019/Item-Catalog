# -*- coding: utf-8 -*-

from scripts import tabledef
from flask import session
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
import bcrypt


@contextmanager
def session_scope():
    """Provide a transactional scope around a series of operations."""
    s = get_session()
    s.expire_on_commit = False
    try:
        yield s
        s.commit()
    except:
        s.rollback()
        raise
    finally:
        s.close()


def get_session():
    return sessionmaker(bind=tabledef.engine)()


def get_user():
    username = session['username']
    with session_scope() as s:
        user = s.query(tabledef.User).filter(tabledef.User.username.in_([username])).first()  # noqa
        return user


def add_user(username, password, email):
    with session_scope() as s:
        u = tabledef.User(username=username,
                          password=password.decode('utf8'),
                          email=email)
        s.add(u)
        s.commit()


def change_user(**kwargs):
    username = session['username']
    with session_scope() as s:
        user = s.query(tabledef.User).filter(tabledef.User.username.in_([username])).first()  # noqa
        for arg, val in kwargs.items():
            if val != "":
                setattr(user, arg, val)
        s.commit()


def hash_password(password):
    return bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())


def credentials_valid(username, password):
    with session_scope() as s:
        user = s.query(tabledef.User).filter(tabledef.User.username.in_([username])).first()  # noqa
        if user:
            return bcrypt.checkpw(password.encode('utf8'),
                                  user.password.encode('utf8'))
        else:
            return False


def username_taken(username):
    with session_scope() as s:
        return s.query(tabledef.User).filter(tabledef.User.username.in_([username])).first()  # noqa

def is_registered(email):
    with session_scope() as s:
        return s.query(tabledef.User).filter(tabledef.User.email == email).count()

def get_user_by_email(email):
    with session_scope() as s:
        return s.query(tabledef.User).filter(tabledef.User.email == email).one()


def query_catalog():
    with session_scope() as s:
        return s.query(tabledef.Catalog).all()


def add_catalog(catalog):
    with session_scope() as s:
        u = tabledef.Catalog(catalog_name=catalog)
        s.add(u)
        s.commit()


def add_item(item_name, description, catalog_id, user_id):
    with session_scope() as s:
        u = tabledef.Item(item_name=item_name,
                          description=description,
                          catalog_id=catalog_id,
                          user_id = user_id)
        s.add(u)
        s.commit()


def query_catalog_and_item():
    with session_scope() as s:
        return s.query(tabledef.Item, tabledef.Catalog,tabledef.User).\
        filter(tabledef.Catalog.id == tabledef.Item.catalog_id).\
        filter(tabledef.User.id == tabledef.Item.user_id).\
        add_columns(tabledef.Item.id, tabledef.Catalog.catalog_name, tabledef.Item.item_name).all()  # noqa


def query_item(id):
    with session_scope() as s:
        return s.query(tabledef.Item, tabledef.Catalog).\
            filter(tabledef.Catalog.id == tabledef.Item.catalog_id).\
            filter(tabledef.Item.id == id).\
            add_columns(tabledef.Item.id,
                        tabledef.Catalog.catalog_name,
                        tabledef.Item.item_name,
                        tabledef.Item.description,
                        tabledef.Item.user_id).all()


def update_item(id, item_title, item_description):
    with session_scope() as s:
        s.query(tabledef.Item).\
                filter(tabledef.Item.id == id).\
                update({"item_name": item_title,
                        "description": item_description})
        s.commit()


def delete_item(id):
    with session_scope() as s:
        s.query(tabledef.Item).\
            filter(tabledef.Item.id == id).\
            delete()
        s.commit()


def query_bycatalogid_and_item(id):
    with session_scope() as s:
        return s.query(tabledef.Item, tabledef.Catalog).\
               filter(tabledef.Catalog.id == tabledef.Item.catalog_id).\
               filter(tabledef.Catalog.id == id).\
               add_columns(tabledef.Item.id,
                           tabledef.Catalog.catalog_name,
                           tabledef.Item.item_name).all()
