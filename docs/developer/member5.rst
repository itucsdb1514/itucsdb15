Parts Implemented by Gökay Şimşek
=================================

1 Sponsor Table
---------------

1.1 sponsors.py
+++++++++++++++

Sql Statements are executed with the functions of the sponsors class.


                +---------------+------------+
                |Name           |Type        |
                +===============+============+
                |id             |INTEGER     |
                +---------------+------------+
                |country        |varchar(40) |
                +---------------+------------+
                |FK_Teams       |varchar(40) |
                +---------------+------------+

__init__ function of sponsors class:

.. code-block:: python
   :linenos:

   def __init__(self, dsn):
        self.connection = dbapi2.connect(dsn)
        self.cursor = self.connection.cursor()

Constructor of the sponsors class.


create_table function of sponsors class:

.. code-block:: python
    :linenos:

    def create_table(self):
        try:
            stat1 = """ DROP TABLE Sponsors """
            self.cursor.execute(stat1)
            self.connection.commit()
        except dbapi2.DatabaseError:
            self.connection.rollback()
        try:
            stat1 = """ CREATE TABLE Sponsors (
                ID SERIAL PRIMARY KEY,
                NAME VARCHAR(40),
                COUNTRY VARCHAR(40),
                FK_Teams int REFERENCES Teams ON DELETE CASCADE ON UPDATE CASCADE
                ) """
            self.cursor.execute(stat1)
            stat1 = """ INSERT INTO Sponsors (NAME, COUNTRY, FK_Teams) VALUES('Ülker', 'Turkey', 1)"""
            self.cursor.execute(stat1)
            stat1 = """ INSERT INTO Sponsors (NAME, COUNTRY, FK_Teams) VALUES('Eti', 'Turkey', 2)"""
            self.cursor.execute(stat1)
            stat1 = """ INSERT INTO Sponsors (NAME, COUNTRY, FK_Teams) VALUES('Efes', 'Turkey', 3)"""
            self.cursor.execute(stat1)
            stat1 = """ INSERT INTO Sponsors (NAME, COUNTRY, FK_Teams) VALUES('Algida', 'Turkey', 3)"""
            self.cursor.execute(stat1)
            self.connection.commit()
        except dbapi2.DatabaseError:
            self.connection.rollback()


This code first drops sponsors table. Then it creates the sponsors table and inserts initial tuples to the table.



select_sponsor function of sponsor class:

.. code-block:: python
    :linenos:


   def select_sponsors(self):
        statement = """ SELECT Sponsors.ID,Sponsors.NAME,Sponsors.COUNTRY,TEAMS.NAME   FROM Sponsors INNER JOIN TEAMS ON TEAMS.ID=Sponsors.FK_Teams """
        self.cursor.execute(statement)
        return self.cursor

This code lists all the tuples in the sponsor table.


update_sponsor function of sponsors class:

.. code-block:: python
    :linenos:

    def update_sponsor(self, Id, name, country):
        statement = """UPDATE Sponsors SET NAME = '{}', COUNTRY = '{}'WHERE ID = {}""".format( name, country, Id)
        self.cursor.execute(statement)
        self.connection.commit()

This code updates the attributes of the sponsor table.

find_sponsor function of sponsor class:

.. code-block:: python
    :linenos:

    def Find_sponsors(self,name,country,team):
        condition=''
        if(name.strip()):
            condition+=""" Sponsors.NAME LIKE '%{}%' """.format(name)
        if(country.strip()):
            if(condition.strip()):
                condition+='AND'
            condition+=""" Sponsors.COUNTRY LIKE '%{}%' """.format(country)
        if(team.strip()):
            if(condition.strip()):
                condition+='AND'
            condition+=""" TEAMS.Name LIKE '%{}%' """.format(team)
        if(condition.strip()):
            condition=' WHERE '+ condition
        statement = """ SELECT Sponsors.ID,Sponsors.NAME,Sponsors.COUNTRY,TEAMS.NAME   FROM Sponsors INNER JOIN TEAMS ON TEAMS.ID=Sponsors.FK_Teams """
        statement=statement+condition
        self.cursor.execute(statement)
        return self.cursor


This code finds the tuples of sponsor table according to the searching criteria.

delete_sponsor function of sponsor class:

.. code-block:: python
    :linenos:

    def delete_sponsor(self,Id):
        stement =""" DELETE FROM Sponsors WHERE ID={}""".format(Id)
        self.cursor.execute(stement)
        self.connection.commit()

This code deletes the tuple which is selected.

add_sponsor function of sponsor class:

.. code-block:: python
    :linenos:

    def add_sponsor(self, name, country, age):
        if(name.strip() and country.strip() ):
            statement = """ INSERT INTO Sponsors (NAME, COUNTRY, FK_Teams) VALUES('{}','{}',{})""".format(name, country, age)
            self.cursor.execute(statement)
            self.connection.commit()

This code adds a tuple to sponsor table.

close_con function of sponsor class:

.. code-block:: python
    :linenos:

    def close_con(self):
        self.connection.close()

This code closes the connection.

1.2 sponsorlist.py
++++++++++++++++++

sponsorlist function:

.. code-block:: python
   :linenos:

   def sponsorsList(dsn):
    sponsorTable = sponsors.Sponsors(dsn)
    if request.method == 'GET':
        now = datetime.datetime.now()
        data=sponsorTable.select_sponsors()
        ts=teams.Teams(dsn)
        tDatas=ts.select_teams()
        return render_template('sponsors.html', current_time=now.ctime(),rows=data,
                               TeamSelect=tDatas,update=False)

This code calls the sponsors page.

.. code-block:: python
    :linenos:

    elif 'Delete' in request.form:
        keys = request.form.getlist('movies_to_delete')
        for key in keys:
            sponsorTable.delete_sponsor(key)
        sponsorTable.close_con()
        return redirect(url_for('sponsorsList'))

This code gets the key, calls the delete_sponsor function and deletes the selected tuple.

.. code-block:: python
    :linenos:

    elif 'Add' in request.form:
        name=request.form['Name']
        country=request.form['Country']
        team=request.form['Team']
        sponsorTable.add_sponsor(name,country,team)
        sponsorTable.close_con()
        return redirect(url_for('sponsorsList'))

This code gets the input values, calls the add_sponsor function and adds a tuple.

.. code-block:: python
    :linenos:

    elif 'Update' in request.form:
        keys = request.form.getlist('movies_to_delete')
        for key in keys:
           name=request.form['UName'+key]
           country=request.form['UCountry'+key]
           sponsorTable.update_sponsor(key, name, country)
        sponsorTable.close_con()
        return redirect(url_for('sponsorsList'))


This code gets the up-to-date values, calls the update_sponsor function and updates the tuple.

.. code-block:: python
    :linenos:

    elif'Find' in request.form:
        name=request.form['FName']
        country=request.form['FCountry']
        team=request.form['FTeam']
        ts=teams.Teams(dsn)
        now = datetime.datetime.now()
        tDatas=ts.select_teams()
        data=sponsorTable.Find_sponsors(name,country,team)
        return render_template('sponsors.html', current_time=now.ctime(),rows=data,TeamSelect=tDatas,update=False)

This code gets the searching criteria, calls the find_sponsor function and finds the requested tuple(s).


sponsorsListUpdate function:

.. code-block:: python
    :linenos:

    def sponsorsListUpdate(dsn):
    sponsorTable = sponsors.Sponsors(dsn)
    if request.method == 'GET':
        now = datetime.datetime.now()
        data=sponsorTable.select_sponsors()
        ts=teams.Teams(dsn)
        tDatas=ts.select_teams()
        return render_template('sponsors.html', current_time=now.ctime(),rows=data,
                               TeamSelect=tDatas,update=True)

This code gets the update page when the "click for update" button is pressed and makes the boolean "update" value True.


2 PlayerTeamHistory Table
-------------------------

2.1 playerHistory.py
++++++++++++++++++++

Sql Statements are executed with the functions of the playerHistory class.


                +---------------+------------+
                |Name           |Type        |
                +===============+============+
                |id             |INTEGER     |
                +---------------+------------+
                |FK_Player      |INTEGER     |
                +---------------+------------+
                |FK_Teams       |INTEGER     |
                +---------------+------------+
                |start          |DateTime    |
                +---------------+------------+
                |end            |DateTime    |
                +---------------+------------+


FK_Player is a foreign key and it references to the player table. FK_Teams is a foreign key and it references to the teams table

__init__ function of playerHistory class:

.. code-block:: python
    :linenos:

    def __init__(self, dsn):
        self.connection = dbapi2.connect(dsn)
        self.cursor = self.connection.cursor()

Constructor of the playerHistory class.

create_table function of playerHistory class:

.. code-block:: python
    :linenos:

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

This code first drops playerHistory table. Then it creates the playerHistory table and inserts initial tuples to the table.


delete_History function of Matches class:

.. code-block:: python
    :linenos:

    def delete_History(self,Id):
        stement =""" DELETE FROM playerHistory WHERE ID={}""".format(Id)
        self.cursor.execute(stement)
        self.connection.commit()

This code deletes the tuple which is selected.

add_History function of Matches class:

.. code-block:: python
    :linenos:

    def add_History(self, player, team,start,end):
        if(player.strip() and team.strip() and start.strip() and start.strip() ):
            statement = """ INSERT INTO playerHistory (FK_Player, FK_Teams, starts,ends) VALUES({},{},'{}', '{}')""".format(player, team, start, end)
            self.cursor.execute(statement)
            self.connection.commit()


This code adds a tuple to playerHistory table.


Update_History function of playerHistory class:

.. code-block:: python
    :linenos:

    def Update_History(self, Id, start, end):
        statement = """UPDATE playerHistory SET starts = '{}', ends = '{}'WHERE ID = {}""".format( start, end, Id)
        self.cursor.execute(statement)
        self.connection.commit()

This code updates the attributes of the playerHistory table except the foreign keys.


Select_PlayersHistory function of playerHistory class:

.. code-block:: python
    :linenos:

    def Select_PlayersHistory(self,id):
        query="""SELECT playerHistory.ID,PLAYERS.NAME,TEAMS.NAME,starts,ends FROM playerHistory
        INNER JOIN PLAYERS ON PLAYERS.ID=playerHistory.FK_Player
        INNER JOIN  Teams ON Teams.ID=FK_Teams WHERE FK_Player={}""".format(id)
        self.cursor.execute(query)
        return self.cursor

This code lists all the tuples in playerHistory table with the foreign keys.

Find_PlayersHistory function of playerHistory class:

.. code-block:: python
    :linenos:

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

This code finds the tuples of playerHistory table according to the searching criteria with foreign keys.

close_con function of playerHistory class:

.. code-block:: python
    :linenos:

    def close_con(self):
        self.connection.close()

This code closes the connection.

2.2 PHDetail.py
+++++++++++++++

PHDetail function:

.. code-block:: python
   :linenos:

    def PHDetail(dsn,id):
    playerH=playerHistory.playerHistory(dsn)
    if request.method == 'GET':
        now = datetime.datetime.now()
        datas= playerH.Select_PlayersHistory(id);
        ps=players.Players(dsn)
        ts=teams.Teams(dsn)
        tDatas=ts.select_teams()
        pDatas=ps.select_players()
        page= render_template('PHDetails.html', current_time=now.ctime(),
                              rows=datas, update = False,historyID=id,
                              PlayerSelect=pDatas,TeamSelect=tDatas,
                              )
        playerH.close_con();
        return page



.. code-block:: python
    :linenos:

    elif 'Delete' in request.form:
        keys = request.form.getlist('movies_to_delete')
        for key in keys:
            playerH.delete_History(key)
        playerH.close_con()
        return redirect(url_for('playerHistory',id=id))

This code gets the key, calls the delete_playerHistory function and deletes the selected tuple.

.. code-block:: python
    :linenos:

    elif 'Add' in request.form:
        playerID=request.form['Player']
        teamID=request.form['Team']
        start=request.form['start']
        end=request.form['end']
        try:
            playerH.add_History(playerID,teamID,start,end)
        except dbapi2.DatabaseError:
            pass
        playerH.close_con()
        return redirect(url_for('playerHistory',id=id))

This code gets the input values, calls the add_playerHistory function and adds a tuple.

.. code-block:: python
    :linenos:

    elif 'Update' in request.form:
        keys = request.form.getlist('movies_to_delete')
        for key in keys:
           start=request.form['UStart'+key]
           end=request.form['UEnd'+key]
           playerH.Update_History(key, start, end)
        playerH.close_con()
        return redirect(url_for('playerHistory',id=id))

This code gets the up-to-date values, calls the update_playerHistory function and updates the tuple.

.. code-block:: python
    :linenos:

    elif 'Find' in request.form:
        print("*************************************************")
        now = datetime.datetime.now()
        team=request.form['FTeam']
        start=request.form['FStart']
        end=request.form['FEnd']
        datas= playerH.Find_PlayersHistory(id,team,start,end);
        ps=players.Players(dsn)
        ts=teams.Teams(dsn)
        tDatas=ts.select_teams()
        pDatas=ps.select_players()
        page= render_template('PHDetails.html', current_time=now.ctime(),
                              rows=datas, update = False,historyID=id,
                              PlayerSelect=pDatas,TeamSelect=tDatas
                              )

This code gets the searching criteria, calls the Find_PlayersHistory function and finds the requested tuple(s). It also calls the select function of the stadiums class because of the foreign keys.

updateCoachesList:

.. code-block:: python
    :linenos:

    def PHDetailUpdate(dsn,id):
    playerH=playerHistory.playerHistory(dsn)
    if request.method == 'GET':
        now = datetime.datetime.now()
        datas= playerH.Select_PlayersHistory(id);
        ps=players.Players(dsn)
        ts=teams.Teams(dsn)
        tDatas=ts.select_teams()
        pDatas=ps.select_players()
        page= render_template('PHDetails.html', current_time=now.ctime(),
                              rows=datas, update = True ,historyID=id,
                              PlayerSelect=pDatas,TeamSelect=tDatas,
                              )
        playerH.close_con();
        return page

This code gets the update page when the "click for update" button is pressed and makes the boolean "update" value True.


3 OutFits
---------

3.1 outfitsTable.py
+++++++++++++++++++

Sql Statements are executed with the functions of the outfits class.


                +---------------+------------+
                |Name           |Type        |
                +===============+============+
                |id             |INTEGER     |
                +---------------+------------+
                |FK_TEAMID      |INTEGER     |
                +---------------+------------+
                |link           |NVARCHAR    |
                +---------------+------------+

FK_TEAMID id is a foreign key and it references to the Team table.

__init__ function of outfits class:

.. code-block:: python
    :linenos:

    def __init__(self, dsn):
        self.connection = dbapi2.connect(dsn)
        self.cursor = self.connection.cursor()


Constructor of the outfits class.

create_table function of outfits class:

.. code-block:: python
    :linenos:

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


This code first drops outfits table. Then it creates the outfits table and insert initial tuples to the table.


delete_betrate function of outfits class:

.. code-block:: python
    :linenos:

    def delete_outfits(self,Id):
        stement =""" DELETE FROM OUTFITS WHERE ID={}""".format(Id)
        self.cursor.execute(stement)
        self.connection.commit()

This code deletes the tuple which is selected.

add_outfits function of Betrate class:

.. code-block:: python
    :linenos:

    def add_outfits(self, teamID,link):
        if(teamID.strip() and link.strip() ):
            statement = """ INSERT INTO OUTFITS (FK_TEAMID,LINK) VALUES({},'{}')""".format(teamID,link)
            print (statement)
            self.cursor.execute(statement)
            self.connection.commit()

This code adds a tuple to OUTFITS table.


update_outfits function of OUTFITS class:

.. code-block:: python
    :linenos:

    def update_outfits(self, link,Id):
        statement = """UPDATE OUTFITS SET LINK='{}' WHERE ID = {}""".format(link, Id)
        self.cursor.execute(statement)
        self.connection.commit()

This code updates the attributes of the OUTFITS table except the foreign keys.


select_outfits function of OUTFITS class:

.. code-block:: python
    :linenos:

    def select_outfits(self,id):
        statement = """ SELECT OUTFITS.ID,TEAMS.NAME,LINK FROM OUTFITS INNER JOIN TEAMS ON OUTFITS.FK_TEAMID=TEAMS.ID where FK_TEAMID={} """.format(id)
        self.cursor.execute(statement)
        return self.cursor

This code lists all the tuples in OUTFITS table with the foreign key.

find_outfits function of OUTFITS class:

.. code-block:: python
    :linenos:

    def find_outfits(self, name,id):
        condition=''
        if(name.strip()):
            condition+=""" TEAMS.NAME LIKE '%{}%' """.format(name)

        if(condition.strip()):
            condition=' WHERE '+ condition

        statement = """ SELECT OUTFITS.ID,TEAMS.NAME,LINK FROM OUTFITS INNER JOIN TEAMS ON OUTFITS.FK_TEAMID=TEAMS.ID """+condition
        self.cursor.execute(statement)
        return self.cursor


This code finds the tuples of OUTFITS table according to the searching criteria with the foreign key.

close_con function of OUTFITS class:

.. code-block:: python
    :linenos:

    def close_con(self):
        self.connection.close()

This code closes the connection.

3.2 outfitPage.py
+++++++++++++++++

outfitPage function:

.. code-block:: python
    :linenos:

    def outfitPage(dsn,id):
    outfits=outfitTable.outfits(dsn)
    if request.method == 'GET':
        now = datetime.datetime.now()
        datas= outfits.select_outfits(id);
        ts=teams.Teams(dsn)
        tDatas=ts.select_teams()
        page= render_template('outfit.html', current_time=now.ctime(),
                              rows=datas, update = False,TeamID=id,
                              teamSelect=tDatas,
                              )
        outfits.close_con();
        return page

This code calls the outfitPage page.

.. code-block:: python
    :linenos:

    elif 'Delete' in request.form:
        keys = request.form.getlist('movies_to_delete')
        for key in keys:
            outfits.delete_outfits(key)
        outfits.close_con()
        return redirect(url_for('outfitpage',id=id))

This code gets the key, calls the delete_outfit function and deletes the selected tuple.

.. code-block:: python
    :linenos:

    elif 'Add' in request.form:
        teamID=request.form['Team']
        link=request.form['Link']

        outfits.add_outfits(teamID,link)

        outfits.close_con()
        return redirect(url_for('outfitpage',id=id))

This code gets the input values, calls the add_outfit function and adds a tuple.

.. code-block:: python
    :linenos:

    elif 'Update' in request.form:
        keys = request.form.getlist('movies_to_delete')
        for key in keys:
           link=request.form['ULink'+key]
           outfits.update_outfits(link,key)
        outfits.close_con()
        return redirect(url_for('outfitpage',id=id))

This code gets the up-to-date values, calls the update_outfit function and updates the tuple.


updateCoachesList:

.. code-block:: python
    :linenos:

    def outfitPageUpdate(dsn,id):
    outfits=outfitTable.outfits(dsn)
    if request.method == 'GET':
        now = datetime.datetime.now()
        datas= outfits.select_outfits(id);
        ts=teams.Teams(dsn)
        tDatas=ts.select_teams()
        page= render_template('outfit.html', current_time=now.ctime(),
                              rows=datas, update = True,TeamID=id,
                              teamSelect=tDatas,
                              )
        outfits.close_con();
        return page

This code gets the update page when the "click for update" button is pressed and makes the boolean "update" value True.









