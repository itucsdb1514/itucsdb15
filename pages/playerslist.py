
from flask import url_for,redirect,render_template,request
from tables import players
import datetime

def playersList(dsn):
    playerTable = players.Players(dsn)
    if request.method == 'GET':
        now = datetime.datetime.now()
        data=playerTable.select_players()
        return render_template('players.html', current_time=now.ctime(),rows=data, update=False)
    elif 'Delete' in request.form:
        keys = request.form.getlist('movies_to_delete')
        for key in keys:
            playerTable.delete_player(key)
        playerTable.close_con()
        return redirect(url_for('playersList'))
    elif 'Add' in request.form:
        name=request.form['Name']
        country=request.form['Country']
        age=request.form['Age']
        playerTable.add_player(name,country,age)
        playerTable.close_con()
        return redirect(url_for('playersList'))
    elif 'Update2' in request.form:
        keys = request.form.getlist('movies_to_delete')
        for key in keys:
           name=request.form['Name'+key]
           country=request.form['Country'+key]
           age=request.form['Age'+key]
           playerTable.update_player(key, name, country, age)
        playerTable.close_con()
        return redirect(url_for('playersListUpdate'))
    elif 'Find' in request.form:
        now = datetime.datetime.now()
        name=request.form['NameF']
        country=request.form['CountryF']
        age=request.form['AgeF']
        data=playerTable.find_Players(name, country, age)
        temp=render_template('players.html', current_time=now.ctime(),rows=data, update=False)
        playerTable.close_con()
        return temp

def updatePlayersList(dsn):
    playerTable = players.Players(dsn)
    if request.method == 'GET':
        now = datetime.datetime.now()
        data=playerTable.select_players()
        temp=render_template('players.html', current_time=now.ctime(),rows=data, update=True)
        playerTable.close_con()
        return temp



