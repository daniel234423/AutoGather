from config.db import connectToMySQL

class Users:
    def __init__(self, data):
        self.id = data['id_user']
        self.name = data['username']
        self.email = data['email']
        self.password = data['password']

    @classmethod
    def user_register(cls, name, email, password):
        query = f"""
        INSERT INTO user (username, email, password) VALUES ('{name}', '{email}', '{password}')
        """
        result = connectToMySQL("AutoGather").query_db(query)
        return result
    @classmethod
    def login_by_email(cls,email):
        query = f"""
        SELECT * FROM user WHERE email = '{email}'
        """
        results = connectToMySQL("AutoGather").query_db(query)
        user = []
        for users in results:
            user.append(cls(users))
        return user