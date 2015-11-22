import psycopg2 as dbapi2
from asyncio.locks import Condition


class Comments:
    def __init__(self, dsn):
        self.connection = dbapi2.connect(dsn)
        self.cursor = self.connection.cursor()

    def create_table(self):
        try:
            stat1 = """ DROP TABLE Comments """
            self.cursor.execute(stat1)
            self.connection.commit()
        except dbapi2.DatabaseError:
            self.connection.rollback()
        try:
            stat1 = """ CREATE TABLE Comments (
                ID SERIAL PRIMARY KEY,
                NOTES VARCHAR(40),
                PointCount INTEGER,
                FK_PlayersID INTEGER REFERENCES PLAYERS
                ) """
            self.cursor.execute(stat1)
            stat1 = """ INSERT INTO Comments ( NOTES, PointCount,FK_PlayersID) VALUES( 'Well-played', 9,1)"""
            self.cursor.execute(stat1)
            stat1 = """ INSERT INTO Comments ( NOTES, PointCount,FK_PlayersID) VALUES( 'Nice', 9,2)"""
            self.cursor.execute(stat1)
            stat1 = """ INSERT INTO Comments ( NOTES, PointCount,FK_PlayersID) VALUES( 'Ordinary', 7,3)"""
            self.cursor.execute(stat1)
            stat1 = """ INSERT INTO Comments ( NOTES, PointCount,FK_PlayersID) VALUES('Well-played', 9,4)"""
            self.cursor.execute(stat1)
            self.connection.commit()
        except dbapi2.DatabaseError:
            self.connection.rollback()

    def select_comments(self):
        statement = """ SELECT * FROM Comments """
        self.cursor.execute(statement)
        return self.cursor
    def find_Comments(self,player,notes,pointCount):
        condition=''
        if(notes.strip()):
            if(condition.strip()):
                condition+='AND'
            condition+=""" NOTES='{}' """.format(notes)
        if(pointCount.strip()):
            if(condition.strip()):
                condition+='AND'
            condition+=""" PointCount={} """.format(pointCount)
        if(condition.strip()):
            condition=' WHERE '+condition

        statement = """ SELECT * FROM Comments """+condition
        self.cursor.execute(statement)
        return self.cursor

    def delete_comment(self,Id):
        stement =""" DELETE FROM Comments WHERE ID={}""".format(Id)
        self.cursor.execute(stement)
        self.connection.commit()

    def add_comment(self, player, notes, point):
        print(player)
        print(notes)
        print()
        if(player.strip() and notes.strip() ):
            statement = """ INSERT INTO Comments (FK_PlayersID, NOTES, PointCount) VALUES('{}','{}',{})""".format(player, notes, point)
            self.cursor.execute(statement)
            self.connection.commit()
    def update_comment(self, Id,notes, point):
        statement = """UPDATE Comments SET  NOTES = '{}', PointCount = {} WHERE ID = {}""".format( notes, point, Id)
        self.cursor.execute(statement)
        self.connection.commit()
    def select_Joint_Comment(self):
        statement = """ SELECT Comments.ID,PLAYERS.Name,NOTES,PointCount FROM Comments INNER JOIN PLAYERS ON PLAYERS.ID=COMMENTS.FK_PLAYERSID  """
        self.cursor.execute(statement)
        return self.cursor

    def find_Joint_Comment(self, player, notes, pointCount):
        statement = """ SELECT Comments.ID,PLAYERS.Name,NOTES,PointCount FROM Comments INNER JOIN PLAYERS ON PLAYERS.ID=COMMENTS.FK_PLAYERSID  """
        condition=''
        if(player.strip()):
            condition+=""" PLAYERS.Name='{}' """.format(player)
        if(notes.strip()):
            if(condition.strip()):
                condition+='AND'
            condition+=""" NOTES='{}' """.format(notes)
        if(pointCount.strip()):
            if(condition.strip()):
                condition+='AND'
            condition+=""" PointCount={} """.format(pointCount)
        if(condition.strip()):
            condition=' WHERE '+condition
        self.cursor.execute(statement+condition)
        return self.cursor
    def close_con(self):
        self.connection.close()





