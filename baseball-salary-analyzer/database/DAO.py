from database.DB_connect import DBConnect
from model.team import Team


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getAllYear():
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)

        # Questa query non è parametrica perchè il valore dell'anno è fornito dalla traccia
        query = """SELECT DISTINCT(t.year)
                    FROM teams t
                    WHERE t.year >= 1980"""
        cursor.execute(query)


        for row in cursor:
            result.append(row["year"])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getTeamsOfYear(year):
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)

        # Questa query è parametrica perchè il valore non è noto a priori
        query = """SELECT *
                    FROM teams t
                    WHERE t.year = %s"""
        cursor.execute(query, (year, ))

        for row in cursor:
            result.append(Team(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getSalariesTeam(year, idMapTeams):
        """Calcola la somma dei salari di ciascuna squadra in un determinato anno"""
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)

        # Questa query è parametrica perchè il valore non è noto a priori
        query = """SELECT t.ID, t.teamCode, sum(s.salary) as totSalary
                    FROM salaries s, teams t, appearances a
                    WHERE s.year = t.year and t.year = a.year and a.year = %s
                    AND t.ID = a.teamID and a.playerID = s.playerID 
                    GROUP BY t.ID, t.teamCode """
        cursor.execute(query, (year,))

        mapSalary = {} # dizionario che associa all'oggetto Team il salario totale

        # idMapTeams è un dizionario che associa all'ID l'oggetto Team
        for row in cursor: # associa all'oggetto Team (valore associato all'id di idMapTeams), il salario totale
            mapSalary[idMapTeams[row["ID"]]] = row["totSalary"]


        cursor.close()
        conn.close()
        return mapSalary
