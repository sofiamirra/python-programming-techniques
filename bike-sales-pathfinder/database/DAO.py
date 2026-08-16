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

        cursor = conn.cursor(dictionary=True)
        query = """SELECT DISTINCT * 
        FROM categories"""

        cursor.execute(query)

        for row in cursor:
            results.append(Category(**row))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllNodes(categoryId):
        conn = DBConnect.get_connection()
        results = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT DISTINCT p.*
        FROM products p
        WHERE p.category_id = %s"""

        cursor.execute(query, (categoryId, ))

        for row in cursor:
            results.append(Product(**row))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllEdges(date1, date2, categoryId, idMapP):
        conn = DBConnect.get_connection()
        results = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT t1.product_id as id1, t2.product_id as id2, t1.n + t2.n as peso
        FROM (SELECT oi.product_id, SUM(oi.quantity) as n 
        FROM order_items oi, orders o, products p
        WHERE o.order_id = oi.order_id AND p.product_id = oi.product_id 
        AND o.order_date BETWEEN %s AND %s
        AND p.category_id = %s
        GROUP BY oi.product_id) as t1, 
        (SELECT oi.product_id, SUM(oi.quantity) as n 
        FROM order_items oi, orders o, products p
        WHERE o.order_id = oi.order_id AND p.product_id = oi.product_id 
        AND o.order_date BETWEEN %s AND %s
        AND p.category_id = %s
        GROUP BY oi.product_id) as t2
        WHERE t1.product_id <> t2.product_id 
        AND t1.n >= t2.n
        GROUP BY t1.product_id, t2.product_id"""

        cursor.execute(query, (date1, date2, categoryId, date1, date2, categoryId))

        for row in cursor:
            results.append(Arco(idMapP[row["id1"]], idMapP[row["id2"]], row["peso"]))

        cursor.close()
        conn.close()
        return results
