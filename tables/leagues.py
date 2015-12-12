import psycopg2 as dbapi2


class Leagues:
    def __init__(self, dsn):
        self.connection = dbapi2.connect(dsn)
        self.cursor = self.connection.cursor()

    def create_table(self):
        try:
            stat1 = """ DROP TABLE Leagues """
            self.cursor.execute(stat1)
            self.connection.commit()
        except dbapi2.DatabaseError:
            self.connection.rollback()
        try:
            stat1 = """ CREATE TABLE Leagues (
                ID SERIAL PRIMARY KEY,
                NAME VARCHAR(40),
                COUNTRY VARCHAR(40),
                YEAR INTEGER
                ) """
            self.cursor.execute(stat1)
            stat1 = """ INSERT INTO Leagues (NAME, COUNTRY, YEAR) VALUES('Major League Baseball', 'USA', 1903)"""
            self.cursor.execute(stat1)
            stat1 = """ INSERT INTO Leagues (NAME, COUNTRY, YEAR) VALUES('Minor League Baseball', 'USA', 1868)"""
            self.cursor.execute(stat1)
            stat1 = """ INSERT INTO Leagues (NAME, COUNTRY, YEAR) VALUES('Dominican Professional Baseball League', 'DOM', 1951)"""
            self.cursor.execute(stat1)
            self.connection.commit()
        except dbapi2.DatabaseError:
            self.connection.rollback()

    def select_leagues(self):
        statement = """ SELECT * FROM Leagues """
        self.cursor.execute(statement)
        return self.cursor

    def update_league(self, Id, name, country, year):
        statement = """UPDATE Leagues SET NAME = '{}', COUNTRY = '{}', YEAR = {} WHERE ID = {}""".format( name, country, year, Id)
        self.cursor.execute(statement)
        self.connection.commit()


    def find_leagues(self, name, country, year):
        condition=''
        if(name.strip()):
            condition+=""" NAME LIKE '%{}%' """.format(name)
        if(country.strip()):
            if(condition.strip()):
                condition+='AND'
            condition+=""" COUNTRY LIKE '%{}%' """.format(country)
        if(year.strip()):
            if(condition.strip()):
                condition+='AND'
            condition+=""" YEAR = {} """.format(year)
        if(condition.strip()):
            condition=' WHERE '+ condition

        statement = """ SELECT * FROM Leagues """+condition
        self.cursor.execute(statement)
        return self.cursor


    def delete_league(self,Id):
        stement =""" DELETE FROM Leagues WHERE ID={}""".format(Id)
        self.cursor.execute(stement)
        self.connection.commit()

    def add_league(self, name, country, year):
        if(name.strip() and country.strip() ):
            statement = """ INSERT INTO Leagues (NAME, COUNTRY, YEAR) VALUES('{}','{}',{})""".format(name, country, year)
            self.cursor.execute(statement)
            self.connection.commit()

    def close_con(self):
        self.connection.close()
