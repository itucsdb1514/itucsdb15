Parts Implemented by Hüseyin Yavuz
**********************************



1 Database Design
=================


1.1 Teams Table
---------------


                +---------------+------------+
                |Name           |Type        |
                +===============+============+
                |id             |INTEGER     |
                +---------------+------------+
                |name           |varchar(40) |
                +---------------+------------+
                |country        |varchar(40) |
                +---------------+------------+
                |foundationyear |INTEGER     |
                +---------------+------------+




1.2 Coaches Table
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
                |team id        |INTEGER     |
                +---------------+------------+
                |league id      |INTEGER     |
                +---------------+------------+

Team id is a foreign key and it references to the Teams table. Team name is used in Coaches table.

League id is a foreign key and it references to the Leagues table. League name is used in Coaches table.

1.3 Leagues Table
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
                |year           |INTEGER     |
                +---------------+------------+
                |team id        |INTEGER     |
                +---------------+------------+

Team id is a foreign key and it references to the Teams table. Team name is used in Leagues table.

2 Code
======

2.1 Teams Table
---------------
Sql Statements are executed with the functions of the Teams class.

2.1.1 teams.py
++++++++++++++



**__init__ function of Teams class:**

.. code-block:: python
    :linenos:

    def __init__(self, dsn):
        self.connection = dbapi2.connect(dsn)
        self.cursor = self.connection.cursor()

Constructor of the team class.


**create_table function of Teams class:**

.. code-block:: python
    :linenos:

    def create_table(self):
        try:
            stat1 = """ DROP TABLE Teams """
            self.cursor.execute(stat1)
            self.connection.commit()
        except dbapi2.DatabaseError:
            self.connection.rollback()
        try:
            stat1 = """ CREATE TABLE Teams (
                ID SERIAL PRIMARY KEY,
                NAME VARCHAR(40),
                COUNTRY VARCHAR(40),
                YEAR INTEGER
                ) """
            self.cursor.execute(stat1)
            stat1 = """ INSERT INTO Teams (NAME, COUNTRY, YEAR) VALUES('New York Yankees', 'USA', 1901)"""
            self.cursor.execute(stat1)
            stat1 = """ INSERT INTO Teams (NAME, COUNTRY, YEAR) VALUES('Boston Red Sox', 'USA', 1903)"""
            self.cursor.execute(stat1)
            stat1 = """ INSERT INTO Teams (NAME, COUNTRY, YEAR) VALUES('San Francisco Giants', 'USA', 1883)"""
            self.cursor.execute(stat1)
            self.connection.commit()
        except dbapi2.DatabaseError:
            self.connection.rollback()


This code first drops Teams table. Then it creates the Teams table and insert initial tuples to the table.


**select_teams function of Teams class:**

.. code-block:: python
    :linenos:

    def select_teams(self):
        statement = """ SELECT * FROM Teams """
        self.cursor.execute(statement)
        return self.cursor

This code lists all the tuples in the Teams table.


**update_team function of Teams class:**

.. code-block:: python
    :linenos:

    def update_team(self, Id, name, country, year):
        statement = """UPDATE Teams SET NAME = '{}', COUNTRY = '{}', YEAR = {} WHERE ID = {}""".format( name, country, year, Id)
        self.cursor.execute(statement)
        self.connection.commit()

This code updates the attributes of the Teams table.


**find_teams function of Teams class:**

.. code-block:: python
    :linenos:

    def find_teams(self, name, country, year):
        condition=''
        if(name.strip()):
            condition+=""" NAME LIKE '%{}%' """.format(name)
        if(country.strip()):
            if(condition.strip()):
                condition+='AND'
            condition+=""" COUNTRY LIKE '%{}%' """.format(country)
        if(year.strip()):
            if(condition.strip()):
                condition+='AND'
            condition+=""" YEAR = {} """.format(year)
        if(condition.strip()):
            condition=' WHERE '+ condition

        statement = """ SELECT * FROM Teams """+condition
        self.cursor.execute(statement)
        return self.cursor

This code finds the tuples of Teams table according to the searching criteria.

**delete_team function of Teams class:**

.. code-block:: python
    :linenos:

    def delete_team(self,Id):
        stement =""" DELETE FROM Teams WHERE ID={}""".format(Id)
        self.cursor.execute(stement)
        self.connection.commit()

This code deletes the tuple which is selected.

**add_team function of Teams class:**

.. code-block:: python
    :linenos:

    def add_team(self, name, country, year):
        if(name.strip() and country.strip() ):
            statement = """ INSERT INTO Teams (NAME, COUNTRY, YEAR) VALUES('{}','{}',{})""".format(name, country, year)
            self.cursor.execute(statement)
            self.connection.commit()

 This code adds a tuple to Teams table.

 **close_con function of Teams class:**

.. code-block:: python
    :linenos:

    def close_con(self):
        self.connection.close()

This code closes the connection.


2.1.2 teamslist.py
++++++++++++++++++

**teamsList function:**

.. code-block:: python
    :linenos:

    def teamsList(dsn):
       teamTable = teams.Teams(dsn)
       if request.method == 'GET':
           now = datetime.datetime.now()
           data=teamTable.select_teams()
           return render_template('teams.html', current_time=now.ctime(),rows=data, update=False)

This code calls the teams page.

.. code-block:: python
    :linenos:

    elif 'Delete' in request.form:
           keys = request.form.getlist('movies_to_delete')
           for key in keys:
               teamTable.delete_team(key)
           teamTable.close_con()
           return redirect(url_for('teamsList'))

This code gets the key, calls the delete_team function and deletes the selected tuple.

.. code-block:: python
    :linenos:

    elif 'Add' in request.form:
           name=request.form['Name']
           country=request.form['Country']
           year=request.form['Year']
           teamTable.add_team(name,country,year)
           teamTable.close_con()
           return redirect(url_for('teamsList'))

This code gets the input values, calls the add_team function and adds a tuple.

.. code-block:: python
    :linenos:

    elif 'Update2' in request.form:
           keys = request.form.getlist('movies_to_delete')
           for key in keys:
              name=request.form['Name'+key]
              country=request.form['Country'+key]
              year=request.form['Year'+key]
              teamTable.update_team(key, name, country, year)
           teamTable.close_con()
           return redirect(url_for('teamsListUpdate'))

This code gets the up-to-date values, calls the update_team function and updates the tuple.

.. code-block:: python
    :linenos:

    elif 'Find' in request.form:
           now = datetime.datetime.now()
           name=request.form['NameF']
           country=request.form['CountryF']
           year=request.form['YearF']
           data=teamTable.find_teams(name, country, year)
           temp=render_template('teams.html', current_time=now.ctime(),rows=data, update=False)
           teamTable.close_con()
           return temp

This code gets the searching criteria, calls the find_teams function and finds the requested tuple(s).


**updateTeamsList function:**

.. code-block:: python
    :linenos:

     def updateTeamsList(dsn):
       teamTable = teams.Teams(dsn)
       if request.method == 'GET':
           now = datetime.datetime.now()
           data=teamTable.select_teams()
           temp=render_template('teams.html', current_time=now.ctime(),rows=data, update=True)
           teamTable.close_con()
           return temp

This code gets the update page when the "click for update" button is pressed and makes the boolean "update" value True.


2.2 Coaches Table
-----------------
Sql Statements are executed with the functions of the Coaches class.

2.2.1 coaches.py
++++++++++++++++


**__init__ function of Coaches class:**

.. code-block:: python
    :linenos:

    def __init__(self, dsn):
        self.connection = dbapi2.connect(dsn)
        self.cursor = self.connection.cursor()

Constructor of the Coaches class.

**create_table function of Coaches class:**

.. code-block:: python
    :linenos:

    def create_table(self):
        try:
            stat1 = """ DROP TABLE Coaches """
            self.cursor.execute(stat1)
            self.connection.commit()
        except dbapi2.DatabaseError:
            self.connection.rollback()
        try:

            stat1 = """ CREATE TABLE Coaches (
                ID SERIAL PRIMARY KEY,
                NAME VARCHAR(40),
                COUNTRY VARCHAR(40),
                AGE INTEGER,
                FK_TeamsID INTEGER REFERENCES Teams ON DELETE CASCADE ON UPDATE CASCADE,
                FK_LeaguesID INTEGER REFERENCES Leagues ON DELETE CASCADE ON UPDATE CASCADE
                ) """
            self.cursor.execute(stat1)
            stat1 = """ INSERT INTO Coaches (NAME, COUNTRY, AGE, FK_TeamsID, FK_LeaguesID) VALUES('Joe Girardi', 'USA', 51,1,1)"""
            self.cursor.execute(stat1)
            stat1 = """ INSERT INTO Coaches (NAME, COUNTRY, AGE, FK_TeamsID, FK_LeaguesID) VALUES('John Farrell', 'USA', 53,2,1)"""
            self.cursor.execute(stat1)
            stat1 = """ INSERT INTO Coaches (NAME, COUNTRY, AGE, FK_TeamsID, FK_LeaguesID) VALUES('Bruce Bochy', 'FRA', 60,3,1)"""
            self.cursor.execute(stat1)
            self.connection.commit()

        except dbapi2.DatabaseError:
            self.connection.rollback()


This code first drops Coaches table. Then it creates the Coaches table and insert initial tuples to the table.


**select_coaches function of Coaches class:**

.. code-block:: python
    :linenos:

    def select_coaches(self):
        statement = """ SELECT * FROM Coaches """
        self.cursor.execute(statement)
        return self.cursor

This code lists all the tuples in the Coaches table.

**find_coaches function of Coaches class:**

.. code-block:: python
    :linenos:

    def find_Coaches(self,team,league,name,country,age):
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
            condition=' WHERE '+condition

        statement = """ SELECT * FROM Coaches """+condition
        self.cursor.execute(statement)
        return self.cursor


This code finds the tuples of Coaches table according to the searching criteria.

**delete_coach function of Coaches class:**

.. code-block:: python
    :linenos:

    def delete_coach(self,Id):
        stement =""" DELETE FROM Coaches WHERE ID={}""".format(Id)
        self.cursor.execute(stement)
        self.connection.commit()


This code deletes the tuple which is selected.

**add_coach function of Coaches class:**

.. code-block:: python
    :linenos:

    def add_coach(self, team, league, name, country, age):
        if(name.strip() and country.strip() ):
            statement = """ INSERT INTO Coaches (FK_TeamsID,FK_LeaguesID, NAME, COUNTRY, AGE) VALUES({},{},'{}','{}',{})""".format(team,league, name, country, age)
            self.cursor.execute(statement)
            self.connection.commit()

This code adds a tuple to Coaches table.


**update_coach function of Coaches class:**

.. code-block:: python
    :linenos:

    def update_coach(self, Id, name, country, age):
        statement = """UPDATE Coaches SET NAME = '{}', COUNTRY = '{}', AGE = {} WHERE ID = {}""".format( name, country, age, Id)
        self.cursor.execute(statement)
        self.connection.commit()


This code updates the attributes of the Coaches table except the foreign keys.


**select_Joint_Coach function of Coaches class:**

.. code-block:: python
    :linenos:

    def select_Joint_Coach(self):
        statement = """ SELECT Coaches.ID,Teams.Name,Leagues.Name, Coaches.NAME,Coaches.COUNTRY,AGE FROM Coaches INNER JOIN Teams ON Teams.ID=Coaches.FK_TeamsID INNER JOIN Leagues ON Leagues.ID=Coaches.FK_LeaguesID  """
        self.cursor.execute(statement)
        return self.cursor

This code lists all the tuples in Coaches table with the foreign keys.

**find_Joint_Coach function of Coaches class:**

.. code-block:: python
    :linenos:

    def find_Joint_Coach(self,team,league,name,country,age):
        statement = """ SELECT Coaches.ID,Teams.Name,Leagues.Name, Coaches.NAME,Coaches.COUNTRY,AGE FROM Coaches INNER JOIN Teams ON Teams.ID=Coaches.FK_TeamsID INNER JOIN Leagues ON Leagues.ID=Coaches.FK_LeaguesID """
        condition=''
        if(team.strip()):
            condition+=""" Teams.Name LIKE '%{}%'""".format(team)
        if(league.strip()):
            condition+=""" Leagues.Name LIKE '%{}%'""".format(league)
        if(name.strip()):
            if(condition.strip()):
                condition+='AND'
            condition+=""" Coaches.NAME LIKE '%{}%' """.format(name)
        if(country.strip()):
            if(condition.strip()):
                condition+='AND'
            condition+=""" Coaches.COUNTRY LIKE '%{}%' """.format(country)
        if(age.strip()):
            if(condition.strip()):
                condition+='AND'
            condition+=""" AGE={} """.format(age)
        if(condition.strip()):
            condition=' WHERE '+condition
        self.cursor.execute(statement+condition)
        return self.cursor

This code finds the tuples of Coaches table according to the searching criteria with foreign keys.

**close_con function of Coaches class:**

.. code-block:: python
    :linenos:

    def close_con(self):
        self.connection.close()

This code closes the connection.


2.2.2 coacheslist.py
++++++++++++++++++++

**coachesList function:**

.. code-block:: python
    :linenos:

    def coachesList(dsn):
    coachTable = coaches.Coaches(dsn)
    if request.method == 'GET':
        now = datetime.datetime.now()
        teamsTable=teams.Teams(dsn)
        data2=teamsTable.select_teams()
        leaguesTable=leagues.Leagues(dsn)
        data3=leaguesTable.select_leagues()
        data=coachTable.select_Joint_Coach()
        return render_template('coaches.html', current_time=now.ctime(),rows=data, update=False,TeamsSelect=data2,LeaguesSelect=data3)

This code calls the coaches page. This page contains information from teams page and leagues page. So it calls the "select" functions of leagues class and teams class and collects the information. Then it calls the select_Joint_Coach function and executes the listing.

.. code-block:: python
    :linenos:

    elif 'Delete' in request.form:
        keys = request.form.getlist('movies_to_delete')
        for key in keys:
            coachTable.delete_coach(key)
        coachTable.close_con()
        return redirect(url_for('coachesList'))

This code gets the key, calls the delete_coach function and deletes the selected tuple.

.. code-block:: python
    :linenos:

    elif 'Add' in request.form:
        team=request.form['SelectTeamName']
        league=request.form['SelectLeagueName']
        name=request.form['Name']
        country=request.form['Country']
        age=request.form['Age']
        coachTable.add_coach(team,league,name,country,age)
        coachTable.close_con()
        return redirect(url_for('coachesList'))

This code gets the input values, calls the add_coach function and adds a tuple.

.. code-block:: python
    :linenos:

    elif 'Update2' in request.form:
        keys = request.form.getlist('movies_to_delete')
        for key in keys:
           name=request.form['Name'+key]
           country=request.form['Country'+key]
           age=request.form['Age'+key]
           coachTable.update_coach(key,name,country,age)
        coachTable.close_con()
        return redirect(url_for('coachesListUpdate'))

This code gets the up-to-date values, calls the update_coach function and updates the tuple.

.. code-block:: python
    :linenos:

    elif 'Find' in request.form:
        now = datetime.datetime.now()
        team=request.form['TeamF']
        league=request.form['LeagueF']
        name=request.form['NameF']
        country=request.form['CountryF']
        age=request.form['AgeF']
        data=coachTable.find_Joint_Coach(team,league,name,country,age)
        teamsTable=teams.Teams(dsn)
        data2 =teamsTable.select_teams()
        leaguesTable=leagues.Leagues(dsn)
        data3=leaguesTable.select_leagues()
        temp=render_template('coaches.html', current_time=now.ctime(),rows=data, update=False,TeamsSelect=data2,LeaguesSelect=data3)
        coachTable.close_con()
        return temp

This code gets the searching criteria, calls the find_Joint_Coach function and finds the requested tuple(s). It also calls select functions of leagues class and teams class because of the foreign keys.

**updateCoachesList:**

.. code-block:: python
    :linenos:

    def updateCoachesList(dsn):
    coachTable = coaches.Coaches(dsn)
    if request.method == 'GET':
        now = datetime.datetime.now()
        data=coachTable.select_Joint_Coach()
        temp=render_template('coaches.html', current_time=now.ctime(),rows=data, update=True)
        coachTable.close_con()
        return temp

This code gets the update page when the "click for update" button is pressed and makes the boolean "update" value True.

2.3 Leagues Table
-----------------
Sql Statements are executed with the functions of the Leagues class.

2.3.1 leagues.py
++++++++++++++++

**__init__ function of Leagues class:**

.. code-block:: python
    :linenos:

    def __init__(self, dsn):
        self.connection = dbapi2.connect(dsn)
        self.cursor = self.connection.cursor()

Constructor of the Leagues class.

**create_table function of Leagues class:**

.. code-block:: python
    :linenos:

    def create_table(self):
        try:
            stat1 = """ DROP TABLE Leagues """
            self.cursor.execute(stat1)
            self.connection.commit()
        except dbapi2.DatabaseError:
            self.connection.rollback()
        try:

            stat1 = """ CREATE TABLE Leagues (
                ID SERIAL PRIMARY KEY,
                NAME VARCHAR(40),
                COUNTRY VARCHAR(40),
                YEAR INTEGER,
                FK_TeamsID INTEGER REFERENCES Teams ON DELETE CASCADE ON UPDATE CASCADE
                ) """
            self.cursor.execute(stat1)
            stat1 = """ INSERT INTO Leagues (NAME, COUNTRY, YEAR, FK_TeamsID) VALUES('Major League Baseball', 'USA', 1903,1)"""
            self.cursor.execute(stat1)
            stat1 = """ INSERT INTO Leagues (NAME, COUNTRY, YEAR, FK_TeamsID) VALUES('Minor League Baseball', 'USA', 1868,2)"""
            self.cursor.execute(stat1)
            stat1 = """ INSERT INTO Leagues (NAME, COUNTRY, YEAR, FK_TeamsID) VALUES('Dominican Professional Baseball League', 'DOM', 1951,3)"""
            self.cursor.execute(stat1)
            self.connection.commit()
        except dbapi2.DatabaseError:
            self.connection.rollback()


This code first drops Leagues table. Then it creates the Leagues table and insert initial tuples to the table.


**select_leagues function of Leagues class:**

.. code-block:: python
    :linenos:

    def select_leagues(self):
        statement = """ SELECT * FROM Leagues """
        self.cursor.execute(statement)
        return self.cursor

This code lists all the tuples in the Leagues table.

**find_leagues function of Leagues class:**

.. code-block:: python
    :linenos:

    def find_Leagues(self,team,name,country,year):
        condition=''
        if(name.strip()):
            condition+=""" NAME LIKE '%{}%' """.format(name)
        if(country.strip()):
            if(condition.strip()):
                condition+='AND'
            condition+=""" COUNTRY LIKE '%{}%' """.format(country)
        if(year.strip()):
            if(condition.strip()):
                condition+='AND'
            condition+=""" YEAR = {} """.format(year)
        if(condition.strip()):
            condition=' WHERE '+condition

        statement = """ SELECT * FROM Leagues """+condition
        self.cursor.execute(statement)
        return self.cursor


This code finds the tuples of Leagues table according to the searching criteria.

**delete_league function of Leagues class:**

.. code-block:: python
    :linenos:

    def delete_league(self,Id):
        stement =""" DELETE FROM Leagues WHERE ID={}""".format(Id)
        self.cursor.execute(stement)
        self.connection.commit()


This code deletes the tuple which is selected.

**add_league function of Leagues class:**

.. code-block:: python
    :linenos:

    def add_league(self, team, name, country, year):
        if(name.strip() and country.strip() ):
            statement = """ INSERT INTO Leagues (FK_TeamsID, NAME, COUNTRY, YEAR) VALUES({},'{}','{}',{})""".format(team, name, country, year)
            self.cursor.execute(statement)
            self.connection.commit()

This code adds a tuple to Leagues table.


**update_league function of Leagues class:**

.. code-block:: python
    :linenos:

    def update_league(self, Id, name, country, year):
        statement = """UPDATE Leagues SET NAME = '{}', COUNTRY = '{}', YEAR = {} WHERE ID = {}""".format( name, country, year, Id)
        self.cursor.execute(statement)
        self.connection.commit()


This code updates the attributes of the Leagues table except the foreign key.


**select_Joint_League function of Leagues class:**

.. code-block:: python
    :linenos:

    def select_Joint_League(self):
        statement = """ SELECT Leagues.ID,Teams.Name,Leagues.NAME,Leagues.COUNTRY,Leagues.YEAR FROM Leagues INNER JOIN Teams ON Teams.ID=Leagues.FK_TeamsID  """
        self.cursor.execute(statement)
        return self.cursor

This code lists all the tuples in Leagues table with the foreign key.

**find_Joint_League function of Leagues class:**

.. code-block:: python
    :linenos:

    def find_Joint_League(self,team,name,country,year):
        statement = """ SELECT Leagues.ID,Teams.Name,Leagues.NAME,Leagues.COUNTRY,Leagues.YEAR FROM Leagues INNER JOIN Teams ON Teams.ID=Leagues.FK_TeamsID  """
        condition=''
        if(team.strip()):
            condition+=""" Teams.Name LIKE '%{}%'""".format(team)
        if(name.strip()):
            if(condition.strip()):
                condition+='AND'
            condition+=""" Leagues.NAME LIKE '%{}%' """.format(name)
        if(country.strip()):
            if(condition.strip()):
                condition+='AND'
            condition+=""" Leagues.COUNTRY LIKE '%{}%' """.format(country)
        if(year.strip()):
            if(condition.strip()):
                condition+='AND'
            condition+=""" Leagues.YEAR={} """.format(year)
        if(condition.strip()):
            condition=' WHERE '+condition
        self.cursor.execute(statement+condition)
        return self.cursor

This code finds the tuples of Leagues table according to the searching criteria with the foreign key.

**close_con function of Leagues class:**

.. code-block:: python
    :linenos:

    def close_con(self):
        self.connection.close()

This code closes the connection.




2.3.2 leagueslist.py
++++++++++++++++++++

**leaguesList function:**

.. code-block:: python
    :linenos:

    def leaguesList(dsn):
    leagueTable = leagues.Leagues(dsn)
    if request.method == 'GET':
        now = datetime.datetime.now()
        teamsTable=teams.Teams(dsn)
        data2=teamsTable.select_teams()
        data=leagueTable.select_Joint_League()
        return render_template('leagues.html', current_time=now.ctime(),rows=data, update=False,TeamsSelect=data2)

This code calls the leagues page. This page contains information from teams page. So it calls the "select" function of teams class and collects the information. Then it calls the select_Joint_Coach function and executes the listing.

.. code-block:: python
    :linenos:

    elif 'Delete' in request.form:
        keys = request.form.getlist('movies_to_delete')
        for key in keys:
            leagueTable.delete_league(key)
        leagueTable.close_con()
        return redirect(url_for('leaguesList'))

This code gets the key, calls the delete_league function and deletes the selected tuple.

.. code-block:: python
    :linenos:

    elif 'Add' in request.form:
        team=request.form['SelectTeamName']
        name=request.form['Name']
        country=request.form['Country']
        year=request.form['Year']
        leagueTable.add_league(team,name,country,year)
        leagueTable.close_con()
        return redirect(url_for('leaguesList'))

This code gets the input values, calls the add_league function and adds a tuple.

.. code-block:: python
    :linenos:

    elif 'Update2' in request.form:
        keys = request.form.getlist('movies_to_delete')
        for key in keys:
           name=request.form['Name'+key]
           country=request.form['Country'+key]
           year=request.form['Year'+key]
           leagueTable.update_league(key,name,country,year)
        leagueTable.close_con()
        return redirect(url_for('leaguesListUpdate'))

This code gets the up-to-date values, calls the update_league function and updates the tuple.

.. code-block:: python
    :linenos:

    elif 'Find' in request.form:
        now = datetime.datetime.now()
        team=request.form['TeamF']
        name=request.form['NameF']
        country=request.form['CountryF']
        year=request.form['YearF']
        data=leagueTable.find_Joint_League(team,name,country,year)
        teamsTable=teams.Teams(dsn)
        data2 =teamsTable.select_teams()
        temp=render_template('leagues.html', current_time=now.ctime(),rows=data, update=False,TeamsSelect=data2)
        leagueTable.close_con()
        return temp

This code gets the searching criteria, calls the find_Joint_League function and finds the requested tuple(s). It also calls select function of teams class because of the foreign key.

**updateLeaguesList:**

.. code-block:: python
    :linenos:

    def updateLeaguesList(dsn):
    leagueTable = leagues.Leagues(dsn)
    if request.method == 'GET':
        now = datetime.datetime.now()
        data=leagueTable.select_Joint_League()
        temp=render_template('leagues.html', current_time=now.ctime(),rows=data, update=True)
        leagueTable.close_con()
        return temp

This code gets the update page when the "click for update" button is pressed and makes the boolean "update" value True.
















