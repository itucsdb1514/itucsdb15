
from flask import url_for,redirect,render_template,request
from tables import players
import datetime

def playersList(dsn):
    playerTable = players.Players(dsn)
    if request.method == 'GET':
        now = datetime.datetime.now()
        data=playerTable.select_players()
        return render_template('players.html', current_time=now.ctime(),rows=data)
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