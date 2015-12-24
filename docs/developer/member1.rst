Parts Implemented by Hüseyin Tosun
==================================


1 Database Design
=================


1.1 Users Table
---------------


                +---------------+------------+
                |Name           |Type        |
                +===============+============+
                |id             |INTEGER     |
                +---------------+------------+
                |uname          |varchar(40) |
                +---------------+------------+
                |utype          |varchar(40) |
                +---------------+------------+
                |birth          |INTEGER     |
                +---------------+------------+




1.2 Comments Table
------------------


                +---------------+------------+
                |Name           |Type        |
                +===============+============+
                |id             |INTEGER     |
                +---------------+------------+
                |notes          |varchar(40) |
                +---------------+------------+
                |pointcount     |varchar(40) |
                +---------------+------------+
                |playersid      |INTEGER     |
                +---------------+------------+

Playersid is a foreign key and it references to the Players table. From players table, names of the players
are extracted, and used in the Comments table.


1.3 Likes Table
---------------

                +---------------+------------+
                |Name           |Type        |
                +===============+============+
                |id             |INTEGER     |
                +---------------+------------+
                |status         |varchar(40) |
                +---------------+------------+
                |usersid        |varchar(40) |
                +---------------+------------+
                |playersid      |varchar(40) |
                +---------------+------------+

Usersid is a foreign key and it references to the Users table. It is used for the user dropdown menu in the Likes page.
Playersid is a foreign key and it references to the Players table. From players table, names of the players
are extracted, and used in the Likes table.

2 Code
======

2.1 Users Table
---------------
Sql Statements are executed with the functions of the Users class.

2.1.1 users.py
++++++++++++++


**__init__ function of Users class:**

.. code-block:: python
    :linenos:

    def __init__(self, dsn):
        self.connection = dbapi2.connect(dsn)
        self.cursor = self.connection.cursor()

Constructor of the Users object.


**create_table function of Users class:**

.. code-block:: python
    :linenos:

    def create_table(self):
        try:
            stat1 = """ DROP TABLE USERS """
            self.cursor.execute(stat1)
            self.connection.commit()
        except dbapi2.DatabaseError:
            self.connection.rollback()
        try:
            stat1 = """ CREATE TABLE USERS (
                ID SERIAL PRIMARY KEY,
                UNAME VARCHAR(40),
                UTYPE VARCHAR(40),
                BIRTH INTEGER
                ) """
            self.cursor.execute(stat1)
            print('*********')
            stat1 = """ INSERT INTO USERS (UNAME, UTYPE, BIRTH) VALUES('Hüseyin Tosun', 'Admin', 1993)"""
            self.cursor.execute(stat1)
            stat1 = """ INSERT INTO USERS (UNAME, UTYPE, BIRTH) VALUES('Zeynep Yirmibeş', 'Moderator', 1993)"""
            self.cursor.execute(stat1)
            stat1 = """ INSERT INTO USERS (UNAME, UTYPE, BIRTH) VALUES('Alican Yılmaz', 'Guest', 1989)"""
            self.cursor.execute(stat1)
            stat1 = """ INSERT INTO USERS (UNAME, UTYPE, BIRTH) VALUES('Mehmet Koytak', 'Guest', 1995)"""
            self.cursor.execute(stat1)
            self.connection.commit()
        except dbapi2.DatabaseError:
            self.connection.rollback()


This code first drops the Users table, in case it already exists.
Then it creates the Users table and insert initial tuples to the table.


**select_users function of Users class:**

.. code-block:: python
    :linenos:

    def select_users(self):
        statement = """ SELECT * FROM USERS """
        self.cursor.execute(statement)
        return self.cursor

This code selects and lists all the tuples in the Users table.


**update_user function of Users class:**

.. code-block:: python
    :linenos:

    def update_user(self, Id, uname, utype, birth):
        statement = """UPDATE USERS SET UNAME = '{}', UTYPE = '{}', BIRTH = {} WHERE ID = {}""".format( uname, utype, birth, Id)
        self.cursor.execute(statement)
        self.connection.commit()

This code updates the attributes of the Users table according to the input the user enters to the site.


**find_users function of Users class:**

.. code-block:: python
    :linenos:

    def find_Users(self, uname, utype, birth):
        condition=''
        if(uname.strip()):
            condition+=""" UNAME LIKE '%{}%' """.format(uname)
        if(utype.strip()):
            if(condition.strip()):
                condition+='AND'
            condition+=""" UTYPE LIKE '%{}%' """.format(utype)
        if(birth.strip()):
            if(condition.strip()):
                condition+='AND'
            condition+=""" BIRTH = {} """.format(birth)
        if(condition.strip()):
            condition=' WHERE '+ condition

        statement = """ SELECT * FROM USERS """+condition
        self.cursor.execute(statement)
        return self.cursor

This code finds the tuples of Users table according to the searching criteria.

**delete_user function of Users class:**

.. code-block:: python
    :linenos:

    def delete_user(self,Id):
        stement =""" DELETE FROM USERS WHERE ID={}""".format(Id)
        self.cursor.execute(stement)
        self.connection.commit()

This code deletes the tuple that is selected.

**add_user function of Users class:**

.. code-block:: python
    :linenos:

    def add_user(self, uname, utype, birth):
        if(uname.strip() and utype.strip() ):
            statement = """ INSERT INTO USERS (UNAME, UTYPE, BIRTH) VALUES('{}','{}',{})""".format(uname, utype, birth)
            self.cursor.execute(statement)
            self.connection.commit()

 This code adds a tuple to Users table, according to the input from the user.

 **close_con function of Users class:**

.. code-block:: python
    :linenos:

    def close_con(self):
        self.connection.close()

This code closes the connection.


2.1.2 userslist.py
++++++++++++++++++

**usersList function:**

.. code-block:: python
    :linenos:

    def usersList(dsn):
      userTable = users.Users(dsn)
      if request.method == 'GET':
        now = datetime.datetime.now()
        data=userTable.select_users()
        return render_template('users.html', current_time=now.ctime(),rows=data, update=False)

This function calls the users page through users.html.

.. code-block:: python
    :linenos:

    elif 'Delete' in request.form:
        keys = request.form.getlist('movies_to_delete')
        for key in keys:
            userTable.delete_user(key)
        userTable.close_con()
        return redirect(url_for('usersList'))

This code gets the key, calls the delete_user function and deletes the selected tuple.

.. code-block:: python
    :linenos:

    elif 'Add' in request.form:
        uname=request.form['Uname']
        utype=request.form['Utype']
        birth=request.form['Birth']
        userTable.add_user(uname,utype,birth)
        userTable.close_con()
        return redirect(url_for('usersList'))

This code gets the input values, calls the add_user function and adds a tuple.

.. code-block:: python
    :linenos:

    elif 'Update2' in request.form:
        keys = request.form.getlist('movies_to_delete')
        for key in keys:
           uname=request.form['Uname'+key]
           utype=request.form['Utype'+key]
           birth=request.form['Birth'+key]
           userTable.update_user(key, uname, utype, birth)
        userTable.close_con()
        return redirect(url_for('usersListUpdate'))

This code gets the up-to-date values, calls the update_user function and updates the tuple.

.. code-block:: python
    :linenos:

    elif 'Find' in request.form:
        now = datetime.datetime.now()
        uname=request.form['UnameF']
        utype=request.form['UtypeF']
        birth=request.form['BirthF']
        data=userTable.find_Users(uname, utype, birth)
        temp=render_template('users.html', current_time=now.ctime(),rows=data, update=False)
        userTable.close_con()
        return temp

This code gets the searching criteria, calls the find_Users function and finds the requested tuple(s).


**updateUsersList function:**

.. code-block:: python
    :linenos:

     def updateUsersList(dsn):
      userTable = users.Users(dsn)
      if request.method == 'GET':
        now = datetime.datetime.now()
        data=userTable.select_users()
        temp=render_template('users.html', current_time=now.ctime(),rows=data, update=True)
        userTable.close_con()
        return temp


This code gets the update page when the "click for update" button is pressed and makes the boolean "update" value True.


2.2 Comments Table
------------------
Sql Statements are executed with the functions of the Comments class.

2.2.1 comments.py
+++++++++++++++++


**__init__ function of Comments class:**

.. code-block:: python
    :linenos:

    def __init__(self, dsn):
        self.connection = dbapi2.connect(dsn)
        self.cursor = self.connection.cursor()

Constructor of the Comments class.

**create_table function of Comments class:**

.. code-block:: python
    :linenos:

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
                FK_PlayersID INTEGER REFERENCES PLAYERS ON DELETE CASCADE ON UPDATE CASCADE
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


This code first drops the Comments table, in case it already exists.
Then it creates the Comments table and insert initial tuples to the table.


**select_comments function of Comments class:**

.. code-block:: python
    :linenos:

    def select_comments(self):
        statement = """ SELECT * FROM Comments """
        self.cursor.execute(statement)
        return self.cursor

This code lists all the tuples in the Comments table.

**delete_comment function of Nats class:**

.. code-block:: python
    :linenos:

    def delete_comment(self,Id):
        stement =""" DELETE FROM Comments WHERE ID={}""".format(Id)
        self.cursor.execute(stement)
        self.connection.commit()


This code deletes the tuple which is selected.

**add_comment function of Comments class:**

.. code-block:: python
    :linenos:

    def add_comment(self, player, notes, point):
        print(player)
        print(notes)
        print()
        if(player.strip() and notes.strip() ):
            statement = """ INSERT INTO Comments (FK_PlayersID, NOTES, PointCount) VALUES('{}','{}',{})""".format(player, notes, point)
            self.cursor.execute(statement)
            self.connection.commit()

This code adds a tuple to Comments table.


**update_comment function of Comments class:**

.. code-block:: python
    :linenos:

    def update_comment(self, Id,notes, point):
        statement = """UPDATE Comments SET  NOTES = '{}', PointCount = {} WHERE ID = {}""".format( notes, point, Id)
        self.cursor.execute(statement)
        self.connection.commit()


This code updates the attributes of the Comments table except for the foreign keys.


**select_Joint_Comment function of Comments class:**

.. code-block:: python
    :linenos:

    def select_Joint_Comment(self):
        statement = """ SELECT Comments.ID,PLAYERS.Name,NOTES,PointCount FROM Comments INNER JOIN PLAYERS ON PLAYERS.ID=COMMENTS.FK_PLAYERSID  """
        self.cursor.execute(statement)
        return self.cursor

This code lists all the tuples in Comments table with the foreign keys.

**find_Joint_Comment function of Comments class:**

.. code-block:: python
    :linenos:

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

This code finds the tuples of Comments table according to the searching criteria with foreign keys.

**close_con function of Comments class:**

.. code-block:: python
    :linenos:

    def close_con(self):
        self.connection.close()

This code closes the connection.


2.2.2 commentslist.py
+++++++++++++++++++++

**commentsList function:**

.. code-block:: python
    :linenos:

    def commentsList(dsn):
    commentTable = comments.Comments(dsn)
    if request.method == 'GET':
        now = datetime.datetime.now()
        playersTable=players.Players(dsn)
        data2 =playersTable.select_players()
        data=commentTable.select_Joint_Comment()
        return render_template('comments.html', current_time=now.ctime(),rows=data, update=False,PlayersSelect=data2)

This code calls the comments page. This page contains information from players page. So it calls the "select" functions of players class and collects the information. Then it calls the select_Joint_Comment function and executes the listing.

.. code-block:: python
    :linenos:

    elif 'Delete' in request.form:
        keys = request.form.getlist('movies_to_delete')
        for key in keys:
            commentTable.delete_comment(key)
        commentTable.close_con()
        return redirect(url_for('commentsList'))

This code gets the key, calls the delete_comment function and deletes the selected tuple.

.. code-block:: python
    :linenos:

    elif 'Add' in request.form:
        player=request.form['SelectPlayerName']
        notes=request.form['Notes']
        point=request.form['Point']
        commentTable.add_comment(player,notes,point)
        commentTable.close_con()
        return redirect(url_for('commentsList'))

This code gets the input values, calls the add_comment function and adds a tuple.

.. code-block:: python
    :linenos:

    elif 'Update2' in request.form:
        keys = request.form.getlist('movies_to_delete')
        for key in keys:
           notes=request.form['Notes'+key]
           point=request.form['Point'+key]
           commentTable.update_comment(key,notes,point)
        commentTable.close_con()
        return redirect(url_for('commentsListUpdate'))

This code gets the up-to-date values, calls the update_comment function and updates the tuple.

.. code-block:: python
    :linenos:

    elif 'Find' in request.form:
        now = datetime.datetime.now()
        player=request.form['PlayerF']
        notes=request.form['NotesF']
        point=request.form['PointF']
        data=commentTable.find_Joint_Comment(player,notes,point)
        playersTable=players.Players(dsn)
        data2 =playersTable.select_players()
        temp=render_template('comments.html', current_time=now.ctime(),rows=data, update=False,PlayersSelect=data2)
        commentTable.close_con()
        return temp

This code gets the searching criteria, calls the find_Joint_Comment function and finds the requested tuple(s). It also calls select functions of players class and comments class because of the foreign keys.

**updateCommentsList function:**

.. code-block:: python
    :linenos:

    def updateCommentsList(dsn):
    commentTable = comments.Comments(dsn)
    if request.method == 'GET':
        now = datetime.datetime.now()
        data=commentTable.select_Joint_Comment()
        temp=render_template('comments.html', current_time=now.ctime(),rows=data, update=True)
        commentTable.close_con()
        return temp

This code gets the update page when the "click for update" button is pressed and makes the boolean "update" value True.

2.3 Likes Table
---------------
Sql Statements are executed with the functions of the Likes class.

2.3.1 likes.py
++++++++++++++

**__init__ function of Likes class:**

.. code-block:: python
    :linenos:

    def __init__(self, dsn):
        self.connection = dbapi2.connect(dsn)
        self.cursor = self.connection.cursor()

Constructor of the Likes class.

**create_table function of Likes class:**

.. code-block:: python
    :linenos:

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

        self.connection.commit()except dbapi2.DatabaseError:
        self.connection.rollback()


This code first drops Likes table. Then it creates the Likes table and insert initial tuples to the table.


**select_likes function of Likes class:**

.. code-block:: python
    :linenos:

    def select_likes(self):
        statement = """ SELECT * FROM Likes """
        self.cursor.execute(statement)
        return self.cursor

This code lists all the tuples in the Likes table.


**delete_like function of Likes class:**

.. code-block:: python
    :linenos:

    def delete_like(self,Id):
        stement =""" DELETE FROM Likes WHERE ID={}""".format(Id)
        self.cursor.execute(stement)
        self.connection.commit()


This code deletes the tuple which is selected.

**add_like function of Likes class:**

.. code-block:: python
    :linenos:

    def add_like(self, user, player, status):
        if(status.strip()):
            statement = """ INSERT INTO Likes (FK_UsersID,FK_PlayersID, STATUS) VALUES({},{},'{}')""".format(user, player, status)
            self.cursor.execute(statement)
            self.connection.commit()

This code adds a tuple to Likes table.


**update_like function of Likes class:**

.. code-block:: python
    :linenos:

    def update_like(self, Id, status):
        statement = """UPDATE Likes SET STATUS = '{}' WHERE ID = {}""".format( status, Id)
        self.cursor.execute(statement)
        self.connection.commit()


This code updates the attributes of the Likes table.


**select_Joint_Like function of Likes class:**

.. code-block:: python
    :linenos:

    def select_Joint_Like(self):
        statement = """ SELECT Likes.ID,Users.Uname,Players.Name, Likes.STATUS FROM Likes INNER JOIN Users ON Users.ID=Likes.FK_UsersID INNER JOIN Players ON Players.ID=Likes.FK_PlayersID  """
        self.cursor.execute(statement)
        return self.cursor

This code lists all the tuples in Likes table with the foreign key.

**find_Joint_Like function of Likes class:**

.. code-block:: python
    :linenos:

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

This code finds the tuples of Likes table according to the searching criteria with the foreign key.

**close_con function of Likes class:**

.. code-block:: python
    :linenos:

    def close_con(self):
        self.connection.close()

This code closes the connection.




2.3.2 likeslist.py
++++++++++++++++++

**likesList function:**

.. code-block:: python
    :linenos:

    def likesList(dsn):
    likeTable = likes.Likes(dsn)
    if request.method == 'GET':
        now = datetime.datetime.now()
        usersTable=users.Users(dsn)
        data2=usersTable.select_users()
        playersTable=players.Players(dsn)
        data3=playersTable.select_players()
        data=likeTable.select_Joint_Like()
        return render_template('likes.html', current_time=now.ctime(),rows=data, update=False,UsersSelect=data2,PlayersSelect=data3)

This code calls the likes page. This page contains information from users page and players page. So it calls the "select" function of players class and users class and collects the information. Then it calls the select_Joint_Like function and executes the listing.

.. code-block:: python
    :linenos:

    elif 'Delete' in request.form:
        keys = request.form.getlist('movies_to_delete')
        for key in keys:
            likeTable.delete_like(key)
        likeTable.close_con()
        return redirect(url_for('likesList'))

This code gets the key, calls the delete_like function and deletes the selected tuple.

.. code-block:: python
    :linenos:

    elif 'Add' in request.form:
        user=request.form['SelectUserStatus']
        player=request.form['SelectPlayerStatus']
        status=request.form['Status']
        likeTable.add_like(user,player,status)
        likeTable.close_con()
        return redirect(url_for('likesList'))

This code gets the input values, calls the add_like function and adds a tuple.

.. code-block:: python
    :linenos:

    elif 'Update2' in request.form:
        keys = request.form.getlist('movies_to_delete')
        for key in keys:
           status=request.form['Status'+key]
           likeTable.update_like(key,status)
        likeTable.close_con()
        return redirect(url_for('likesListUpdate'))

This code gets the up-to-date values, calls the update_like function and updates the tuple.

.. code-block:: python
    :linenos:

    elif 'Find' in request.form:
        now = datetime.datetime.now()
        user=request.form['UserF']
        player=request.form['PlayerF']
        status=request.form['StatusF']
        data=likeTable.find_Joint_Like(user,player,status)
        usersTable=users.Users(dsn)
        data2 =usersTable.select_users()
        playersTable=players.Players(dsn)
        data3=playersTable.select_players()
        temp=render_template('likes.html', current_time=now.ctime(),rows=data, update=False,UsersSelect=data2,PlayersSelect=data3)
        likeTable.close_con()
        return temp

This code gets the searching criteria, calls the find_Joint_Like function and finds the requested tuple(s). It also calls select function of users and players class because of the foreign key.

**updateLikesList:**

.. code-block:: python
    :linenos:

    def updateLikesList(dsn):
    likeTable = likes.Likes(dsn)
    if request.method == 'GET':
        now = datetime.datetime.now()
        data=likeTable.select_Joint_Like()
        temp=render_template('likes.html', current_time=now.ctime(),rows=data, update=True)
        likeTable.close_con()
        return temp

This code gets the update page when the "click for update" button is pressed and makes the boolean "update" value True.

