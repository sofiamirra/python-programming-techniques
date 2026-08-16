from database.DB_connect import DBConnect
from model.arco import Arco
from model.circuit import Circuit
from model.placement import Placement


class DAO():

    @staticmethod
    def getAllYears():
        conn = DBConnect.get_connection()
        results = []

        cursor = conn.cursor(dictionary=True)
        query = "SELECT distinct year FROM seasons s  ORDER BY year"

        cursor.execute(query)

        for row in cursor:
            results.append(row["year"])

        cursor.close()
        conn.close()
        return results


    @staticmethod
    def getAllCircuits():
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = """SELECT DISTINCT c.*
        FROM circuits c, races r
        WHERE c.circuitId = r.raceId """
        cursor.execute(query)

        res = []
        for row in cursor:
            res.append(Circuit(**row))

        cursor.close()
        cnx.close()
        return res

    @staticmethod
    def getPlacements(year, circuitId):
        conn = DBConnect.get_connection()

        cursor = conn.cursor(dictionary=True)
        query = """SELECT re.driverId as driverId, re.time as time
               FROM results re, races r
               WHERE re.raceId = r.raceId 
               AND r.year = %s 
               AND r.circuitId = %s
               AND re.time is not null """

        cursor.execute(query, (year, circuitId))

        result = []
        for row in cursor:
            result.append(Placement(row["driverId"], row["time"]))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllEdges(year1, year2, idMapC):
        conn = DBConnect.get_connection()
        results = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT t1.circuitId as id1, t2.circuitId as id2, t1.n + t2.n as peso
                FROM (SELECT r.circuitId, COUNT(DISTINCT re.driverId) as n
                FROM results re, races r 
                WHERE re.raceId = r.raceId 
                AND re.time is not null
                AND r.year > %s AND r.year < %s
                GROUP BY r.circuitId) as t1, 
                (SELECT r.circuitId, COUNT(DISTINCT re.driverId) as n
                FROM results re, races r 
                WHERE re.raceId = r.raceId 
                AND re.time is not null
                AND r.year > %s AND r.year < %s
                GROUP BY r.circuitId) as t2
                WHERE t1.circuitId > t2.circuitId 
                GROUP BY t1.circuitId, t2.circuitId
                """

        cursor.execute(query, (year1, year2, year1, year2))

        for row in cursor:
            results.append(Arco(idMapC[row["id1"]], idMapC[row["id2"]], row["peso"]))

        cursor.close()
        conn.close()
        return results


