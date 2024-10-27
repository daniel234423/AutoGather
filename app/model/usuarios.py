from ..config.db import connectToMySQL

class Users:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['username']
        self.email = data['email']
        self.password = data['password']

    @classmethod
    def user_register(cls, name, email, password):
        query = f"""
        INSERT INTO user (username, email, password) VALUES ('{name}','{email}','{password}')
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
        if results:  # Verificar si hay resultados
            for user_data in results:
                user.append(cls(user_data))
        return user
    @classmethod
    def get_user_data(cls,id):
        query = f"select dc.matricula, dc.color, dc.tipo_vheiculo from date_cars as dc join user on dc.id_user = user.id where user.id = {id};"
        results = connectToMySQL("AutoGather").query_db(query)
        datos = []
        if results:  # Verificar si hay resultados
            for car_data in results:
                datos.append(cls(car_data))
        return datos