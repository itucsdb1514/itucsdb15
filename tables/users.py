import psycopg2 as dbapi2


class Users:
    def __init__(self, dsn):
        self.connection = dbapi2.connect(dsn)
        self.cursor = self.connection.cursor()

    def create_table(self):
        try:
            stat1 = """ DROP TABLE USERS """
            self.cursor.execute(stat1)
            self.connection.commit()
        except dbapi2.DatabaseError:
            self.connection.rollback()
        try:
            stat1 = """ CREATE TABLE USERS (
                ID SERIAL PRIMARY KEY,
                UNAME VARCHAR(40),
                UTYPE VARCHAR(40),
                BIRTH INTEGER
                ) """
            self.cursor.execute(stat1)
            print('*********')
            stat1 = """ INSERT INTO USERS (UNAME, UTYPE, BIRTH) VALUES('Hüseyin Tosun', 'Admin', 1993)"""
            self.cursor.execute(stat1)
            stat1 = """ INSERT INTO USERS (UNAME, UTYPE, BIRTH) VALUES('Zeynep Yirmibeş', 'Moderator', 1993)"""
            self.cursor.execute(stat1)
            stat1 = """ INSERT INTO USERS (UNAME, UTYPE, BIRTH) VALUES('Alican Yılmaz', 'Guest', 1989)"""
            self.cursor.execute(stat1)
            stat1 = """ INSERT INTO USERS (UNAME, UTYPE, BIRTH) VALUES('Mehmet Koytak', 'Guest', 1995)"""
            self.cursor.execute(stat1)
            self.connection.commit()
        except dbapi2.DatabaseError:
            self.connection.rollback()

    def select_users(self):
        statement = """ SELECT * FROM USERS """
        self.cursor.execute(statement)
        return self.cursor

    def update_user(self, Id, uname, utype, birth):
        statement = """UPDATE USERS SET UNAME = '{}', UTYPE = '{}', BIRTH = {} WHERE ID = {}""".format( uname, utype, birth, Id)
        self.cursor.execute(statement)
        self.connection.commit()

    def find_Users(self, uname, utype, birth):
        condition=''
        if(uname.strip()):
            condition+=""" UNAME LIKE '%{}%' """.format(uname)
        if(utype.strip()):
            if(condition.strip()):
                condition+='AND'
            condition+=""" UTYPE LIKE '%{}%' """.format(utype)
        if(birth.strip()):
            if(condition.strip()):
                condition+='AND'
            condition+=""" BIRTH = {} """.format(birth)
        if(condition.strip()):
            condition=' WHERE '+ condition

        statement = """ SELECT * FROM USERS """+condition
        self.cursor.execute(statement)
        return self.cursor

    def delete_user(self,Id):
        stement =""" DELETE FROM USERS WHERE ID={}""".format(Id)
        self.cursor.execute(stement)
        self.connection.commit()

    def add_user(self, uname, utype, birth):
        if(uname.strip() and utype.strip() ):
            statement = """ INSERT INTO USERS (UNAME, UTYPE, BIRTH) VALUES('{}','{}',{})""".format(uname, utype, birth)
            self.cursor.execute(statement)
            self.connection.commit()

    def close_con(self):
        self.connection.close()





