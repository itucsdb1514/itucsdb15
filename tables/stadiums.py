import psycopg2 as dbapi2


class Stadiums:
    def __init__(self, dsn):
        self.connection = dbapi2.connect(dsn)
        self.cursor = self.connection.cursor()

    def create_table(self):
        try:
            stat1 = """ DROP TABLE Stadiums """
            self.cursor.execute(stat1)
            self.connection.commit()
        except dbapi2.DatabaseError:
            self.connection.rollback()
        try:
            stat1 = """ CREATE TABLE Stadiums (
                ID SERIAL PRIMARY KEY,
                NAME VARCHAR(40),
                CITY VARCHAR(40),
                YEAR INTEGER
                ) """
            self.cursor.execute(stat1)
            stat1 = """ INSERT INTO Stadiums (NAME, CITY, YEAR) VALUES('StadiumOne', 'CityOne', 1900)"""
            self.cursor.execute(stat1)
            stat1 = """ INSERT INTO Stadiums (NAME, CITY, YEAR) VALUES('StadiumTwo', 'CityTwo', 1901)"""
            self.cursor.execute(stat1)
            self.connection.commit()
        except dbapi2.DatabaseError:
            self.connection.rollback()

    def select_stadiums(self):
        statement = """ SELECT * FROM Stadiums """
        self.cursor.execute(statement)
        return self.cursor

    def delete_stadium(self,Id):
        stement =""" DELETE FROM Stadiums WHERE ID={}""".format(Id)
        self.cursor.execute(stement)
        self.connection.commit()

    def add_stadium(self, name, city, year):
        if(name.strip() and city.strip() ):
            statement = """ INSERT INTO Stadiums (NAME, CITY, YEAR) VALUES('{}','{}',{})""".format(name, city, year)
            self.cursor.execute(statement)
            self.connection.commit()

    def update_stadium(self, Id, name, city, year):
        statement = """UPDATE Stadiums SET NAME = '{}', CITY = '{}', YEAR = {} WHERE ID = {}""".format( name, city, year, Id)
        self.cursor.execute(statement)
        self.connection.commit()

    def find_Stadiums(self, name, city, year):
        condition=''
        if(name.strip()):
            condition+=""" NAME LIKE '%{}%' """.format(name)
        if(city.strip()):
            if(condition.strip()):
                condition+='AND'
            condition+=""" CITY LIKE '%{}%' """.format(city)
        if(year.strip()):
            if(condition.strip()):
                condition+='AND'
            condition+=""" YEAR = {} """.format(year)
        if(condition.strip()):
            condition=' WHERE '+ condition

        statement = """ SELECT * FROM Stadiums """+condition
        self.cursor.execute(statement)
        return self.cursor

    def close_con(self):
        self.connection.close()





