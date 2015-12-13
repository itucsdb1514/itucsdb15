import psycopg2 as dbapi2


class Sponsors:
    def __init__(self, dsn):
        self.connection = dbapi2.connect(dsn)
        self.cursor = self.connection.cursor()

    def create_table(self):
        try:
            stat1 = """ DROP TABLE Sponsors """
            self.cursor.execute(stat1)
            self.connection.commit()
        except dbapi2.DatabaseError:
            self.connection.rollback()
        try:
            stat1 = """ CREATE TABLE Sponsors (
                ID SERIAL PRIMARY KEY,
                NAME VARCHAR(40),
                COUNTRY VARCHAR(40),
                FK_Teams int REFERENCES Teams ON DELETE CASCADE ON UPDATE CASCADE
                ) """
            self.cursor.execute(stat1)
            stat1 = """ INSERT INTO Sponsors (NAME, COUNTRY, FK_Teams) VALUES('Ülker', 'Turkey', 1)"""
            self.cursor.execute(stat1)
            stat1 = """ INSERT INTO Sponsors (NAME, COUNTRY, FK_Teams) VALUES('Eti', 'Turkey', 2)"""
            self.cursor.execute(stat1)
            stat1 = """ INSERT INTO Sponsors (NAME, COUNTRY, FK_Teams) VALUES('Efes', 'Turkey', 3)"""
            self.cursor.execute(stat1)
            stat1 = """ INSERT INTO Sponsors (NAME, COUNTRY, FK_Teams) VALUES('Algida', 'Turkey', 3)"""
            self.cursor.execute(stat1)
            self.connection.commit()
        except dbapi2.DatabaseError:
            self.connection.rollback()

    def select_sponsors(self):
        statement = """ SELECT Sponsors.ID,Sponsors.NAME,Sponsors.COUNTRY,TEAMS.NAME   FROM Sponsors INNER JOIN TEAMS ON TEAMS.ID=Sponsors.FK_Teams """
        self.cursor.execute(statement)
        return self.cursor
    def Find_sponsors(self,name,country,team):
        condition=''
        if(name.strip()):
            condition+=""" Sponsors.NAME LIKE '%{}%' """.format(name)
        if(country.strip()):
            if(condition.strip()):
                condition+='AND'
            condition+=""" Sponsors.COUNTRY LIKE '%{}%' """.format(country)
        if(team.strip()):
            if(condition.strip()):
                condition+='AND'
            condition+=""" Sponsors.FK_Teams = {} """.format(team)
        if(condition.strip()):
            condition=' WHERE '+ condition
        statement = """ SELECT Sponsors.ID,Sponsors.NAME,Sponsors.COUNTRY,TEAMS.NAME   FROM Sponsors INNER JOIN TEAMS ON TEAMS.ID=Sponsors.FK_Teams """
        statement=statement+condition
        print(statement)
        self.cursor.execute(statement)
        return self.cursor
    def delete_sponsor(self,Id):
        stement =""" DELETE FROM Sponsors WHERE ID={}""".format(Id)
        self.cursor.execute(stement)
        self.connection.commit()

    def add_sponsor(self, name, country, age):
        if(name.strip() and country.strip() ):
            statement = """ INSERT INTO Sponsors (NAME, COUNTRY, FK_Teams) VALUES('{}','{}',{})""".format(name, country, age)
            self.cursor.execute(statement)
            self.connection.commit()

    def close_con(self):
        self.connection.close()





