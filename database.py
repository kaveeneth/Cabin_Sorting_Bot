from config import Config


import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

Pdb = credentials.Certificate(
    "Database.json"
    )

firebase_admin.initialize_app(Pdb, {
    'databaseURL': Config.FIREBASE_URL
})


pdb = db.reference('Database/')


class DB:
    """Basic Database Commands"""
    def set_data(key, val):
        """set(key, value)"""
        data = {key: val}
        pdb.update(data)
    def get_data(key):
        d = pdb.get()[key]
        return d
    def del_data(key):
        dt = pdb.get()
        dt.pop(key)
        pdb.set(dt)
    def check(key):
        try:
            pdb.get()[key]
            return True
        except KeyError:
            return False
        except TypeError:
            return False
    def mk_dir(Dirname):
        pdb.child(f"/{Dirname}")


DB = pdb.child("Assistant/")
Users = pdb.child("Users/")


class db:
    def set_data(key, val):
        """set(key, value)"""
        data = {key: val}
        DB.update(data)
    def get_data(key):
        d = DB.get(key)
        return d
    def del_data(key):
        dt = DB.get()
        dt.pop(key)
        pdb.set(dt)
    def mk_dir(Dirname):
        DB.child(f"/{Dirname}")
    def add_users(ID, name, bd, mail, scl, city ,uname, cabin, cnum):
        data = {ID: {"Name": name, "Username": uname, "Birthdate": bd, "Email": mail, "School": scl, "City": city, "CabinNm": cabin, "CabinNo": cnum}}
        Users.update(data)
    def rem_user(ID):
        d = Users.get()
        d.pop(ID, None)
    def get_users():
        try:
            d = Users.get()
            return d
        except:
            return None
    def check(key):
        try:
            DB.get()[key]
            return True
        except KeyError:
            return False
        except TypeError:
            return False
