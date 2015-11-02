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
                EmployeeCount INTEGER
                ) """
            self.cursor.execute(stat1)
            stat1 = """ INSERT INTO Sponsors (NAME, COUNTRY, EmployeeCount) VALUES('Ülker', 'Turkey', 23000)"""
            self.cursor.execute(stat1)
            stat1 = """ INSERT INTO Sponsors (NAME, COUNTRY, EmployeeCount) VALUES('Eti', 'Turkey', 30000)"""
            self.cursor.execute(stat1)
            stat1 = """ INSERT INTO Sponsors (NAME, COUNTRY, EmployeeCount) VALUES('Efes', 'Turkey', 45000)"""
            self.cursor.execute(stat1)
            stat1 = """ INSERT INTO Sponsors (NAME, COUNTRY, EmployeeCount) VALUES('Algida', 'Turkey', 2100)"""
            self.cursor.execute(stat1)
            self.connection.commit()
        except dbapi2.DatabaseError:
            self.connection.rollback()

    def select_sponsors(self):
        statement = """ SELECT * FROM Sponsors """
        self.cursor.execute(statement)
        return self.cursor

    def delete_sponsor(self,Id):
        stement =""" DELETE FROM Sponsors WHERE ID={}""".format(Id)
        self.cursor.execute(stement)
        self.connection.commit()

    def add_sponsor(self, name, country, age):
        if(name.strip() and country.strip() ):
            statement = """ INSERT INTO Sponsors (NAME, COUNTRY, EmployeeCount) VALUES('{}','{}',{})""".format(name, country, age)
            self.cursor.execute(statement)
            self.connection.commit()

    def close_con(self):
        self.connection.close()





