
from flask import url_for,redirect,render_template,request
from tables import teams
import datetime


def teamsList(dsn):
    teamTable = teams.Teams(dsn)
    if request.method == 'GET':
        now = datetime.datetime.now()
        data=teamTable.select_teams()
        return render_template('teams.html', current_time=now.ctime(),rows=data, update=False)
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
    elif 'Update2' in request.form:
        keys = request.form.getlist('movies_to_delete')
        for key in keys:
           name=request.form['Name'+key]
           country=request.form['Country'+key]
           year=request.form['Year'+key]
           teamTable.update_team(key, name, country, year)
        teamTable.close_con()
        return redirect(url_for('teamsListUpdate'))
    elif 'Find' in request.form:
        now = datetime.datetime.now()
        name=request.form['NameF']
        country=request.form['CountryF']
        year=request.form['YearF']
        data=teamTable.find_teams(name, country, year)
        temp=render_template('teams.html', current_time=now.ctime(),rows=data, update=False)
        teamTable.close_con()
        return temp


def updateTeamsList(dsn):
    teamTable = teams.Teams(dsn)
    if request.method == 'GET':
        now = datetime.datetime.now()
        data=teamTable.select_teams()
        temp=render_template('teams.html', current_time=now.ctime(),rows=data, update=True)
        teamTable.close_con()
        return temp





