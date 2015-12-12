from flask import url_for,redirect,render_template,request
from tables import leagues
import datetime


def leaguesList(dsn):
    leagueTable = leagues.Leagues(dsn)
    if request.method == 'GET':
        now = datetime.datetime.now()
        data=leagueTable.select_leagues()
        return render_template('leagues.html', current_time=now.ctime(),rows=data, update=False)
    elif 'Delete' in request.form:
        keys = request.form.getlist('movies_to_delete')
        for key in keys:
            leagueTable.delete_league(key)
        leagueTable.close_con()
        return redirect(url_for('leaguesList'))
    elif 'Add' in request.form:
        name=request.form['Name']
        country=request.form['Country']
        year=request.form['Year']
        leagueTable.add_league(name,country,year)
        leagueTable.close_con()
        return redirect(url_for('leaguesList'))
    elif 'Update2' in request.form:
        keys = request.form.getlist('movies_to_delete')
        for key in keys:
           name=request.form['Name'+key]
           country=request.form['Country'+key]
           year=request.form['Year'+key]
           leagueTable.update_league(key, name, country, year)
        leagueTable.close_con()
        return redirect(url_for('leaguesListUpdate'))
    elif 'Find' in request.form:
        now = datetime.datetime.now()
        name=request.form['NameF']
        country=request.form['CountryF']
        year=request.form['YearF']
        data=leagueTable.find_leagues(name, country, year)
        temp=render_template('leagues.html', current_time=now.ctime(),rows=data, update=False)
        leagueTable.close_con()
        return temp


def updateLeaguesList(dsn):
    leagueTable = leagues.Leagues(dsn)
    if request.method == 'GET':
        now = datetime.datetime.now()
        data=leagueTable.select_leagues()
        temp=render_template('leagues.html', current_time=now.ctime(),rows=data, update=True)
        leagueTable.close_con()
        return temp
