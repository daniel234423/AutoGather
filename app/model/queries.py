# importar la función que devolverá una instancia de una conexión
from ..config.db import connectToMySQL
# modelar la clase después de la tabla friend de nuestra base de datos
class Info:
    def __init__( self , data ):
        self.id = data['id']
        self.matricual = data['matricula']
        self.tipo_vehiculo = data['tipo_vehiculo']
        self.color = data['color']

    # ahora usamos métodos de clase para consultar nuestra base de datos
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM informacion;"
        results = connectToMySQL('AutoGather').query_db(query, data=None)
        if results is False: 
            return []  # Devolver una lista vacía si hubo un error
        friends = []
        for friend in results:
            friends.append(cls(friend))
        return friends
    @classmethod
    def post_all(cls, matricula, tipo_vehiculo, color):
        query = "insert into date_cars (matricula, color, tipo_vehiculo) values (%s, %s, %s);"
        # asegúrate de llamar a la función connectToMySQL con el esquema al que te diriges
        result = connectToMySQL('AutoGather').query_db(query, (matricula, color, tipo_vehiculo,))
        return result

