from flask import url_for,redirect,render_template,request
from tables import likes,users,players
import datetime


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
    elif 'Delete' in request.form:
        keys = request.form.getlist('movies_to_delete')
        for key in keys:
            likeTable.delete_like(key)
        likeTable.close_con()
        return redirect(url_for('likesList'))
    elif 'Add' in request.form:
        user=request.form['SelectUserStatus']
        player=request.form['SelectPlayerStatus']
        status=request.form['Status']
        likeTable.add_like(user,player,status)
        likeTable.close_con()
        return redirect(url_for('likesList'))
    elif 'Update2' in request.form:
        keys = request.form.getlist('movies_to_delete')
        for key in keys:
           status=request.form['Status'+key]
           likeTable.update_like(key,status)
        likeTable.close_con()
        return redirect(url_for('likesListUpdate'))
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

def updateLikesList(dsn):
    likeTable = likes.Likes(dsn)
    if request.method == 'GET':
        now = datetime.datetime.now()
        data=likeTable.select_Joint_Like()
        temp=render_template('likes.html', current_time=now.ctime(),rows=data, update=True)
        likeTable.close_con()
        return temp