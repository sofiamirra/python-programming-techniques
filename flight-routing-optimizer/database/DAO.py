from database.DB_connect import DBConnect
from model.airport import Airport
from model.tratta import Tratta

class DAO():

    @staticmethod
    def getAllAirports():
        """Recupera tytti gli aeroporti per popolare la mappa del Model"""
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        # Query semplice per costuire l'oggetto Airport
        query = """SELECT * from airports a order by a.AIRPORT asc"""
        cursor.execute(query)

        for row in cursor:
            # Il costrutto **row, mappa le colonne del DB agli attributi dell'oggetto
            result.append(Airport(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllNodes(n, idMapA):
        """Recupera solo gli aeroporti con almeno N compagnie di volo (nodi del grafo)"""
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        # La subquery conta prima le compagnie per ogni aeroporto
        # poi filtra quelli che ne hanno almeno N
        query = """SELECT t.ID, t.IATA_CODE, count(*) as N
                    FROM (select a.ID, a.IATA_CODE, f.AIRLINE_ID, count(*)
                    from airports a, flights f
                    where a.ID = f.ORIGIN_AIRPORT_ID 
                    or a.ID = f.DESTINATION_AIRPORT_ID 
                    GROUP BY a.ID, a.IATA_CODE, f.AIRLINE_ID ) t
                    GROUP BY t.ID, t.IATA_CODE
                    having N >= %s
                    order by N asc"""
        cursor.execute(query, (n, ))

        for row in cursor:
            # Inserisce tra i risultati l'oggetto Airport con l'ID dato dal DB
            result.append(idMapA[row["ID"]])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllEdges(idMapA):
        """Recupera tutte le rotte e conta i voli totali tra coppie di aeroporti"""
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)

        # Conta il totale dei voli che partono da A1 e arrivano a A2 (es. Roma, Milano, 500)
        query = """SELECT f.ORIGIN_AIRPORT_ID , f.DESTINATION_AIRPORT_ID, count(*) as peso 
                    FROM flights f
                    GROUP BY f.ORIGIN_AIRPORT_ID, f.DESTINATION_AIRPORT_ID
                    ORDER BY f.ORIGIN_AIRPORT_ID, f.DESTINATION_AIRPORT_ID
                    """
        cursor.execute(query)

        for row in cursor:
            result.append(Tratta(
                idMapA[row["ORIGIN_AIRPORT_ID"]],
                idMapA[row["DESTINATION_AIRPORT_ID"]],
                row["peso"]))

        cursor.close()
        conn.close()
        return result



