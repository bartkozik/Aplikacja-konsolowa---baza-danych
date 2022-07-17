from clcrypto import hash_password


class User:
    def __init__(self, username="", password="", salt=""):
        self._id = -1
        self.username = username
        self._hashed_password = hash_password(password, salt)

    @property
    def id(self):
        return self._id

    @property
    def hashed_password(self):
        return self._hashed_password

    def set_password(self, password, salt=''):
        self._hashed_password = hash_password(password, salt)

    @hashed_password.setter
    def hashed_password(self, password):
        self.set_password(password)

    def save_to_db(self, cursor):
        if self._id == -1:
            sql = """insert into users(username, hashed_password) values(%s, %s) returning id;"""
            values = (self.username, self.hashed_password)
            cursor.execute(sql, values)
            self._id = cursor.fetchone()[0]
            return True
        else:
            sql = """update users set username=%s, hashed_password=%s where id=%s;"""
            values = (self.username, self.hashed_password, self.id)
            cursor.execute(sql, values)
            return True

    @staticmethod
    def load_user_by_username(cursor, username):
        sql = "select id, username, hashed_password from users where username=%s;"
        cursor.execute(sql, (username,))
        data = cursor.fetchone()
        if data:
            id_, username, hashed_password = data
            loaded_user = User(username)
            loaded_user._id = id_
            loaded_user._hashed_password = hashed_password
            return loaded_user
        else:
            return None

    @staticmethod
    def load_all_users(cursor):
        sql = "select id, username, hashed_password from users;"
        users = []
        cursor.execute(sql)
        for row in cursor.fetchall():
            id_, username, hashed_password = row
            loaded_user = User()
            loaded_user._id = id_
            loaded_user.username = username
            loaded_user._hashed_password = hashed_password
            users.append(loaded_user)
        return users



    @staticmethod
    def load_user_by_id(cursor, id_):
        sql = "select id, username, hashed_password from users;"
        users = []
        cursor.execute(sql)
        for row in cursor.fetchall():
            id_, username, hashed_password = row
            loaded_user = User()
            loaded_user._id = id_
            loaded_user.username = username
            loaded_user._hashed_password = hashed_password
            users.append(loaded_user)
        return users

    def delete(self, cursor):
        sql = "delete from users where id=%s;"
        cursor.execute(sql,(self.id,))
        self.id = -1
        return True


class Messages:

    def __init__(self, from_id, to_id, text):
        self._id = -1
        self.from_id = from_id
        self.to_id = to_id
        self.text = text
        self._creation_data = None

    @property
    def creation_date(self):
        return self._creation_date

    @property
    def id(self):
        return self._id

    def save_to_db(self, cursor):
        if self._id == -1:
            sql = """insert into messages(from_id, to_id, text) values(%s, %s, %s) returning id creation_date;"""
            values = (self.from_id, self.to_id, self.text)
            cursor.execute(sql, values)
            self._id, self._creation_data = cursor.fetchone()[0]
            return True
        else:
            sql = """update messages set to_id=%s, from_id=%s, text=%s where id=%s;"""
            values = (self.self.from_id, self.to_id, self.text, self.id)
            cursor.execute(sql, values)
            return True

    @staticmethod
    def load_all_messages(cursor, user_id=None):
        if user_id:
            sql = "select id, from_id, to_id, text, creation_data from messages where to_id=%s;"
            cursor.execute(sql, (user_id,))
        else:
            sql = "select id, from_id, to_id, text, creation_data from messages;"
            cursor.execute(sql)
        messages = []
        for row in cursor.fetchall():
            id_, from_id, to_id, text, creation_data = row
            loaded_message = Messages(from_id, to_id, text)
            loaded_message._id = id_
            loaded_message.creation_data = creation_data
            messages.append(loaded_message)
        return messages











