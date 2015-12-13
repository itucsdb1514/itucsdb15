from flask import url_for,redirect,render_template,request
from tables import leagues,teams
import datetime


def leaguesList(dsn):
    leagueTable = leagues.Leagues(dsn)
    if request.method == 'GET':
        now = datetime.datetime.now()
        teamsTable=teams.Teams(dsn)
        data2=teamsTable.select_teams()
        data=leagueTable.select_Joint_League()
        return render_template('leagues.html', current_time=now.ctime(),rows=data, update=False,TeamsSelect=data2)
    elif 'Delete' in request.form:
        keys = request.form.getlist('movies_to_delete')
        for key in keys:
            leagueTable.delete_league(key)
        leagueTable.close_con()
        return redirect(url_for('leaguesList'))
    elif 'Add' in request.form:
        team=request.form['SelectTeamName']
        name=request.form['Name']
        country=request.form['Country']
        year=request.form['Year']
        leagueTable.add_league(team,name,country,year)
        leagueTable.close_con()
        return redirect(url_for('leaguesList'))
    elif 'Update2' in request.form:
        keys = request.form.getlist('movies_to_delete')
        for key in keys:
           name=request.form['Name'+key]
           country=request.form['Country'+key]
           year=request.form['Year'+key]
           leagueTable.update_league(key,name,country,year)
        leagueTable.close_con()
        return redirect(url_for('leaguesListUpdate'))
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

def updateLeaguesList(dsn):
    leagueTable = leagues.Leagues(dsn)
    if request.method == 'GET':
        now = datetime.datetime.now()
        data=leagueTable.select_Joint_League()
        temp=render_template('leagues.html', current_time=now.ctime(),rows=data, update=True)
        leagueTable.close_con()
        return temp