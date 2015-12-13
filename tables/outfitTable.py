import psycopg2 as dbapi2


class outfits:
    def __init__(self, dsn):
        self.connection = dbapi2.connect(dsn)
        self.cursor = self.connection.cursor()

    def create_table(self):
        try:
            stat1 = """ DROP TABLE OUTFITS """
            self.cursor.execute(stat1)
            self.connection.commit()
        except dbapi2.DatabaseError:
            self.connection.rollback()
        try:
            stat1 = """ CREATE TABLE OUTFITS (
                ID SERIAL PRIMARY KEY,
                FK_TEAMID INT REFERENCES Teams ON DELETE CASCADE ON UPDATE CASCADE,
                link VARCHAR(255)
                ) """
            self.cursor.execute(stat1)
            stat1 = """ INSERT INTO OUTFITS (FK_TEAMID,link) VALUES(1,'http://usatftw.files.wordpress.com/2013/07/580466_10151828406877573_187877171_n.jpg')"""
            self.cursor.execute(stat1)
            stat1 = """ INSERT INTO OUTFITS (FK_TEAMID,link) VALUES(3,'http://usatftw.files.wordpress.com/2013/07/580466_10151828406877573_187877171_n.jpg')"""
            self.cursor.execute(stat1)
            stat1 = """ INSERT INTO OUTFITS (FK_TEAMID,link) VALUES(2,'http://usatftw.files.wordpress.com/2013/07/580466_10151828406877573_187877171_n.jpg')"""
            self.cursor.execute(stat1)
            self.connection.commit()
        except dbapi2.DatabaseError:
            self.connection.rollback()

    def select_outfits(self,id):
        statement = """ SELECT OUTFITS.ID,TEAMS.NAME,LINK FROM OUTFITS INNER JOIN TEAMS ON OUTFITS.FK_TEAMID=TEAMS.ID where FK_TEAMID={} """.format(id)
        self.cursor.execute(statement)
        return self.cursor

    def update_outfits(self, link,Id):
        statement = """UPDATE OUTFITS SET LINK='{}' WHERE ID = {}""".format(link, Id)
        self.cursor.execute(statement)
        self.connection.commit()

    def find_outfits(self, name,id):
        condition=''
        if(name.strip()):
            condition+=""" TEAMS.NAME LIKE '%{}%' """.format(name)

        if(condition.strip()):
            condition=' WHERE '+ condition

        statement = """ SELECT OUTFITS.ID,TEAMS.NAME,LINK FROM OUTFITS INNER JOIN TEAMS ON OUTFITS.FK_TEAMID=TEAMS.ID """+condition
        self.cursor.execute(statement)
        return self.cursor

    def delete_outfits(self,Id):
        stement =""" DELETE FROM OUTFITS WHERE ID={}""".format(Id)
        self.cursor.execute(stement)
        self.connection.commit()

    def add_outfits(self, teamID,link):
        if(teamID.strip() and link.strip() ):
            statement = """ INSERT INTO OUTFITS (FK_TEAMID,LINK) VALUES({},'{}')""".format(teamID,link)
            print (statement)
            self.cursor.execute(statement)
            self.connection.commit()

    def close_con(self):
        self.connection.close()





