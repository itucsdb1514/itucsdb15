
from flask import url_for,redirect,render_template,request
from tables import teams
import datetime


def teamsList(dsn):
    teamTable = teams.Teams(dsn)
    if request.method == 'GET':
        now = datetime.datetime.now()
        data=teamTable.select_teams()
        return render_template('teams.html', current_time=now.ctime(),rows=data)
    elif 'Delete' in request.form:
        keys = request.form.getlist('movies_to_delete')
        for key in keys:
            teamTable.delete_team(key)
        teamTable.close_con()
        return redirect(url_for('teamsList'))
    elif 'Add' in request.form:
        name=request.form['Name']
        country=request.form['Country']
        year=request.form['Year']
        teamTable.add_team(name,country,year)
        teamTable.close_con()
        return redirect(url_for('teamsList'))
