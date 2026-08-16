from database.DB_connect import DBConnect
from model.actor import Actor

class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getAllRatings():
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)

        # Questa query non è parametrica
        query = """SELECT DISTINCT(r.avg_rating)
                    FROM ratings r
                    ORDER BY r.avg_rating"""
        cursor.execute(query)

        for row in cursor:
            result.append(row["avg_rating"]) # passo una riga semplice, non un oggetto

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllActors():
        """Recupera tutti gli attori con data di nascita valida e calcola l'età"""
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        result = []

        # L'età è calcolata come la differenza in anni tra la data di nascita e la data odierna
        # La data di nascita è valida se non è maggiore di quella odiera e non è NULL
        query = """
            SELECT n.id, n.name, n.height, n.date_of_birth, n.known_for_movies, TIMESTAMPDIFF(YEAR, n.date_of_birth, CURDATE()) AS age
            FROM names n
            WHERE n.date_of_birth IS NOT NULL
            AND n.date_of_birth <= CURDATE()
        """
        cursor.execute(query)

        # row deve contenere anche l'attributo age definito nella query
        for row in cursor:
            result.append(Actor(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllNodes(r1, r2, idMapA):
        """Recupera solo gli attori che hanno recitato in un film nel range di rating.
        Gli attori senza età valida sono già esclusi perché non presenti in idMapA."""
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)

        min_r = min(r1, r2)
        max_r = max(r1, r2)

        query = """
            SELECT DISTINCT rm.name_id AS id
            FROM ratings r, role_mapping rm
            WHERE rm.movie_id = r.movie_id 
              AND r.avg_rating BETWEEN %s AND %s
              AND rm.category IN ('actor', 'actress')
        """

        cursor.execute(query, (min_r, max_r))

        for row in cursor:
            # idMapA contiene solo attori validi
            if row["id"] in idMapA:
                result.append(idMapA[row["id"]])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getCoppieAttori(r1, r2):
        """Restituisce le coppie di attori con il peso dell'arco. Ogni tupla restituita ha forma:
            (id_attore_1, id_attore_2, peso), dove peso è la somma degli incassi dei film in comune."""

        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        result = []

        min_r = min(r1, r2)
        max_r = max(r1, r2)

        query = """
            SELECT 
                rm1.name_id AS id_1,
                rm2.name_id AS id_2,
                m.id AS movie_id,
                m.worlwide_gross_income AS incasso
            FROM role_mapping rm1, role_mapping rm2, movie m, ratings r
            WHERE rm1.movie_id = rm2.movie_id
              AND rm1.movie_id = m.id
              AND r.movie_id = m.id
              AND rm1.name_id > rm2.name_id
              AND r.avg_rating BETWEEN %s AND %s
              AND rm1.category IN ('actor', 'actress')
              AND rm2.category IN ('actor', 'actress')
              AND m.worlwide_gross_income IS NOT NULL
              AND m.worlwide_gross_income <> ''
        """

        cursor.execute(query, (min_r, max_r))

        # Dizionario per sommare gli incassi delle coppie di attori.
        # Chiave: (id_1, id_2)
        # Valore: peso totale dell'arco
        dizionario_pesi = {}

        for row in cursor:
            id_1 = row["id_1"]
            id_2 = row["id_2"]
            incasso = row["incasso"]

            incasso = incasso.replace("$", "")
            incasso = incasso.replace(",", "")
            incasso = incasso.strip()

            try:
                peso_film = int(incasso)
            except ValueError:
                continue

            coppia = (id_1, id_2)

            # Se è la prima volta che incontro questa coppia, inizializzo il peso.
            if coppia not in dizionario_pesi:
                dizionario_pesi[coppia] = 0

            # Sommo l'incasso del film corrente al peso totale della coppia.
            dizionario_pesi[coppia] += peso_film

        cursor.close()
        conn.close()

        # Trasformo il dizionario nella lista di tuple attesa dal Model.
        for coppia, peso_totale in dizionario_pesi.items():
            id_1, id_2 = coppia
            result.append((id_1, id_2, peso_totale))

        return result