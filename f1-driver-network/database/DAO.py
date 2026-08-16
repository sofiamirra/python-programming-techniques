from database.DB_connect import DBConnect
from model.arco import Arco
from model.driver import Driver

class DAO():

    @staticmethod
    def getAllYears():
        """ Recupera dal database la lista di tutti gli anni presenti nelle stagioni dal piu vecchio al piu recente"""
        conn = DBConnect.get_connection()
        results = []

        cursor = conn.cursor(dictionary=True)
        query = "SELECT distinct year FROM seasons s  ORDER BY year"

        cursor.execute(query)

        for row in cursor:
            # estrazione del singolo campo anno senza creare un oggetto
            results.append(row["year"])

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllNodes(year1, year2):
        """Recupera dal database tutti i piloti che hanno partecipato alle gare nel lasso di tempo indicato senza duplicati"""
        conn = DBConnect.get_connection()
        results = []

        cursor = conn.cursor(dictionary=True)
        # select usa d.* per prendere solo i campi del pilota anche se ci sono piu tabelle
        query = """SELECT DISTINCT d.*
                FROM drivers d, races r, results re
                WHERE r.raceId = re.raceId AND re.driverId = d.driverId  
                AND r.year BETWEEN %s AND %s
                AND re.position IS NOT NULL
                ORDER BY d.driverId
                """

        cursor.execute(query, (year1, year2))

        for row in cursor:
            results.append(Driver(**row))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllEdges(year1, year2, idMapD):
        """Metodo per la creazione degli archi dal DB"""
        conn = DBConnect.get_connection()
        results = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT r1.driverId as id1, r2.driverId as id2, COUNT(*) as peso
                FROM results r1, results r2, races r
                    WHERE r.raceId = r1.raceId AND r.raceId = r2.raceId
                    AND r1.constructorId = r2.constructorId
                    AND r1.position IS NOT NULL
                    AND r2.position IS NOT NULL
                    AND r1.driverId > r2.driverId 
                    AND r.year BETWEEN %s AND %s
                    GROUP BY r1.driverId, r2.driverId """

        cursor.execute(query, (year1, year2))

        for row in cursor:
            # impacchetto i dati direttamente nell'oggetto DTO
            results.append(Arco(idMapD[row["id1"]], idMapD[row["id2"]], row["peso"]))

        cursor.close()
        conn.close()
        return results

