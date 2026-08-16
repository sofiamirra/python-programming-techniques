from database.DB_connect import DBConnect
from model import state
from model.state import State
from model.sighting import Sighting


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getAllYears():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT DISTINCT YEAR(s.datetime) as year
            FROM sighting s
            ORDER BY year ASC"""
            cursor.execute(query)

            for row in cursor:
                result.append(row["year"])
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def get_all_states(year):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT DISTINCT s.* 
            FROM state s, sighting si
            WHERE s.id = si.state
            AND YEAR(si.datetime) = %s"""
            cursor.execute(query, (year, ))

            for row in cursor:
                result.append(
                    State(row["id"],
                          row["Name"],
                          row["Capital"],
                          row["Lat"],
                          row["Lng"],
                          row["Area"],
                          row["Population"],
                          row["Neighbors"]))

            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getAllNodes(year, state):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT DISTINCT s.*
                FROM sighting s, state st
                WHERE s.state = st.id 
                AND YEAR(s.datetime) = %s
                AND st.Name = %s"""
            cursor.execute(query, (year, state))

            for row in cursor:
                result.append(Sighting(**row))
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getEdgesInformation(year, state):
        """SQL fa il lavoro facile: trova le coppie con la stessa forma"""
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT s1.id as id1, s2.id as id2  
            FROM sighting s1, sighting s2, state st
            WHERE s1.state = st.id AND s1.state = s2.state 
              AND s1.shape = s2.shape 
              AND s1.id > s2.id 
              AND YEAR(s1.datetime) = %s
              AND YEAR(s2.datetime) = %s
              AND st.Name = %s"""
            cursor.execute(query, (year, year, state))

            for row in cursor:
                result.append(row)
            cursor.close()
            cnx.close()
        return result