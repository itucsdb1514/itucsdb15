import psycopg2 as dbapi2

class playerHistory:
    def __init__(self, dsn):
        self.connection = dbapi2.connect(dsn)
        self.cursor = self.connection.cursor()

    def create_table(self):
        try:
            stat1 = """ DROP TABLE playerHistory """
            self.cursor.execute(stat1)
            self.connection.commit()
        except dbapi2.DatabaseError:
            self.connection.rollback()
        try:
            stat1 = """ CREATE TABLE playerHistory (
                ID SERIAL PRIMARY KEY,
                FK_Player int REFERENCES PLAYERS ON DELETE CASCADE ON UPDATE CASCADE,
                FK_Teams int REFERENCES Teams ON DELETE CASCADE ON UPDATE CASCADE,
                starts date,
                ends date
                ) """
            self.cursor.execute(stat1)
            stat1 = """ INSERT INTO playerHistory (FK_Player, FK_Teams, starts,ends) VALUES(1, 2, '1994-11-28','1994-11-28')"""
            self.cursor.execute(stat1)
            stat1 = """ INSERT INTO playerHistory (FK_Player, FK_Teams, starts,ends) VALUES(2, 3, '1994-11-28','1994-11-28')"""
            self.cursor.execute(stat1)
            stat1 = """ INSERT INTO playerHistory (FK_Player, FK_Teams, starts,ends) VALUES(3, 1, '1994-11-28','1994-11-28')"""
            self.cursor.execute(stat1)
            stat1 = """ INSERT INTO playerHistory (FK_Player, FK_Teams, starts,ends) VALUES(4, 2, '1994-11-28','1994-11-28')"""
            self.cursor.execute(stat1)
            self.connection.commit()
        except dbapi2.DatabaseError:
            self.connection.rollback()
    def Select_PlayersHistory(self,id):
        query="""SELECT playerHistory.ID,PLAYERS.NAME,TEAMS.NAME,starts,ends FROM playerHistory
        INNER JOIN PLAYERS ON PLAYERS.ID=playerHistory.FK_Player
        INNER JOIN  Teams ON Teams.ID=FK_Teams WHERE FK_Player={}""".format(id)
        self.cursor.execute(query)
        return self.cursor
    def Find_PlayersHistory(self,id,Team,Start,End):
        condition=''
        if(Team.strip()):
            condition+=""" Teams.Name LIKE '%{}%' """.format(Team)
        if(Start.strip()):
            if(condition.strip()):
                condition+='AND'
            condition+=""" playerHistory.starts = '{}' """.format(Start)
        if(End.strip()):
            if(condition.strip()):
                condition+='AND'
            condition+=""" playerHistory.ends = '{}' """.format(End)
        if(condition.strip()):
            condition=' AND '+ condition
        query="""SELECT playerHistory.ID,PLAYERS.NAME,TEAMS.NAME,starts,ends FROM playerHistory
        INNER JOIN PLAYERS ON PLAYERS.ID=playerHistory.FK_Player
        INNER JOIN  Teams ON Teams.ID=FK_Teams WHERE FK_Player={} """.format(id)
        query=query+condition
        self.cursor.execute(query)
        return self.cursor
    def close_con(self):
        self.connection.close()

    def add_History(self, player, team,start,end):
        if(player.strip() and team.strip() and start.strip() and start.strip() ):
            statement = """ INSERT INTO playerHistory (FK_Player, FK_Teams, starts,ends) VALUES({},{},'{}', '{}')""".format(player, team, start, end)
            self.cursor.execute(statement)
            self.connection.commit()

    def delete_History(self,Id):
        stement =""" DELETE FROM playerHistory WHERE ID={}""".format(Id)
        self.cursor.execute(stement)
        self.connection.commit()