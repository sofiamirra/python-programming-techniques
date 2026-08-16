from database.DB_connect import DBConnect
from model.Arco import Arco
from model.Constructor import Constructor

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
    def getConstructors(y1, y2):
        conn = DBConnect.get_connection()
        results = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT DISTINCT c.constructorId, c.constructorRef, c.name, c.nationality
        FROM results r, races ra, constructors c
        WHERE r.constructorId = c.constructorId AND ra.raceId = r.raceId 
        AND ra.year BETWEEN %s AND %s 
        AND r.position is not null"""

        cursor.execute(query, (y1, y2))

        for row in cursor:
            results.append(Constructor(**row))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllEdges(year1, year2, _idMapC):
        conn = DBConnect.get_connection()
        results = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT t1.constructorId as id1, t2.constructorId as id2, COUNT(DISTINCT t1.driverId) as peso
                FROM (SELECT DISTINCT r.driverId, r.constructorId
                     FROM results r, races ra
                     WHERE r.raceId = ra.raceId 
                     AND ra.year BETWEEN %s AND %s
                     AND r.position IS NOT NULL) as t1,
                    (SELECT DISTINCT r.driverId, r.constructorId
                     FROM results r, races ra
                     WHERE r.raceId = ra.raceId 
                     AND ra.year BETWEEN %s AND %s
                     AND r.position IS NOT NULL) as t2
                WHERE t1.driverId = t2.driverId        
                AND t1.constructorId > t2.constructorId
                GROUP BY t1.constructorId, t2.constructorId"""

        cursor.execute(query, (year1, year2, year1, year2))

        for row in cursor:
            results.append(Arco(_idMapC[row["id1"]], _idMapC[row["id2"]], row["peso"]))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getDoB(squadra, year1, year2):
        """Metodo per recuperare il pilota più anziano per ciascuna squadra"""
        conn = DBConnect.get_connection()
        results = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT MIN(d.dob) as oldest_dob
                    FROM drivers d, results r, races ra
                    WHERE d.driverId = r.driverId 
                    AND r.raceId = ra.raceId
                    AND r.constructorId = %s
                    AND ra.year BETWEEN %s AND %s
                                    """

        cursor.execute(query, (squadra.constructorId, year1, year2))

        for row in cursor:
            squadra.oldest_driver_dob = row["oldest_dob"]
        cursor.close()
        conn.close()
        return results

