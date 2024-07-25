# importar la función que devolverá una instancia de una conexión
from config.db import connectToMySQL
# modelar la clase después de la tabla friend de nuestra base de datos
class Tarea:
    def __init__( self , data ):
        self.id = data['tareId']
        self.nombre = data['nombre']

    # ahora usamos métodos de clase para consultar nuestra base de datos
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM tareas;"
        results = connectToMySQL('tareas').query_db(query, data=None)
        if results is False: 
            return []  # Devolver una lista vacía si hubo un error
        friends = []
        for friend in results:
            friends.append(cls(friend))
        return friends
    @classmethod
    def post_all(cls, nombre):
        query = "insert into tareas (nombre) values (%s);"
        # asegúrate de llamar a la función connectToMySQL con el esquema al que te diriges
        result = connectToMySQL('tareas').query_db(query, (nombre,))
        return result

