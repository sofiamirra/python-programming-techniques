from database.DB_connect import DBConnect
from model.artist import Artist
from model.genre import Genre


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getAllGenres():
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)

        # Questa query non è parametrica
        query = """SELECT *
                FROM Genre"""
        cursor.execute(query)

        for row in cursor:
            result.append(Genre(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllArtists():
        """Recupera tutti gli artisti per popolare la mappa del Model"""
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        result = []

        query = """SELECT * 
                FROM artist a"""
        cursor.execute(query)

        for row in cursor:
            result.append(Artist(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllNodes(g, idMapA):
        """Recupera solo gli Artisti che possiedono almeno un brano appartenente a quel genere (nodi del grafo)"""
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)

        query = """SELECT DISTINCT(a.ArtistId)
                FROM artist a, album ab, track t
                WHERE a.ArtistId = ab.ArtistId AND t.AlbumId = ab.AlbumId AND t.GenreId = %s
                """
        cursor.execute(query, (g, ))

        for row in cursor:
            # Inserisce tra i risultati l'oggetto Artist con l'Id dato dal DB
            result.append(idMapA[row["ArtistId"]])

        cursor.close()
        conn.close()
        return result

    # Si utilizzano due query separate nel DAO (una per le Popolarità, una per gli Archi)
    # per evitare una singola query SQL troppo pesante.
    # Il DB esegue calcoli semplici, mentre Model si occupa di incrociare i dati.
    @staticmethod
    def getMappaPopolarita(genre_id):
        """Conta la popolarità per ciascun artista"""
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)

        # Conta la popolarità (somma di brani venduti per ciascun artista)
        query = """SELECT a.Name, a.ArtistId, sum(il.Quantity) as popolarita
                FROM track t, album ab, artist a, InvoiceLine il
                WHERE t.TrackId = il.TrackId AND ab.AlbumId = t.AlbumId AND ab.ArtistId = a.ArtistId 
                AND t.GenreId = %s
                GROUP BY a.ArtistId, a.Name 
                        """
        cursor.execute(query, (genre_id, ))

        # Restituisce un dizionario {ArtistId1: 150, ArtistId1: 300}
        mappa = {}
        for row in cursor:
            mappa[row["ArtistId"]] = row["popolarita"]

        cursor.close()
        conn.close()
        return mappa

    @staticmethod
    def getCoppieArtisti(g):
        """Recupera le coppie di ID degli artisti (filtrati per genere)
        che condividono almeno un acquisto da parte dello stesso cliente"""
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        result = []

        # Trova coppie uniche di artisti (del genere scelto) acquistati dallo stesso cliente
        # La condizione a1.ArtistId > a2.ArtistId evita archi ripetuti (A-B e B-A)
        query = """
                SELECT DISTINCT a1.ArtistId AS a1_id, a2.ArtistId AS a2_id
                FROM track t1, album al1, artist a1, invoiceline il1, invoice i1, 
                     invoice i2, invoiceline il2, track t2, album al2, artist a2
                WHERE 
                    t1.AlbumId = al1.AlbumId 
                    AND al1.ArtistId = a1.ArtistId 
                    AND t1.TrackId = il1.TrackId 
                    AND il1.InvoiceId = i1.InvoiceId 
                    
                    AND i1.CustomerId = i2.CustomerId 
                    
                    AND i2.InvoiceId = il2.InvoiceId 
                    AND il2.TrackId = t2.TrackId 
                    AND t2.AlbumId = al2.AlbumId 
                    AND al2.ArtistId = a2.ArtistId 
                    
                    AND t1.GenreId = %s 
                    AND t2.GenreId = %s 
                    AND a1.ArtistId > a2.ArtistId
            """

        # Passo due volte 'g' perché il parametro %s compare due volte nella query (t1 e t2)
        cursor.execute(query, (g, g))

        for row in cursor:
            # Restituisco una semplice tupla con i due ID
            result.append((row["a1_id"], row["a2_id"]))

        cursor.close()
        conn.close()
        return result