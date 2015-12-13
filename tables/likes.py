import psycopg2 as dbapi2
from asyncio.locks import Condition

class Likes:
    def __init__(self, dsn):
        self.connection = dbapi2.connect(dsn)
        self.cursor = self.connection.cursor()

    def create_table(self):
        try:
            stat1 = """ DROP TABLE Likes """
            self.cursor.execute(stat1)
            self.connection.commit()
        except dbapi2.DatabaseError:
            self.connection.rollback()
        try:

            stat1 = """ CREATE TABLE Likes (
                ID SERIAL PRIMARY KEY,
                STATUS VARCHAR(40),
                FK_UsersID INTEGER REFERENCES Users ON DELETE CASCADE ON UPDATE CASCADE,
                FK_PlayersID INTEGER REFERENCES Players ON DELETE CASCADE ON UPDATE CASCADE
                ) """
            self.cursor.execute(stat1)
            stat1 = """ INSERT INTO Likes (STATUS, FK_UsersID, FK_PlayersID) VALUES('Like',1,1)"""
            self.cursor.execute(stat1)
            stat1 = """ INSERT INTO Likes (STATUS, FK_UsersID, FK_PlayersID) VALUES('Like',2,2)"""
            self.cursor.execute(stat1)
            stat1 = """ INSERT INTO Likes (STATUS, FK_UsersID, FK_PlayersID) VALUES('Dislike',3,3)"""
            self.cursor.execute(stat1)
            self.connection.commit()

        except dbapi2.DatabaseError:
            self.connection.rollback()

    def select_likes(self):
        statement = """ SELECT * FROM Likes """
        self.cursor.execute(statement)
        return self.cursor

    def find_Likes(self,user,player,status):
        condition=''
        if(status.strip()):
            condition+=""" STATUS LIKE '%{}%' """.format(status)
        if(condition.strip()):
            condition=' WHERE '+condition

        statement = """ SELECT * FROM Likes """+condition
        self.cursor.execute(statement)
        return self.cursor

    def delete_like(self,Id):
        stement =""" DELETE FROM Likes WHERE ID={}""".format(Id)
        self.cursor.execute(stement)
        self.connection.commit()

    def add_like(self, user, player, status):
        if(status.strip()):
            statement = """ INSERT INTO Likes (FK_UsersID,FK_PlayersID, STATUS) VALUES({},{},'{}')""".format(user, player, status)
            self.cursor.execute(statement)
            self.connection.commit()

    def update_like(self, Id, status):
        statement = """UPDATE Likes SET STATUS = '{}' WHERE ID = {}""".format( status, Id)
        self.cursor.execute(statement)
        self.connection.commit()


    def select_Joint_Like(self):
        statement = """ SELECT Likes.ID,Users.Uname,Players.Name, Likes.STATUS FROM Likes INNER JOIN Users ON Users.ID=Likes.FK_UsersID INNER JOIN Players ON Players.ID=Likes.FK_PlayersID  """
        self.cursor.execute(statement)
        return self.cursor

    def find_Joint_Like(self,user,player,status):
        statement = """ SELECT Likes.ID,Users.Uname,Players.Name, Likes.STATUS FROM Likes INNER JOIN Users ON Users.ID=Likes.FK_UsersID INNER JOIN Players ON Players.ID=Likes.FK_PlayersID """
        condition=''
        if(user.strip()):
            condition+=""" Users.Uname LIKE '%{}%'""".format(user)
        if(player.strip()):
            condition+=""" Players.Name LIKE '%{}%'""".format(player)
        if(status.strip()):
            if(condition.strip()):
                condition+='AND'
            condition+=""" Likes.STATUS LIKE '%{}%' """.format(status)
        if(condition.strip()):
            condition=' WHERE '+condition
        self.cursor.execute(statement+condition)
        return self.cursor

    def close_con(self):
        self.connection.close()