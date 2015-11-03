import psycopg2 as dbapi2


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
                PLAYER VARCHAR(40),
                NOTES VARCHAR(40),
                PointCount INTEGER
                ) """
            self.cursor.execute(stat1)
            stat1 = """ INSERT INTO Comments (PLAYER, NOTES, PointCount) VALUES('Ahmet', 'Well-played', 9)"""
            self.cursor.execute(stat1)
            stat1 = """ INSERT INTO Comments (PLAYER, NOTES, PointCount) VALUES('Mehmet', 'Nice', 9)"""
            self.cursor.execute(stat1)
            stat1 = """ INSERT INTO Comments (PLAYER, NOTES, PointCount) VALUES('Zeynep', 'Ordinary', 7)"""
            self.cursor.execute(stat1)
            stat1 = """ INSERT INTO Comments (PLAYER, NOTES, PointCount) VALUES('Ali', 'Well-played', 9)"""
            self.cursor.execute(stat1)
            self.connection.commit()
        except dbapi2.DatabaseError:
            self.connection.rollback()

    def select_comments(self):
        statement = """ SELECT * FROM Comments """
        self.cursor.execute(statement)
        return self.cursor

    def delete_comment(self,Id):
        stement =""" DELETE FROM Comments WHERE ID={}""".format(Id)
        self.cursor.execute(stement)
        self.connection.commit()

    def add_comment(self, player, notes, point):
        if(player.strip() and notes.strip() ):
            statement = """ INSERT INTO Comments (PLAYER, NOTES, PointCount) VALUES('{}','{}',{})""".format(player, notes, point)
            self.cursor.execute(statement)
            self.connection.commit()

    def close_con(self):
        self.connection.close()





