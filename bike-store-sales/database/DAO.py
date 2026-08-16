from database.DB_connect import DBConnect
from model.arco import Arco
from model.category import Category
from model.product import Product


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getDateRange():

        conn = DBConnect.get_connection()
        results = []

        cursor = conn.cursor(dictionary=True)
        query = "SELECT distinct (order_date) from orders o order by order_date"

        cursor.execute(query)

        for row in cursor:
            results.append(row["order_date"])

        first = results[0]
        last = results[-1]

        cursor.close()
        conn.close()
        return first, last

    @staticmethod
    def getCategorie():

        conn = DBConnect.get_connection()
        results = []

        """Query che seleziona l'intero oggetto Category"""
        cursor = conn.cursor(dictionary=True)
        query =  """SELECT * FROM
        categories """

        cursor.execute(query)

        for row in cursor:
            results.append(Category(**row)) # lista di oggetti Category

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getProductsByCategory(category):

        conn = DBConnect.get_connection()
        results = []

        cursor = conn.cursor(dictionary=True)
        query =  """SELECT * 
            FROM products p
            WHERE p.category_id = %s"""

        cursor.execute(query, (category.category_id,))

        for row in cursor:
            results.append(Product(**row))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllEdges(category, d1, d2, idMapP):
        """La costruzione degli archi viene delegata interamente al DataBase"""
        conn = DBConnect.get_connection()
        results = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT t1.product_id as id1, t2.product_id as id2, t1.n as nid1, t2.n as nid2, t1.n + t2.n as peso
                FROM (SELECT p.product_id, count(*) as n
                FROM products p, order_items oi, orders o
                WHERE oi.order_id = o.order_id AND oi.product_id = p.product_id 
                AND o.order_date BETWEEN %s AND %s
                AND p.category_id = %s
                GROUP BY p.product_id 
                ) t1, 
                (SELECT p.product_id, count(*) as n
                FROM products p, order_items oi, orders o
                WHERE oi.order_id = o.order_id AND oi.product_id = p.product_id 
                AND o.order_date BETWEEN %s AND %s
                AND p.category_id = %s
                GROUP BY p.product_id 
                ) t2
                WHERE t1.product_id <> t2.product_id 
                AND t1.n >= t2.n
                ORDER BY peso desc"""
        # RECALL: <> non collega un nodo a sè stesso, >= gestisce la direzione dell'arco (dal maggiore al minore)
        cursor.execute(query, (d1, d2, category.category_id, d1, d2, category.category_id)) # passo tutti e 6 i parametri

        for row in cursor:
            results.append(Arco(idMapP[row["id1"]], idMapP[row["id2"]], row["peso"]))

        cursor.close()
        conn.close()
        return results