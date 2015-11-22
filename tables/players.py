import psycopg2 as dbapi2


class Players:
    def __init__(self, dsn):
        self.connection = dbapi2.connect(dsn)
        self.cursor = self.connection.cursor()

    def create_table(self):
        try:
            stat1 = """ DROP TABLE PLAYERS """
            self.cursor.execute(stat1)
            self.connection.commit()
        except dbapi2.DatabaseError:
            self.connection.rollback()
        try:
            stat1 = """ CREATE TABLE PLAYERS (
                ID SERIAL PRIMARY KEY,
                NAME VARCHAR(40),
                COUNTRY VARCHAR(40),
                AGE INTEGER
                ) """
            self.cursor.execute(stat1)
            print('*********')
            stat1 = """ INSERT INTO PLAYERS (NAME, COUNTRY, AGE) VALUES('Ahmet Sezer', 'Turkey', 23)"""
            self.cursor.execute(stat1)
            stat1 = """ INSERT INTO PLAYERS (NAME, COUNTRY, AGE) VALUES('Yılmaz Kel', 'Turkey', 30)"""
            self.cursor.execute(stat1)
            stat1 = """ INSERT INTO PLAYERS (NAME, COUNTRY, AGE) VALUES('Hüseyin Yavuz', 'Turkey', 45)"""
            self.cursor.execute(stat1)
            stat1 = """ INSERT INTO PLAYERS (NAME, COUNTRY, AGE) VALUES('Burak Bayboğa', 'Turkey', 21)"""
            self.cursor.execute(stat1)
            self.connection.commit()
        except dbapi2.DatabaseError:
            self.connection.rollback()

    def select_players(self):
        statement = """ SELECT * FROM PLAYERS """
        self.cursor.execute(statement)
        return self.cursor

    def update_player(self, Id, name, country, age):
        statement = """UPDATE PLAYERS SET NAME = '{}', COUNTRY = '{}', AGE = {} WHERE ID = {}""".format( name, country, age, Id)
        self.cursor.execute(statement)
        self.connection.commit()

    def find_Players(self, name, country, age):
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
            condition=' WHERE '+ condition

        statement = """ SELECT * FROM PLAYERS """+condition
        self.cursor.execute(statement)
        return self.cursor

    def delete_player(self,Id):
        stement =""" DELETE FROM PLAYERS WHERE ID={}""".format(Id)
        self.cursor.execute(stement)
        self.connection.commit()

    def add_player(self, name, country, age):
        if(name.strip() and country.strip() ):
            statement = """ INSERT INTO PLAYERS (NAME, COUNTRY, AGE) VALUES('{}','{}',{})""".format(name, country, age)
            self.cursor.execute(statement)
            self.connection.commit()

    def close_con(self):
        self.connection.close()





