import psycopg2 as dbapi2


class Nats:
    def __init__(self, dsn):
        self.connection = dbapi2.connect(dsn)
        self.cursor = self.connection.cursor()

    def create_table(self):
        try:
            stat1 = """ DROP TABLE NATS """
            self.cursor.execute(stat1)
            self.connection.commit()
        except dbapi2.DatabaseError:
            self.connection.rollback()
        try:
            stat1 = """ CREATE TABLE NATS (
                ID SERIAL PRIMARY KEY,
                NAT VARCHAR(40),
                FK_PlayersID INTEGER REFERENCES PLAYERS ON DELETE CASCADE ON UPDATE CASCADE
                ) """
            self.cursor.execute(stat1)
            stat1 = """ INSERT INTO NATS (NAT, FK_PlayersID) VALUES('Oflu', 1)"""
            self.cursor.execute(stat1)
            stat1 = """ INSERT INTO NATS (NAT, FK_PlayersID) VALUES('Turkish', 2)"""
            self.cursor.execute(stat1)
            stat1 = """ INSERT INTO NATS (NAT, FK_PlayersID) VALUES('Bulgarian', 3)"""
            self.cursor.execute(stat1)
            stat1 = """ INSERT INTO NATS (NAT, FK_PlayersID) VALUES('Spanish', 4)"""
            self.cursor.execute(stat1)
            self.connection.commit()
        except dbapi2.DatabaseError:
            self.connection.rollback()

    def select_nats(self):
        statement = """ SELECT * FROM NATS """
        self.cursor.execute(statement)
        return self.cursor

    def select_Joint_Nat(self):
        statement = """ SELECT NATS.ID, PLAYERS.Name,NAT FROM NATS INNER JOIN PLAYERS ON PLAYERS.ID=NATS.FK_PLAYERSID  """
        self.cursor.execute(statement)
        return self.cursor

    def delete_nat(self,Id):
        stement =""" DELETE FROM NATS WHERE ID={}""".format(Id)
        self.cursor.execute(stement)
        self.connection.commit()

    def add_nat(self, player, nat):
        if(nat.strip()):
            statement = """ INSERT INTO NATS (FK_PlayersID, NAT) VALUES('{}','{}')""".format(player, nat)
            self.cursor.execute(statement)
            self.connection.commit()

    def update_nat(self, Id, nat):
        statement = """UPDATE NATS SET NAT = '{}' WHERE ID = {}""".format( nat, Id)
        self.cursor.execute(statement)
        self.connection.commit()

    def find_Joint_Nat(self, player, nat):
        statement = """ SELECT NATS.ID, PLAYERS.Name, NAT FROM NATS INNER JOIN PLAYERS ON PLAYERS.ID=NATS.FK_PLAYERSID  """
        condition=''
        if(player.strip()):
            condition+=""" PLAYERS.Name LIKE '%{}%' """.format(player)
        if(nat.strip()):
            if(condition.strip()):
                condition+='AND'
            condition+=""" NAT LIKE '%{}%' """.format(nat)
        if(condition.strip()):
            condition=' WHERE '+condition
        self.cursor.execute(statement+condition)
        return self.cursor

    def close_con(self):
        self.connection.close()





