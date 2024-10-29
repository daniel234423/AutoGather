# importar la función que devolverá una instancia de una conexión
from ..config.db import connectToMySQL
# modelar la clase después de la tabla friend de nuestra base de datos
class Info:
    def __init__( self , data ):
        self.id = data['id_date_cars']
        self.matricual = data['matricula']
        self.tipo_vehiculo = data['tipo_vheiculo']
        self.color = data['color']

    @classmethod
    def get_all_by_id(cls, id_user):
        query = "SELECT * FROM date_cars WHERE id_user = %s"
        results = connectToMySQL('AutoGather').query_db(query, id_user)
        if results is False: 
            return [] 
        datos = []
        for date in results:
            datos.append(cls(date))
        return datos
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM date_cars;"
        results = connectToMySQL('AutoGather').query_db(query, data=None)
        if results is False: 
            return [] 
        friends = []
        for friend in results:
            friends.append(cls(friend))
        return friends
    @classmethod
    def post_all(cls, matricula, tipo_vehiculo, color, id_user):
        select = "SELECT * FROM date_cars WHERE matricula = %s AND id_user = %s;"
        results = connectToMySQL('AutoGather').query_db(select, (matricula, id_user))
        if results:
            return "El dato ya existe para este usuario."
        else:
            query = "INSERT INTO date_cars (matricula, tipo_vheiculo, color, id_user) VALUES (%s, %s, %s, %s);"
            result = connectToMySQL('AutoGather').query_db(query, (matricula, tipo_vehiculo, color, id_user))
            return result
    @classmethod
    def delete_by_app(cls, id, id_user):
        query = "DELETE FROM date_cars WHERE id_date_cars = %s AND id_user = %s;"
        results = connectToMySQL('AutoGather').query_db(query,(id, id_user))
        return results
    @classmethod
    def delet_by_id(cls, id):
        query = "DELETE FROM date_cars WHERE id_date_cars = %s;"
        results = connectToMySQL('AutoGather').query_db(query,(id,))
        return results