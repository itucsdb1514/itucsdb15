import psycopg2 as dbapi2
from asyncio.locks import Condition

class Betrates:
    def __init__(self, dsn):
        self.connection = dbapi2.connect(dsn)
        self.cursor = self.connection.cursor()

    def create_table(self):
        try:
            stat1 = """ DROP TABLE Betrates """
            self.cursor.execute(stat1)
            self.connection.commit()
        except dbapi2.DatabaseError:
            self.connection.rollback()
        try:
            stat1 = """ CREATE TABLE Betrates (
                ID SERIAL PRIMARY KEY,
                HOME INTEGER,
                AWAY INTEGER,
                DRAW INTEGER,
                FK_MatchesID INTEGER REFERENCES MATCHES ON DELETE CASCADE ON UPDATE CASCADE
                ) """
            self.cursor.execute(stat1)
            stat1 = """ INSERT INTO Betrates (HOME, AWAY, DRAW, FK_MatchesID) VALUES(2, 5, 15,1)"""
            self.cursor.execute(stat1)
            stat1 = """ INSERT INTO Betrates (HOME, AWAY, DRAW, FK_MatchesID) VALUES(2, 3, 4,2)"""
            self.cursor.execute(stat1)
            self.connection.commit()
        except dbapi2.DatabaseError:
            self.connection.rollback()

    def delete_betrate(self,Id):
        stement =""" DELETE FROM Betrates WHERE ID={}""".format(Id)
        self.cursor.execute(stement)
        self.connection.commit()

    def add_betrate(self, home, away, draw, match):
        statement = """ INSERT INTO Betrates (HOME, AWAY, DRAW, FK_MatchesID) VALUES({},{},{},'{}')""".format(home, away, draw, match)
        self.cursor.execute(statement)
        self.connection.commit()

    def update_betrate(self, Id, home, away, draw):
        statement = """UPDATE Betrates SET HOME = {}, AWAY = {}, DRAW = {} WHERE ID = {}""".format(home, away, draw, Id)
        self.cursor.execute(statement)
        self.connection.commit()

    def select_Joint_Betrate(self):
        statement = """ SELECT Betrates.ID, Matches.OP1, Matches.OP2, HOME, AWAY, DRAW FROM Betrates INNER JOIN Matches ON Matches.ID = Betrates.FK_MatchesID """
        self.cursor.execute(statement)
        return self.cursor

    def find_Joint_Betrate(self, home, away, draw, match1, match2):
        statement = """ SELECT Betrates.ID, Matches.OP1, Matches.OP2, Home, Away, Draw FROM Betrates INNER JOIN Matches ON Matches.ID = Betrates.FK_MatchesID """
        condition=''
        if(match1.strip()):
            condition+=""" Matches.OP1='{}' """.format(match1)
        if(match2.strip()):
            if(condition.strip()):
                condition+=' AND'
            condition+=""" Matches.OP2='{}' """.format(match2)
        if(home.strip()):
            if(condition.strip()):
                condition+=' AND'
            condition+=""" HOME={} """.format(home)
        if(away.strip()):
            if(condition.strip()):
                condition+=' AND'
            condition+= """ AWAY={} """.format(away)
        if(draw.strip()):
            if(condition.strip()):
                condition+=' AND'
            condition+= """ DRAW = {} """.format(draw)
        if(condition.strip()):
            condition = ' WHERE ' + condition
        self.cursor.execute(statement+condition)
        return self.cursor


    def close_con(self):
        self.connection.close()





