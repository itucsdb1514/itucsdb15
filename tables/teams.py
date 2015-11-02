import psycopg2 as dbapi2


class Teams:
    def __init__(self, dsn):
        self.connection = dbapi2.connect(dsn)
        self.cursor = self.connection.cursor()

    def create_table(self):
        try:
            stat1 = """ DROP TABLE Teams """
            self.cursor.execute(stat1)
            self.connection.commit()
        except dbapi2.DatabaseError:
            self.connection.rollback()
        try:
            stat1 = """ CREATE TABLE Teams (
                ID SERIAL PRIMARY KEY,
                NAME VARCHAR(40),
                COUNTRY VARCHAR(40),
                YEAR INTEGER
                ) """
            self.cursor.execute(stat1)
            stat1 = """ INSERT INTO Teams (NAME, COUNTRY, YEAR) VALUES('New York Yankees', 'USA', 1901)"""
            self.cursor.execute(stat1)
            stat1 = """ INSERT INTO Teams (NAME, COUNTRY, YEAR) VALUES('Boston Red Sox', 'USA', 1903)"""
            self.cursor.execute(stat1)
            stat1 = """ INSERT INTO Teams (NAME, COUNTRY, YEAR) VALUES('San Francisco Giants', 'USA', 1883)"""
            self.cursor.execute(stat1)
            self.connection.commit()
        except dbapi2.DatabaseError:
            self.connection.rollback()

    def select_teams(self):
        statement = """ SELECT * FROM Teams """
        self.cursor.execute(statement)
        return self.cursor

    def delete_team(self,Id):
        stement =""" DELETE FROM Teams WHERE ID={}""".format(Id)
        self.cursor.execute(stement)
        self.connection.commit()

    def add_team(self, name, country, year):
        if(name.strip() and country.strip() ):
            statement = """ INSERT INTO Teams (NAME, COUNTRY, YEAR) VALUES('{}','{}',{})""".format(name, country, year)
            self.cursor.execute(statement)
            self.connection.commit()

    def close_con(self):
        self.connection.close()
