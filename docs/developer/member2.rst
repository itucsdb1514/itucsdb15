Parts Implemented by Burak Bayboğa
==================================

1 Stadiums Table
----------------

1.1 stadiums.py
+++++++++++++++

Sql Statements are executed with the functions of the Stadiums class.


                +---------------+------------+
                |Name           |Type        |
                +===============+============+
                |id             |INTEGER     |
                +---------------+------------+
                |name           |varchar(40) |
                +---------------+------------+
                |city           |varchar(40) |
                +---------------+------------+
                |year           |INTEGER     |
                +---------------+------------+

__init__ function of Stadiums class:

.. code-block:: python
   :linenos:

   def __init__(self, dsn):
        self.connection = dbapi2.connect(dsn)
        self.cursor = self.connection.cursor()

Constructor of the stadium class.


create_table function of Stadiums class:

.. code-block:: python
    :linenos:

    def create_table(self):
        try:
            stat1 = """ DROP TABLE Stadiums """
            self.cursor.execute(stat1)
            self.connection.commit()
        except dbapi2.DatabaseError:
            self.connection.rollback()
        try:
            stat1 = """ CREATE TABLE Stadiums (
                ID SERIAL PRIMARY KEY,
                NAME VARCHAR(40),
                CITY VARCHAR(40),
                YEAR INTEGER
                ) """
            self.cursor.execute(stat1)
            stat1 = """ INSERT INTO Stadiums (NAME, CITY, YEAR) VALUES('StadiumOne', 'CityOne', 1900)"""
            self.cursor.execute(stat1)
            stat1 = """ INSERT INTO Stadiums (NAME, CITY, YEAR) VALUES('StadiumTwo', 'CityTwo', 1901)"""
            self.cursor.execute(stat1)
            self.connection.commit()
        except dbapi2.DatabaseError:
            self.connection.rollback()


This code first drops Stadiums table. Then it creates the Stadiums table and inserts initial tuples to the table.



select_stadiums function of Stadiums class:

.. code-block:: python
    :linenos:


   def select_stadiums(self):
        statement = """ SELECT * FROM Stadiums """
        self.cursor.execute(statement)
        return self.cursor

This code lists all the tuples in the Stadiums table.


update_stadium function of Stadiums class:

.. code-block:: python
    :linenos:

    def update_stadium(self, Id, name, city, year):
        statement = """UPDATE Stadiums SET NAME = '{}', CITY = '{}', YEAR = {} WHERE ID = {}""".format( name, city, year, Id)
        self.cursor.execute(statement)
        self.connection.commit()

This code updates the attributes of the Stadiums table.

find_teams function of Stadiums class:

.. code-block:: python
    :linenos:

    def find_Stadiums(self, name, city, year):
        condition=''
        if(name.strip()):
            condition+=""" NAME LIKE '%{}%' """.format(name)
        if(city.strip()):
            if(condition.strip()):
                condition+='AND'
            condition+=""" CITY LIKE '%{}%' """.format(city)
        if(year.strip()):
            if(condition.strip()):
                condition+='AND'
            condition+=""" YEAR = {} """.format(year)
        if(condition.strip()):
            condition=' WHERE '+ condition

        statement = """ SELECT * FROM Stadiums """+condition
        self.cursor.execute(statement)
        return self.cursor


This code finds the tuples of Stadiums table according to the searching criteria.

delete_team function of Stadiums class:

.. code-block:: python
    :linenos:

    def delete_stadium(self,Id):
        stement =""" DELETE FROM Stadiums WHERE ID={}""".format(Id)
        self.cursor.execute(stement)
        self.connection.commit()

This code deletes the tuple which is selected.

add_team function of Stadiums class:

.. code-block:: python
    :linenos:

    def add_stadium(self, name, city, year):
        if(name.strip() and city.strip() ):
            statement = """ INSERT INTO Stadiums (NAME, CITY, YEAR) VALUES('{}','{}',{})""".format(name, city, year)
            self.cursor.execute(statement)
            self.connection.commit()

This code adds a tuple to Stadiums table.

close_con function of Stadiums class:

.. code-block:: python
    :linenos:

    def close_con(self):
        self.connection.close()

This code closes the connection.

1.2 stadiumslist.py
+++++++++++++++++++

stadiumsList function:

.. code-block:: python
   :linenos:

   def stadiumsList(dsn):
    stadiumTable = stadiums.Stadiums(dsn)
    if request.method == 'GET':
        now = datetime.datetime.now()
        data=stadiumTable.select_stadiums()
        return render_template('stadiums.html', current_time=now.ctime(),rows=data, update=False)

This code calls the stadiums page.

.. code-block:: python
    :linenos:

    elif 'Delete' in request.form:
        keys = request.form.getlist('movies_to_delete')
        for key in keys:
            stadiumTable.delete_stadium(key)
        stadiumTable.close_con()
        return redirect(url_for('stadiumsList'))

This code gets the key, calls the delete_stadium function and deletes the selected tuple.

.. code-block:: python
    :linenos:

    elif 'Add' in request.form:
        name=request.form['Name']
        city=request.form['City']
        year=request.form['Year']
        stadiumTable.add_stadium(name,city,year)
        stadiumTable.close_con()
        return redirect(url_for('stadiumsList'))

This code gets the input values, calls the add_stadium function and adds a tuple.

.. code-block:: python
    :linenos:

    elif 'Update2' in request.form:
        keys = request.form.getlist('movies_to_delete')
        for key in keys:
           name=request.form['Name'+key]
           city=request.form['City'+key]
           year=request.form['Year'+key]
           stadiumTable.update_stadium(key, name, city, year)
        stadiumTable.close_con()
        return redirect(url_for('stadiumsListUpdate'))


This code gets the up-to-date values, calls the update_team function and updates the tuple.

.. code-block:: python
    :linenos:

    elif 'Find' in request.form:
        now = datetime.datetime.now()
        name=request.form['NameF']
        city=request.form['CityF']
        year=request.form['YearF']
        data=stadiumTable.find_Stadiums(name, city, year)
        temp=render_template('stadiums.html', current_time=now.ctime(),rows=data, update=False)
        stadiumTable.close_con()
        return temp

This code gets the searching criteria, calls the find_teams function and finds the requested tuple(s).


updateStadiumsList function:

.. code-block:: python
    :linenos:

    def updateStadiumsList(dsn):
    stadiumTable = stadiums.Stadiums(dsn)
    if request.method == 'GET':
        now = datetime.datetime.now()
        data=stadiumTable.select_stadiums()
        temp=render_template('stadiums.html', current_time=now.ctime(),rows=data, update=True)
        stadiumTable.close_con()
        return temp

This code gets the update page when the "click for update" button is pressed and makes the boolean "update" value True.


2 Matches Table
---------------

2.1 matches.py
++++++++++++++

Sql Statements are executed with the functions of the Matches class.


                +---------------+------------+
                |Name           |Type        |
                +===============+============+
                |id             |INTEGER     |
                +---------------+------------+
                |op1            |varchar(40) |
                +---------------+------------+
                |op2            |varchar(40) |
                +---------------+------------+
                |year           |INTEGER     |
                +---------------+------------+
                |stadium id     |INTEGER     |
                +---------------+------------+


Stadium ID is a foreign key and it references to the Stadiums table. The stadium name is used in the Matches table.

__init__ function of Matches class:

.. code-block:: python
    :linenos:

    def __init__(self, dsn):
        self.connection = dbapi2.connect(dsn)
        self.cursor = self.connection.cursor()

Constructor of the Matches class.

create_table function of Matches class:

.. code-block:: python
    :linenos:

    def create_table(self):
        try:
            stat1 = """ DROP TABLE Matches """
            self.cursor.execute(stat1)
            self.connection.commit()
        except dbapi2.DatabaseError:
            self.connection.rollback()
        try:
            stat1 = """ CREATE TABLE Matches (
                ID SERIAL PRIMARY KEY,
                OP1 VARCHAR(40),
                OP2 VARCHAR(40),
                YEAR INTEGER,
                FK_StadiumsID INTEGER REFERENCES STADIUMS ON DELETE CASCADE ON UPDATE CASCADE
                ) """
            self.cursor.execute(stat1)
            stat1 = """ INSERT INTO Matches (OP1, OP2, YEAR, FK_StadiumsID) VALUES('fener', 'galata', 1900,1)"""
            self.cursor.execute(stat1)
            stat1 = """ INSERT INTO Matches (OP1, OP2, YEAR, FK_StadiumsID) VALUES('besiktas', 'trabzon', 1901,2)"""
            self.cursor.execute(stat1)
            self.connection.commit()
        except dbapi2.DatabaseError:
            self.connection.rollback()

This code first drops Matches table. Then it creates the Matches table and inserts initial tuples to the table.


delete_match function of Matches class:

.. code-block:: python
    :linenos:

    def delete_match(self,Id):
        stement =""" DELETE FROM Matches WHERE ID={}""".format(Id)
        self.cursor.execute(stement)
        self.connection.commit()

This code deletes the tuple which is selected.

add_match function of Matches class:

.. code-block:: python
    :linenos:

    def add_match(self, op1, op2, year, stadium):
        if(op1.strip() and op2.strip() ):
            statement = """ INSERT INTO Matches (OP1, OP2, YEAR, FK_StadiumsID) VALUES('{}','{}',{}, '{}')""".format(op1, op2, year, stadium)
            self.cursor.execute(statement)
            self.connection.commit()


This code adds a tuple to Matches table.


update_match function of Matches class:

.. code-block:: python
    :linenos:

    def update_match(self, Id, op1, op2, year):
        statement = """UPDATE Matches SET OP1 = '{}', OP2 = '{}', YEAR={} WHERE ID = {}""".format(op1, op2, year, Id)
        self.cursor.execute(statement)
        self.connection.commit()

This code updates the attributes of the Matches table except the foreign keys.


select_Joint_Match function of Coaches class:

.. code-block:: python
    :linenos:

    def select_Joint_Match(self):
        statement = """ SELECT Matches.ID, Stadiums.Name, OP1, OP2, Matches.YEAR FROM Matches INNER JOIN Stadiums ON Stadiums.ID = Matches.FK_StadiumsID """
        self.cursor.execute(statement)
        return self.cursor

This code lists all the tuples in Matches table with the foreign keys.

find_Joint_Match function of Matches class:

.. code-block:: python
    :linenos:

    def find_Joint_Match(self, op1, op2, year, stadium):
        statement = """ SELECT Matches.ID, Stadiums.Name, OP1, OP2, Matches.YEAR FROM Matches INNER JOIN Stadiums ON Stadiums.ID = Matches.FK_StadiumsID """
        condition=''
        if(stadium.strip()):
            condition+=""" Stadiums.Name LIKE '%{}%' """.format(stadium)
        if(op1.strip()):
            if(condition.strip()):
                condition+=' AND'
            condition+=""" OP1  LIKE '%{}%' """.format(op1)
        if(op2.strip()):
            if(condition.strip()):
                condition+=' AND'
            condition+= """ OP2 LIKE '%{}%' """.format(op2)
        if(year.strip()):
            if(condition.strip()):
                condition+=' AND'
            condition+= """ Matches.YEAR = {} """.format(year)
        if(condition.strip()):
            condition = ' WHERE ' + condition
        self.cursor.execute(statement+condition)
        return self.cursor

This code finds the tuples of Matches table according to the searching criteria with foreign keys.

close_con function of Matches class:

.. code-block:: python
    :linenos:

    def close_con(self):
        self.connection.close()

This code closes the connection.

2.2 matcheslist.py
++++++++++++++++++

matchesList function:

.. code-block:: python
   :linenos:

    def matchesList(dsn):
    matchTable = matches.Matches(dsn)
    if request.method == 'GET':
        now = datetime.datetime.now()
        stadiumsTable = stadiums.Stadiums(dsn)
        data2 = stadiumsTable.select_stadiums()
        data=matchTable.select_Joint_Match()
        return render_template('matches.html', current_time=now.ctime(),rows=data, update = False, StadiumsSelect=data2)

This code calls the matches page. This page contains information from the
stadiums page. So it calls the "select" functions of stadiums class and
collects the information. Then it calls the select_Joint_Match function
and executes the listing.

.. code-block:: python
    :linenos:

    elif 'Delete' in request.form:
        keys = request.form.getlist('movies_to_delete')
        for key in keys:
            matchTable.delete_match(key)
        matchTable.close_con()
        return redirect(url_for('matchesList'))

This code gets the key, calls the delete_match function and deletes the selected tuple.

.. code-block:: python
    :linenos:

    elif 'Add' in request.form:
        stadium = request.form['SelectStadiumName']
        op1=request.form['OP1']
        op2=request.form['OP2']
        year=request.form['Year']
        matchTable.add_match(op1,op2,year,stadium)
        matchTable.close_con()
        return redirect(url_for('matchesList'))

This code gets the input values, calls the add_match function and adds a tuple.

.. code-block:: python
    :linenos:

    elif 'Update2' in request.form:
        keys = request.form.getlist('movies_to_delete')
        for key in keys:
            op1=request.form['OP1'+key]
            op2=request.form['OP2'+key]
            year=request.form['Year'+key]
            matchTable.update_match(key,op1,op2,year)
        matchTable.close_con()
        return redirect(url_for('matchesListUpdate'))

This code gets the up-to-date values, calls the update_match function and updates the tuple.

.. code-block:: python
    :linenos:

    elif 'Find' in request.form:
        now = datetime.datetime.now()
        stadium=request.form['StadiumF']
        op1=request.form['OP1F']
        op2=request.form['OP2F']
        year = request.form['YearF']
        data=matchTable.find_Joint_Match(op1,op2,year,stadium)
        stadiumsTable=stadiums.Stadiums(dsn)
        data2 =stadiumsTable.select_stadiums()
        temp=render_template('matches.html', current_time=now.ctime(),rows=data, update=False,StadiumsSelect=data2)
        matchTable.close_con()
        return temp

This code gets the searching criteria, calls the find_Joint_Match function and finds the requested tuple(s). It also calls the select function of the stadiums class because of the foreign keys.

updateCoachesList:

.. code-block:: python
    :linenos:

    def updateMatchesList(dsn):
    matchTable = matches.Matches(dsn)
    if request.method=='GET':
        now = datetime.datetime.now()
        data=matchTable.select_Joint_Match()
        temp=render_template('matches.html', current_time=now.ctime(),rows=data,update=True)
        matchTable.close_con()
        return temp

This code gets the update page when the "click for update" button is pressed and makes the boolean "update" value True.


3 Bet Bates Table
-----------------

3.1 betrates.py
+++++++++++++++

Sql Statements are executed with the functions of the Betrates class.


                +---------------+------------+
                |Name           |Type        |
                +===============+============+
                |id             |INTEGER     |
                +---------------+------------+
                |home           |INTEGER     |
                +---------------+------------+
                |away           |INTEGER     |
                +---------------+------------+
                |draw           |INTEGER     |
                +---------------+------------+
                |match id       |INTEGER     |
                +---------------+------------+

Match id is a foreign key and it references to the Matches table. Two teams from the same ID are used in the Betrates table.

__init__ function of Betrates class:

.. code-block:: python
    :linenos:

    def __init__(self, dsn):
        self.connection = dbapi2.connect(dsn)
        self.cursor = self.connection.cursor()


Constructor of the Betrates class.

create_table function of Betrates class:

.. code-block:: python
    :linenos:

    def create_table(self):
        try:
            stat1 = """ DROP TABLE Betrates """
            self.cursor.execute(stat1)
            self.connection.commit()
        except dbapi2.DatabaseError:
            self.connection.rollback()
        try:
            stat1 = """ CREATE TABLE Betrates (
                ID SERIAL PRIMARY KEY,
                HOME INTEGER,
                AWAY INTEGER,
                DRAW INTEGER,
                FK_MatchesID INTEGER REFERENCES MATCHES ON DELETE CASCADE ON UPDATE CASCADE
                ) """
            self.cursor.execute(stat1)
            stat1 = """ INSERT INTO Betrates (HOME, AWAY, DRAW, FK_MatchesID) VALUES(2, 5, 15,1)"""
            self.cursor.execute(stat1)
            stat1 = """ INSERT INTO Betrates (HOME, AWAY, DRAW, FK_MatchesID) VALUES(2, 3, 4,2)"""
            self.cursor.execute(stat1)
            self.connection.commit()
        except dbapi2.DatabaseError:
            self.connection.rollback()


This code first drops Betrates table. Then it creates the Betrates table and insert initial tuples to the table.


delete_betrate function of Betrate class:

.. code-block:: python
    :linenos:

    def delete_betrate(self,Id):
        stement =""" DELETE FROM Betrates WHERE ID={}""".format(Id)
        self.cursor.execute(stement)
        self.connection.commit()

This code deletes the tuple which is selected.

add_betrate function of Betrate class:

.. code-block:: python
    :linenos:

    def add_betrate(self, home, away, draw, match):
        statement = """ INSERT INTO Betrates (HOME, AWAY, DRAW, FK_MatchesID) VALUES({},{},{},'{}')""".format(home, away, draw, match)
        self.cursor.execute(statement)
        self.connection.commit()

This code adds a tuple to Betrate table.


update_betrate function of Betrates class:

.. code-block:: python
    :linenos:

    def update_betrate(self, Id, home, away, draw):
        statement = """UPDATE Betrates SET HOME = {}, AWAY = {}, DRAW = {} WHERE ID = {}""".format(home, away, draw, Id)
        self.cursor.execute(statement)
        self.connection.commit()

This code updates the attributes of the Betrate table except the foreign keys.


select_Joint_Betrate function of Betrate class:

.. code-block:: python
    :linenos:

    def select_Joint_Betrate(self):
        statement = """ SELECT Betrates.ID, Matches.OP1, Matches.OP2, HOME, AWAY, DRAW FROM Betrates INNER JOIN Matches ON Matches.ID = Betrates.FK_MatchesID """
        self.cursor.execute(statement)
        return self.cursor

This code lists all the tuples in Betrates table with the foreign key.

find_Joint_Betrate function of Betrates class:

.. code-block:: python
    :linenos:

    def find_Joint_Betrate(self, home, away, draw, match1, match2):
        statement = """ SELECT Betrates.ID, Matches.OP1, Matches.OP2, Home, Away, Draw FROM Betrates INNER JOIN Matches ON Matches.ID = Betrates.FK_MatchesID """
        condition=''
        if(match1.strip()):
            condition+=""" Matches.OP1='{}' """.format(match1)
        if(match2.strip()):
            if(condition.strip()):
                condition+=' AND'
            condition+=""" Matches.OP2='{}' """.format(match2)
        if(home.strip()):
            if(condition.strip()):
                condition+=' AND'
            condition+=""" HOME={} """.format(home)
        if(away.strip()):
            if(condition.strip()):
                condition+=' AND'
            condition+= """ AWAY={} """.format(away)
        if(draw.strip()):
            if(condition.strip()):
                condition+=' AND'
            condition+= """ DRAW = {} """.format(draw)
        if(condition.strip()):
            condition = ' WHERE ' + condition
        self.cursor.execute(statement+condition)
        return self.cursor


This code finds the tuples of Betrates table according to the searching criteria with the foreign key.

close_con function of Betrates class:

.. code-block:: python
    :linenos:

    def close_con(self):
        self.connection.close()

This code closes the connection.

3.2 betrates.py
+++++++++++++++

betratesList function:

.. code-block:: python
    :linenos:

    def betratesList(dsn):
    betrateTable = betrates.Betrates(dsn)
    if request.method == 'GET':
        now = datetime.datetime.now()
        matchesTable = matches.Matches(dsn)
        data2 = matchesTable.select_Joint_Match()
        data=betrateTable.select_Joint_Betrate()
        return render_template('betrates.html', current_time=now.ctime(),rows=data, update = False, MatchesSelect=data2)

This code calls the betrates page. This page contains information from the matches page. So it calls the "select" function of matches class and collects the information. Then it calls the select_Joint_Coach function and executes the listing.

.. code-block:: python
    :linenos:

    elif 'Delete' in request.form:
        keys = request.form.getlist('movies_to_delete')
        for key in keys:
            betrateTable.delete_betrate(key)
        betrateTable.close_con()
        return redirect(url_for('betratesList'))

This code gets the key, calls the delete_betrate function and deletes the selected tuple.

.. code-block:: python
    :linenos:

    elif 'Add' in request.form:
        match = request.form['SelectMatchOP1']
        home=request.form['Home']
        away=request.form['Away']
        draw=request.form['Draw']
        betrateTable.add_betrate(home,away,draw,match)
        betrateTable.close_con()
        return redirect(url_for('betratesList'))

This code gets the input values, calls the add_betrate function and adds a tuple.

.. code-block:: python
    :linenos:

    elif 'Update2' in request.form:
        keys = request.form.getlist('movies_to_delete')
        for key in keys:
            home=request.form['Home'+key]
            away=request.form['Away'+key]
            draw=request.form['Draw'+key]
            betrateTable.update_betrate(key,home,away, draw)
        betrateTable.close_con()
        return redirect(url_for('betratesListUpdate'))

This code gets the up-to-date values, calls the update_betrate function and updates the tuple.

.. code-block:: python
    :linenos:

    elif 'Find' in request.form:
        now = datetime.datetime.now()
        match1=request.form['Match1F']
        match2=request.form['Match2F']
        home=request.form['HomeF']
        away=request.form['AwayF']
        draw = request.form['DrawF']
        data=betrateTable.find_Joint_Betrate(home,away,draw,match1, match2)
        matchesTable=matches.Matches(dsn)
        data2 =matchesTable.select_Joint_Match()
        temp=render_template('betrates.html', current_time=now.ctime(),rows=data, update=False,MatchesSelect=data2)
        betrateTable.close_con()
        return temp

This code gets the searching criteria, calls the find_Joint_Betrate function and finds the requested tuple(s). It also calls the select function of the matches class because of the foreign key.

updateCoachesList:

.. code-block:: python
    :linenos:

    def updateBetratesList(dsn):
    betrateTable = betrates.Betrates(dsn)
    if request.method=='GET':
        now = datetime.datetime.now()
        data=betrateTable.select_Joint_Betrate()
        temp=render_template('betrates.html', current_time=now.ctime(),rows=data,update=True)
        betrateTable.close_con()
        return temp

This code gets the update page when the "click for update" button is pressed and makes the boolean "update" value True.









