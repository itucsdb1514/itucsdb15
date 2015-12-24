Parts Implemented by Zeynep Yirmibeşoğlu
========================================


1 Database Design
=================


1.1 Players Table
-----------------


                +---------------+------------+
                |Name           |Type        |
                +===============+============+
                |id             |INTEGER     |
                +---------------+------------+
                |name           |varchar(40) |
                +---------------+------------+
                |country        |varchar(40) |
                +---------------+------------+
                |age            |INTEGER     |
                +---------------+------------+




1.2 Nationalities Table
-----------------------


                +---------------+------------+
                |Name           |Type        |
                +===============+============+
                |id             |INTEGER     |
                +---------------+------------+
                |nat            |varchar(40) |
                +---------------+------------+
                |player id      |INTEGER     |
                +---------------+------------+

Player id is a foreign key and it references to the Players table. From players table, names of the players
are extracted, and used in the Nationalities table.


1.3 Statistics Table
--------------------

                +---------------+------------+
                |Name           |Type        |
                +===============+============+
                |id             |INTEGER     |
                +---------------+------------+
                |player         |varchar(40) |
                +---------------+------------+
                |num of games   |INTEGER     |
                +---------------+------------+
                |team id        |INTEGER     |
                +---------------+------------+

Team id is a foreign key and it references to the Teams table. Team name is used in the Statistics table.

2 Code
======

2.1 Players Table
-----------------
Sql Statements are executed with the functions of the Players class.

2.1.1 players.py
++++++++++++++++


**__init__ function of Players class:**

.. code-block:: python
    :linenos:

    def __init__(self, dsn):
        self.connection = dbapi2.connect(dsn)
        self.cursor = self.connection.cursor()

Constructor of the Players object.


**create_table function of Players class:**

.. code-block:: python
    :linenos:

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
            stat1 = """ INSERT INTO PLAYERS (NAME, COUNTRY, AGE) VALUES('Miguel Cabrera', 'USA', 32)"""
            self.cursor.execute(stat1)
            stat1 = """ INSERT INTO PLAYERS (NAME, COUNTRY, AGE) VALUES('Dee Gordon', 'USA', 27)"""
            self.cursor.execute(stat1)
            stat1 = """ INSERT INTO PLAYERS (NAME, COUNTRY, AGE) VALUES('Bryce Harper', 'USA', 23)"""
            self.cursor.execute(stat1)
            stat1 = """ INSERT INTO PLAYERS (NAME, COUNTRY, AGE) VALUES('DJ LeMahieu', 'USA', 27)"""
            self.cursor.execute(stat1)
            self.connection.commit()
        except dbapi2.DatabaseError:
            self.connection.rollback()


This code first drops the Players table, in case it already exists.
Then it creates the Players table and insert initial tuples to the table.


**select_players function of Players class:**

.. code-block:: python
    :linenos:

    def select_players(self):
        statement = """ SELECT * FROM PLAYERS """
        self.cursor.execute(statement)
        return self.cursor

This code selects and lists all the tuples in the Players table.


**update_player function of Players class:**

.. code-block:: python
    :linenos:

    def update_player(self, Id, name, country, age):
        statement = """UPDATE PLAYERS SET NAME = '{}', COUNTRY = '{}', AGE = {} WHERE ID = {}""".format( name, country, age, Id)
        self.cursor.execute(statement)
        self.connection.commit()

This code updates the attributes of the Players table according to the input the user enters to the site.


**find_players function of Players class:**

.. code-block:: python
    :linenos:

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

This code finds the tuples of Players table according to the searching criteria.

**delete_player function of Players class:**

.. code-block:: python
    :linenos:

    def delete_player(self,Id):
        stement =""" DELETE FROM PLAYERS WHERE ID={}""".format(Id)
        self.cursor.execute(stement)
        self.connection.commit()

This code deletes the tuple that is selected.

**add_player function of Players class:**

.. code-block:: python
    :linenos:

    def add_player(self, name, country, age):
        if(name.strip() and country.strip() ):
            statement = """ INSERT INTO PLAYERS (NAME, COUNTRY, AGE) VALUES('{}','{}',{})""".format(name, country, age)
            self.cursor.execute(statement)
            self.connection.commit()

 This code adds a tuple to Players table, according to the input from the user.

 **close_con function of Players class:**

.. code-block:: python
    :linenos:

    def close_con(self):
        self.connection.close()

This code closes the connection.


2.1.2 playerslist.py
++++++++++++++++++++

**playersList function:**

.. code-block:: python
    :linenos:

    def playersList(dsn):
    playerTable = players.Players(dsn)
    if request.method == 'GET':
        now = datetime.datetime.now()
        data=playerTable.select_players()
        return render_template('players.html', current_time=now.ctime(),rows=data, update=False)

This function calls the players page through players.html.

.. code-block:: python
    :linenos:

    elif 'Delete' in request.form:
        keys = request.form.getlist('movies_to_delete')
        for key in keys:
            playerTable.delete_player(key)
        playerTable.close_con()
        return redirect(url_for('playersList'))

This code gets the key, calls the delete_player function and deletes the selected tuple.

.. code-block:: python
    :linenos:

    elif 'Add' in request.form:
        name=request.form['Name']
        country=request.form['Country']
        age=request.form['Age']
        playerTable.add_player(name,country,age)
        playerTable.close_con()
        return redirect(url_for('playersList'))

This code gets the input values, calls the add_player function and adds a tuple.

.. code-block:: python
    :linenos:

    elif 'Update2' in request.form:
        keys = request.form.getlist('movies_to_delete')
        for key in keys:
           name=request.form['Name'+key]
           country=request.form['Country'+key]
           age=request.form['Age'+key]
           playerTable.update_player(key, name, country, age)
        playerTable.close_con()
        return redirect(url_for('playersListUpdate'))

This code gets the up-to-date values, calls the update_player function and updates the tuple.

.. code-block:: python
    :linenos:

    elif 'Find' in request.form:
        now = datetime.datetime.now()
        name=request.form['NameF']
        country=request.form['CountryF']
        age=request.form['AgeF']
        data=playerTable.find_Players(name, country, age)
        temp=render_template('players.html',  current_time=now.ctime(),rows=data, update=False)
        playerTable.close_con()
        return temp

This code gets the searching criteria, calls the find_Players function and finds the requested tuple(s).


**updatePlayersList function:**

.. code-block:: python
    :linenos:

     def updatePlayersList(dsn):
         playerTable = players.Players(dsn)
         if request.method == 'GET':
            now = datetime.datetime.now()
            data=playerTable.select_players()
            temp=render_template('players.html', current_time=now.ctime(),rows=data, update=True)
            playerTable.close_con()
            return temp

This code gets the update page when the "click for update" button is pressed and makes the boolean "update" value True.


2.2 Nationalities Table
-----------------------
Sql Statements are executed with the functions of the Nats class.

2.2.1 nats.py
+++++++++++++


**__init__ function of Nats class:**

.. code-block:: python
    :linenos:

    def __init__(self, dsn):
        self.connection = dbapi2.connect(dsn)
        self.cursor = self.connection.cursor()

Constructor of the Nats class.

**create_table function of Nats class:**

.. code-block:: python
    :linenos:

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
            stat1 = """ INSERT INTO NATS (NAT, FK_PlayersID) VALUES('Venezuelan', 1)"""
            self.cursor.execute(stat1)
            stat1 = """ INSERT INTO NATS (NAT, FK_PlayersID) VALUES('American', 2)"""
            self.cursor.execute(stat1)
            stat1 = """ INSERT INTO NATS (NAT, FK_PlayersID) VALUES('American', 3)"""
            self.cursor.execute(stat1)
            stat1 = """ INSERT INTO NATS (NAT, FK_PlayersID) VALUES('American', 4)"""
            self.cursor.execute(stat1)
            self.connection.commit()
        except dbapi2.DatabaseError:
            self.connection.rollback()


This code first drops the Nats table, in case it already exists.
Then it creates the Nats table and insert initial tuples to the table.


**select_nats function of Nats class:**

.. code-block:: python
    :linenos:

    def select_nats(self):
        statement = """ SELECT * FROM NATS """
        self.cursor.execute(statement)
        return self.cursor

This code lists all the tuples in the Nats table.

**delete_nat function of Nats class:**

.. code-block:: python
    :linenos:

    def delete_nat(self,Id):
        stement =""" DELETE FROM NATS WHERE ID={}""".format(Id)
        self.cursor.execute(stement)
        self.connection.commit()


This code deletes the tuple which is selected.

**add_nat function of Nats class:**

.. code-block:: python
    :linenos:

    def add_nat(self, player, nat):
        if(nat.strip()):
            statement = """ INSERT INTO NATS (FK_PlayersID, NAT) VALUES('{}','{}')""".format(player, nat)
            self.cursor.execute(statement)
            self.connection.commit()

This code adds a tuple to Nats table.


**update_nat function of Nats class:**

.. code-block:: python
    :linenos:

    def update_nat(self, Id, nat):
        statement = """UPDATE NATS SET NAT = '{}' WHERE ID = {}""".format( nat, Id)
        self.cursor.execute(statement)
        self.connection.commit()


This code updates the attributes of the Nats table except for the foreign keys.


**select_Joint_Nat function of Nats class:**

.. code-block:: python
    :linenos:

    def select_Joint_Nat(self):
        statement = """ SELECT NATS.ID, PLAYERS.Name,NAT FROM NATS INNER JOIN PLAYERS ON PLAYERS.ID=NATS.FK_PLAYERSID  """
        self.cursor.execute(statement)
        return self.cursor

This code lists all the tuples in Nats table with the foreign keys.

**find_Joint_Nat function of Nats class:**

.. code-block:: python
    :linenos:

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

This code finds the tuples of Nats table according to the searching criteria with foreign keys.

**close_con function of Nats class:**

.. code-block:: python
    :linenos:

    def close_con(self):
        self.connection.close()

This code closes the connection.


2.2.2 natslist.py
+++++++++++++++++

**natsList function:**

.. code-block:: python
    :linenos:

    def natsList(dsn):
    natTable = nats.Nats(dsn)
    if request.method == 'GET':
        now = datetime.datetime.now()
        playersTable=players.Players(dsn)
        data2 =playersTable.select_players()
        data=natTable.select_Joint_Nat()
        return render_template('nats.html', current_time=now.ctime(),rows=data, update=False,PlayersSelect=data2)

This code calls the nats page. This page contains information from nats page and players page. So it calls the "select" functions of players class and nats class and collects the information. Then it calls the select_Joint_Nat function and executes the listing.

.. code-block:: python
    :linenos:

    elif 'Delete' in request.form:
        keys = request.form.getlist('movies_to_delete')
        for key in keys:
            natTable.delete_nat(key)
        natTable.close_con()
        return redirect(url_for('natsList'))

This code gets the key, calls the delete_nat function and deletes the selected tuple.

.. code-block:: python
    :linenos:

    elif 'Add' in request.form:
        player=request.form['SelectPlayerName']
        nat=request.form['Nat']
        natTable.add_nat(player, nat)
        natTable.close_con()
        return redirect(url_for('natsList'))

This code gets the input values, calls the add_nat function and adds a tuple.

.. code-block:: python
    :linenos:

    elif 'Update2' in request.form:
        keys = request.form.getlist('movies_to_delete')
        for key in keys:
           nat=request.form['Nat'+key]
           natTable.update_nat(key,nat)
        natTable.close_con()
        return redirect(url_for('natsListUpdate'))

This code gets the up-to-date values, calls the update_nat function and updates the tuple.

.. code-block:: python
    :linenos:

    elif 'Find' in request.form:
        now = datetime.datetime.now()
        player=request.form['PlayerF']
        nat=request.form['NatF']
        data=natTable.find_Joint_Nat(player,nat)
        playersTable=players.Players(dsn)
        data2 =playersTable.select_players()
        temp=render_template('nats.html', current_time=now.ctime(),rows=data, update=False,PlayersSelect=data2)
        natTable.close_con()
        return temp

This code gets the searching criteria, calls the find_Joint_Nat function and finds the requested tuple(s). It also calls select functions of players class and nats class because of the foreign keys.

**updateNatsList function:**

.. code-block:: python
    :linenos:

    def updateNatsList(dsn):
         natTable = nats.Nats(dsn)
         if request.method == 'GET':
            now = datetime.datetime.now()
            data=natTable.select_Joint_Nat()
            temp=render_template('nats.html', current_time=now.ctime(),rows=data, update=True)
            natTable.close_con()
            return temp

This code gets the update page when the "click for update" button is pressed and makes the boolean "update" value True.

2.3 Statistics Table
--------------------
Sql Statements are executed with the functions of the Stats class.

2.3.1 stats.py
++++++++++++++

**__init__ function of Stats class:**

.. code-block:: python
    :linenos:

    def __init__(self, dsn):
        self.connection = dbapi2.connect(dsn)
        self.cursor = self.connection.cursor()

Constructor of the Stats class.

**create_table function of Stats class:**

.. code-block:: python
    :linenos:

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


This code first drops Stats table. Then it creates the Stats table and insert initial tuples to the table.


**select_stats function of Stats class:**

.. code-block:: python
    :linenos:

    def select_stats(self):
        statement = """ SELECT * FROM STATS """
        self.cursor.execute(statement)
        return self.cursor

This code lists all the tuples in the Stats table.


**delete_stat function of Stats class:**

.. code-block:: python
    :linenos:

    def delete_stat(self,Id):
        stement =""" DELETE FROM STATS WHERE ID={}""".format(Id)
        self.cursor.execute(stement)
        self.connection.commit()


This code deletes the tuple which is selected.

**add_stat function of Stats class:**

.. code-block:: python
    :linenos:

    def add_stat(self, team, stat, player):
        if(stat.strip()):
            statement = """ INSERT INTO STATS (FK_TeamsID, NUMOFGAMES, PLAYER) VALUES('{}','{}','{}')""".format(team, stat, player)
            self.cursor.execute(statement)
            self.connection.commit()

This code adds a tuple to Stats table.


**update_stat function of Stats class:**

.. code-block:: python
    :linenos:

    def update_stat(self, Id, stat):
        statement = """UPDATE STATS SET NUMOFGAMES = {} WHERE ID = {}""".format( stat, Id)
        self.cursor.execute(statement)
        self.connection.commit()


This code updates the attributes of the Stats table except the foreign key.


**select_Joint_Stat function of Stats class:**

.. code-block:: python
    :linenos:

    def select_Joint_Stat(self):
        statement = """ SELECT STATS.ID, TEAMS.Name,PLAYER, NUMOFGAMES FROM STATS INNER JOIN TEAMS ON TEAMS.ID=STATS.FK_TEAMSID  """
        self.cursor.execute(statement)
        return self.cursor

This code lists all the tuples in Stats table with the foreign key.

**find_Joint_Stat function of Stats class:**

.. code-block:: python
    :linenos:

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

This code finds the tuples of Stats table according to the searching criteria with the foreign key.

**close_con function of Stats class:**

.. code-block:: python
    :linenos:

    def close_con(self):
        self.connection.close()

This code closes the connection.




2.3.2 statslist.py
++++++++++++++++++

**statsList function:**

.. code-block:: python
    :linenos:

    def statsList(dsn):
    statTable = stats.Stats(dsn)
    if request.method == 'GET':
        now = datetime.datetime.now()
        teamsTable=teams.Teams(dsn)
        data2 =teamsTable.select_teams()
        data=statTable.select_Joint_Stat()
        return render_template('stats.html', current_time=now.ctime(),rows=data, update=False,TeamsSelect=data2)

This code calls the stats page. This page contains information from teams page. So it calls the "select" function of teams class and collects the information. Then it calls the select_Joint_Stat function and executes the listing.

.. code-block:: python
    :linenos:

    elif 'Delete' in request.form:
        keys = request.form.getlist('movies_to_delete')
        for key in keys:
            statTable.delete_stat(key)
        statTable.close_con()
        return redirect(url_for('statsList'))

This code gets the key, calls the delete_stat function and deletes the selected tuple.

.. code-block:: python
    :linenos:

    elif 'Add' in request.form:
        team=request.form['SelectTeamName']
        player=request.form['Player']
        stat=request.form['Stat']
        statTable.add_stat(team, stat, player)
        statTable.close_con()
        return redirect(url_for('statsList'))

This code gets the input values, calls the add_stat function and adds a tuple.

.. code-block:: python
    :linenos:

    elif 'Update2' in request.form:
        keys = request.form.getlist('movies_to_delete')
        for key in keys:
           stat=request.form['Stat'+key]
           statTable.update_stat(key,stat)
        statTable.close_con()
        return redirect(url_for('statsListUpdate'))

This code gets the up-to-date values, calls the update_stat function and updates the tuple.

.. code-block:: python
    :linenos:

    elif 'Find' in request.form:
        now = datetime.datetime.now()
        team=request.form['TeamF']
        player=request.form['PlayerF']
        stat=request.form['StatF']
        data=statTable.find_Joint_Stat(team,stat, player)
        teamsTable=teams.Teams(dsn)
        data2 =teamsTable.select_teams()
        temp=render_template('stats.html', current_time=now.ctime(),rows=data, update=False,TeamsSelect=data2)
        statTable.close_con()
        return temp

This code gets the searching criteria, calls the find_Joint_Stat function and finds the requested tuple(s). It also calls select function of teams class because of the foreign key.

**updateStatsList:**

.. code-block:: python
    :linenos:

    def updateStatsList(dsn):
         statTable = stats.Stats(dsn)
         if request.method == 'GET':
            now = datetime.datetime.now()
            data=statTable.select_Joint_Stat()
            temp=render_template('stats.html', current_time=now.ctime(),rows=data, update=True)
            statTable.close_con()
            return temp

This code gets the update page when the "click for update" button is pressed and makes the boolean "update" value True.

