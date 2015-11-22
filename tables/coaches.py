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
                FK_TeamsID INTEGER REFERENCES Teams
                ) """
            self.cursor.execute(stat1)
            stat1 = """ INSERT INTO Coaches (NAME, COUNTRY, AGE, FK_TeamsID) VALUES('Joe Girardi', 'USA', 51,1)"""
            self.cursor.execute(stat1)
            stat1 = """ INSERT INTO Coaches (NAME, COUNTRY, AGE, FK_TeamsID) VALUES('John Farrell', 'USA', 53,2)"""
            self.cursor.execute(stat1)
            stat1 = """ INSERT INTO Coaches (NAME, COUNTRY, AGE, FK_TeamsID) VALUES('Bruce Bochy', 'FRA', 60,3)"""
            self.cursor.execute(stat1)
            self.connection.commit()

        except dbapi2.DatabaseError:
            self.connection.rollback()

    def select_coaches(self):
        statement = """ SELECT * FROM Coaches """
        self.cursor.execute(statement)
        return self.cursor

    def find_Coaches(self,team,name,country,age):
        condition=''
        if(name.strip()):
            if(condition.strip()):
                condition+='AND'
            condition+=""" NAME='{}' """.format(name)
        if(country.strip()):
            if(condition.strip()):
                condition+='AND'
            condition+=""" COUNTRY={} """.format(country)
        if(age.strip()):
            if(condition.strip()):
                condition+='AND'
            condition+=""" AGE={} """.format(age)
        if(condition.strip()):
            condition=' WHERE '+condition

        statement = """ SELECT * FROM Coaches """+condition
        self.cursor.execute(statement)
        return self.cursor

    def delete_coach(self,Id):
        stement =""" DELETE FROM Coaches WHERE ID={}""".format(Id)
        self.cursor.execute(stement)
        self.connection.commit()

    def add_coach(self, team, name, country, age):
        if(name.strip() and country.strip() ):
            statement = """ INSERT INTO Coaches (FK_TeamsID, NAME, COUNTRY, AGE) VALUES({},'{}','{}',{})""".format(team, name, country, age)
            self.cursor.execute(statement)
            self.connection.commit()

    def update_coach(self, Id, name, country, age):
        statement = """UPDATE Coaches SET NAME = '{}', COUNTRY = '{}', AGE = {} WHERE ID = {}""".format( name, country, age, Id)
        self.cursor.execute(statement)
        self.connection.commit()


    def select_Joint_Coach(self):
        statement = """ SELECT Coaches.ID,Teams.Name,Coaches.NAME,Coaches.COUNTRY,AGE FROM Coaches INNER JOIN Teams ON Teams.ID=Coaches.FK_TeamsID  """
        self.cursor.execute(statement)
        return self.cursor

    def find_Joint_Coach(self,team,name,country,age):
        statement = """ SELECT Coaches.ID,Teams.Name,Coaches.NAME,Coaches.COUNTRY,AGE FROM Coaches INNER JOIN Teams ON Teams.ID=Coaches.FK_TeamsID  """
        condition=''
        if(team.strip()):
            condition+=""" Teams.Name='{}' """.format(team)
        if(name.strip()):
            if(condition.strip()):
                condition+='AND'
            condition+=""" Coaches.NAME='{}' """.format(name)
        if(country.strip()):
            if(condition.strip()):
                condition+='AND'
            condition+=""" Coaches.COUNTRY='{}' """.format(country)
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
