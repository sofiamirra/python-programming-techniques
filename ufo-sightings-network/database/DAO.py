from database.DB_connect import DBConnect
from model.arco import Arco
from model.state import State

class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getBorderValues():
        conn = DBConnect.get_connection()
        results = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT MIN(s.Lat) as min_latitude, MAX(s.Lat) as max_latitude, MIN(s.Lng) as min_longitude, MAX(s.Lng) as max_longitude
                FROM state s"""

        cursor.execute(query)

        for row in cursor:
            # results sarà { 'max_latitude': #value, 'max_longitude': #value }
            results.append(row)

        cursor.close()
        conn.close()
        return results[0]


    @staticmethod
    def get_all_states():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select DISTINCT * 
                    from state s"""
            cursor.execute(query)

            for row in cursor:
                result.append(
                    State(**row))

            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getAllShapes():
        conn = DBConnect.get_connection()
        results = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT DISTINCT shape 
        FROM sighting 
        WHERE shape <> ''
        ORDER BY shape desc"""

        cursor.execute(query)

        for row in cursor:
            results.append(row["shape"])

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllNodes(shape, lat, lng):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT DISTINCT s.*
            FROM state s, sighting si
            WHERE s.id = si.state 
            AND si.shape = %s
            AND s.Lat > %s
            AND s.Lng > %s"""
            cursor.execute(query, (shape, lat, lng))

            for row in cursor:
                result.append(State(**row))
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getAllEdges(shape, lat, lng, idMapS):
        conn = DBConnect.get_connection()
        results = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT t1.id as id1, t2.id as id2, t1.n + t2.n as peso
        FROM (SELECT s.id, SUM(si.duration) as n 
        FROM state s, sighting si
        WHERE si.state = s.id 
        AND si.shape = %s
        AND s.Lat > %s
        AND s.Lng > %s
        GROUP BY s.id) as t1, 
        (SELECT s.id, SUM(si.duration) as n 
        FROM state s, sighting si
        WHERE si.state = s.id 
        AND si.shape = %s
        AND s.Lat > %s
        AND s.Lng > %s
        GROUP BY s.id) as t2, neighbor n 
        WHERE t1.id > t2.id 
        AND n.state1 = t1.id AND n.state2 = t2.id
        GROUP BY t1.id, t2.id """

        cursor.execute(query, (shape, lat, lng, shape, lat, lng))

        for row in cursor:
            results.append(Arco(idMapS[row["id1"]], idMapS[row["id2"]], row["peso"]))

        cursor.close()
        conn.close()
        return results




