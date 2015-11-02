
from flask import url_for,redirect,render_template,request
from tables import players

def playersList(dsn):
    companies = players.Players(dsn)
    if request.method == 'GET':
        now = datetime.datetime.now()
        data=companies.select_players()
        return render_template('players.html', current_time=now.ctime())
    elif 'Delete' in request.form:
        keys = request.form.getlist('movies_to_delete')
        for key in keys:
            companies.delete_player(key)
        companies.close_con()
        return redirect(url_for('playersList'))
    elif 'Add' in request.form:
        name=request.form['Name']
        country=request.form['Country']
        age=request.form['Count']
        companies.add_player(name,country,age)
        companies.close_con()
        return redirect(url_for('playersList'))
