import psycopg2 as dbapi2


class Stats:
    def __init__(self, dsn):
        self.connection = dbapi2.connect(dsn)
        self.cursor = self.connection.cursor()

    def create_table(self):
        try:
            stat1 = """ DROP TABLE STATS """
            self.cursor.execute(stat1)
            self.connection.commit()
        except dbapi2.DatabaseError:
            self.connection.rollback()
        try:
            stat1 = """ CREATE TABLE STATS (
                ID SERIAL PRIMARY KEY,
                PLAYER VARCHAR(40),
                NUMOFGAMES INTEGER,
                FK_TeamsID INTEGER REFERENCES TEAMS ON DELETE CASCADE ON UPDATE CASCADE
                ) """
            self.cursor.execute(stat1)
            stat1 = """ INSERT INTO STATS (PLAYER, NUMOFGAMES, FK_TeamsID) VALUES('Miguel Cabrera', 119, 1)"""
            self.cursor.execute(stat1)
            stat1 = """ INSERT INTO STATS (PLAYER, NUMOFGAMES, FK_TeamsID) VALUES('Dee Gordon', 145, 1)"""
            self.cursor.execute(stat1)
            stat1 = """ INSERT INTO STATS (PLAYER, NUMOFGAMES, FK_TeamsID) VALUES('Bryce Harper', 153, 2)"""
            self.cursor.execute(stat1)
            stat1 = """ INSERT INTO STATS (PLAYER, NUMOFGAMES, FK_TeamsID) VALUES('DJ LeMahieu', 128, 3)"""
            self.cursor.execute(stat1)
            self.connection.commit()
        except dbapi2.DatabaseError:
            self.connection.rollback()

    def select_stats(self):
        statement = """ SELECT * FROM STATS """
        self.cursor.execute(statement)
        return self.cursor

    def select_Joint_Stat(self):
        statement = """ SELECT STATS.ID, TEAMS.Name,PLAYER, NUMOFGAMES FROM STATS INNER JOIN TEAMS ON TEAMS.ID=STATS.FK_TEAMSID  """
        self.cursor.execute(statement)
        return self.cursor

    def delete_stat(self,Id):
        stement =""" DELETE FROM STATS WHERE ID={}""".format(Id)
        self.cursor.execute(stement)
        self.connection.commit()

    def add_stat(self, team, stat, player):
        if(stat.strip()):
            statement = """ INSERT INTO STATS (FK_TeamsID, NUMOFGAMES, PLAYER) VALUES('{}','{}','{}')""".format(team, stat, player)
            self.cursor.execute(statement)
            self.connection.commit()

    def update_stat(self, Id, stat):
        statement = """UPDATE STATS SET NUMOFGAMES = {} WHERE ID = {}""".format( stat, Id)
        self.cursor.execute(statement)
        self.connection.commit()

    def find_Joint_Stat(self, team, stat, player):
        statement = """ SELECT STATS.ID, TEAMS.Name, PLAYER , NUMOFGAMES FROM STATS INNER JOIN TEAMS ON TEAMS.ID=STATS.FK_TeamsID  """
        condition=''
        if(team.strip()):
            condition+=""" TEAMS.Name LIKE '%{}%' """.format(team)
        if(stat.strip()):
            if(condition.strip()):
                condition+='AND'
            condition+=""" NUMOFGAMES = {} """.format(stat)
        if(player.strip()):
            if(condition.strip()):
                condition+='AND'
            condition+=""" PLAYER LIKE '%{}%' """.format(player)
        if(condition.strip()):
            condition=' WHERE '+condition
        self.cursor.execute(statement+condition)
        return self.cursor

    def close_con(self):
        self.connection.close()





