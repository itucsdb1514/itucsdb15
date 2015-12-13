import psycopg2 as dbapi2
from asyncio.locks import Condition

class Coaches:
    def __init__(self, dsn):
        self.connection = dbapi2.connect(dsn)
        self.cursor = self.connection.cursor()

    def create_table(self):
        try:
            stat1 = """ DROP TABLE Coaches """
            self.cursor.execute(stat1)
            self.connection.commit()
        except dbapi2.DatabaseError:
            self.connection.rollback()
        try:

            stat1 = """ CREATE TABLE Coaches (
                ID SERIAL PRIMARY KEY,
                NAME VARCHAR(40),
                COUNTRY VARCHAR(40),
                AGE INTEGER,
                FK_TeamsID INTEGER REFERENCES Teams ON DELETE CASCADE ON UPDATE CASCADE,
                FK_LeaguesID INTEGER REFERENCES Leagues ON DELETE CASCADE ON UPDATE CASCADE
                ) """
            self.cursor.execute(stat1)
            stat1 = """ INSERT INTO Coaches (NAME, COUNTRY, AGE, FK_TeamsID, FK_LeaguesID) VALUES('Joe Girardi', 'USA', 51,1,1)"""
            self.cursor.execute(stat1)
            stat1 = """ INSERT INTO Coaches (NAME, COUNTRY, AGE, FK_TeamsID, FK_LeaguesID) VALUES('John Farrell', 'USA', 53,2,1)"""
            self.cursor.execute(stat1)
            stat1 = """ INSERT INTO Coaches (NAME, COUNTRY, AGE, FK_TeamsID, FK_LeaguesID) VALUES('Bruce Bochy', 'FRA', 60,3,1)"""
            self.cursor.execute(stat1)
            self.connection.commit()

        except dbapi2.DatabaseError:
            self.connection.rollback()

    def select_coaches(self):
        statement = """ SELECT * FROM Coaches """
        self.cursor.execute(statement)
        return self.cursor

    def find_Coaches(self,team,league,name,country,age):
        condition=''
        if(name.strip()):
            condition+=""" NAME LIKE '%{}%' """.format(name)
        if(country.strip()):
            if(condition.strip()):
                condition+='AND'
            condition+=""" COUNTRY LIKE '%{}%' """.format(country)
        if(age.strip()):
            if(condition.strip()):
                condition+='AND'
            condition+=""" AGE = {} """.format(age)
        if(condition.strip()):
            condition=' WHERE '+condition

        statement = """ SELECT * FROM Coaches """+condition
        self.cursor.execute(statement)
        return self.cursor

    def delete_coach(self,Id):
        stement =""" DELETE FROM Coaches WHERE ID={}""".format(Id)
        self.cursor.execute(stement)
        self.connection.commit()

    def add_coach(self, team, league, name, country, age):
        if(name.strip() and country.strip() ):
            statement = """ INSERT INTO Coaches (FK_TeamsID,FK_LeaguesID, NAME, COUNTRY, AGE) VALUES({},{},'{}','{}',{})""".format(team,league, name, country, age)
            self.cursor.execute(statement)
            self.connection.commit()

    def update_coach(self, Id, name, country, age):
        statement = """UPDATE Coaches SET NAME = '{}', COUNTRY = '{}', AGE = {} WHERE ID = {}""".format( name, country, age, Id)
        self.cursor.execute(statement)
        self.connection.commit()


    def select_Joint_Coach(self):
        statement = """ SELECT Coaches.ID,Teams.Name,Leagues.Name, Coaches.NAME,Coaches.COUNTRY,AGE FROM Coaches INNER JOIN Teams ON Teams.ID=Coaches.FK_TeamsID INNER JOIN Leagues ON Leagues.ID=Coaches.FK_LeaguesID  """
        self.cursor.execute(statement)
        return self.cursor

    def find_Joint_Coach(self,team,league,name,country,age):
        statement = """ SELECT Coaches.ID,Teams.Name,Leagues.Name, Coaches.NAME,Coaches.COUNTRY,AGE FROM Coaches INNER JOIN Teams ON Teams.ID=Coaches.FK_TeamsID INNER JOIN Leagues ON Leagues.ID=Coaches.FK_LeaguesID """
        condition=''
        if(team.strip()):
            condition+=""" Teams.Name LIKE '%{}%'""".format(team)
        if(league.strip()):
            condition+=""" Leagues.Name LIKE '%{}%'""".format(league)
        if(name.strip()):
            if(condition.strip()):
                condition+='AND'
            condition+=""" Coaches.NAME LIKE '%{}%' """.format(name)
        if(country.strip()):
            if(condition.strip()):
                condition+='AND'
            condition+=""" Coaches.COUNTRY LIKE '%{}%' """.format(country)
        if(age.strip()):
            if(condition.strip()):
                condition+='AND'
            condition+=""" AGE={} """.format(age)
        if(condition.strip()):
            condition=' WHERE '+condition
        self.cursor.execute(statement+condition)
        return self.cursor

    def close_con(self):
        self.connection.close()
