import psycopg2 as dbapi2
from asyncio.locks import Condition

class Matches:
    def __init__(self, dsn):
        self.connection = dbapi2.connect(dsn)
        self.cursor = self.connection.cursor()

    def create_table(self):
        try:
            stat1 = """ DROP TABLE Matches """
            self.cursor.execute(stat1)
            self.connection.commit()
        except dbapi2.DatabaseError:
            self.connection.rollback()
        try:
            stat1 = """ CREATE TABLE Matches (
                ID SERIAL PRIMARY KEY,
                OP1 VARCHAR(40),
                OP2 VARCHAR(40),
                YEAR INTEGER,
                FK_StadiumsID INTEGER REFERENCES STADIUMS ON DELETE CASCADE ON UPDATE CASCADE
                ) """
            self.cursor.execute(stat1)
            stat1 = """ INSERT INTO Matches (OP1, OP2, YEAR, FK_StadiumsID) VALUES('fener', 'galata', 1900,1)"""
            self.cursor.execute(stat1)
            stat1 = """ INSERT INTO Matches (OP1, OP2, YEAR, FK_StadiumsID) VALUES('besiktas', 'trabzon', 1901,2)"""
            self.cursor.execute(stat1)
            self.connection.commit()
        except dbapi2.DatabaseError:
            self.connection.rollback()

    def delete_match(self,Id):
        stement =""" DELETE FROM Matches WHERE ID={}""".format(Id)
        self.cursor.execute(stement)
        self.connection.commit()

    def add_match(self, op1, op2, year, stadium):
        if(op1.strip() and op2.strip() ):
            statement = """ INSERT INTO Matches (OP1, OP2, YEAR, FK_StadiumsID) VALUES('{}','{}',{}, '{}')""".format(op1, op2, year, stadium)
            self.cursor.execute(statement)
            self.connection.commit()

    def update_match(self, Id, op1, op2):
        statement = """UPDATE Matches SET OP1 = '{}', OP2 = '{}' WHERE ID = {}""".format(op1, op2, Id)
        self.cursor.execute(statement)
        self.connection.commit()

    def select_Joint_Match(self):
        statement = """ SELECT Matches.ID, Stadiums.Name, OP1, OP2, Matches.YEAR FROM Matches INNER JOIN Stadiums ON Stadiums.ID = Matches.FK_StadiumsID """
        self.cursor.execute(statement)
        return self.cursor

    def find_Joint_Match(self, op1, op2, year, stadium):
        statement = """ SELECT Matches.ID, Stadiums.Name, OP1, OP2, Matches.YEAR FROM Matches INNER JOIN Stadiums ON Stadiums.ID = Matches.FK_StadiumsID """
        condition=''
        if(stadium.strip()):
            condition+=""" Stadiums.Name LIKE '%{}%' """.format(stadium)
        if(op1.strip()):
            if(condition.strip()):
                condition+=' AND'
            condition+=""" OP1  LIKE '%{}%' """.format(op1)
        if(op2.strip()):
            if(condition.strip()):
                condition+=' AND'
            condition+= """ OP2 LIKE '%{}%' """.format(op2)
        if(year.strip()):
            if(condition.strip()):
                condition+=' AND'
            condition+= """ Matches.YEAR = {} """.format(year)
        if(condition.strip()):
            condition = ' WHERE ' + condition
        self.cursor.execute(statement+condition)
        return self.cursor


    def close_con(self):
        self.connection.close()





