import mysql.connector
from mysql.connector import errorcode
import pathlib

class DBConnect:
    """Class that is used to create and manage a pool of connections to the database.
    It implements a class method that works as a factory for lending the connections from the pool"""
    # we keep the pool of connections as a class attribute, not an instance attribute
    _cnxpool = None

    def __init__(self):
        raise RuntimeError('Do not create an instance, use the class method get_connection()!')

    @classmethod
    def get_connection(cls, pool_name="my_pool", pool_size=3):
        if cls._cnxpool is None:
            try:
                # CREA IL DIZIONARIO CON LE TUE CREDENZIALI
                dbconfig = {
                    "user": "root",
                    "password": "rootroot",
                    "host": "127.0.0.1",
                    "database": "formula1"
                }

                # USA IL DIZIONARIO E TOGLI 'option_files'
                cls._cnxpool = mysql.connector.pooling.MySQLConnectionPool(
                    pool_name=pool_name,
                    pool_size=pool_size,
                    **dbconfig
                )
                return cls._cnxpool.get_connection()
            except mysql.connector.Error as err:
                print(f"Errore connessione: {err}")
                return None
        else:
            return cls._cnxpool.get_connection()