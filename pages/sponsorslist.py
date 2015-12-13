
from flask import url_for,redirect,render_template,request
from tables import sponsors,teams
import datetime

def sponsorsList(dsn):
    sponsorTable = sponsors.Sponsors(dsn)
    if request.method == 'GET':
        now = datetime.datetime.now()
        data=sponsorTable.select_sponsors()
        ts=teams.Teams(dsn)
        tDatas=ts.select_teams()
        return render_template('sponsors.html', current_time=now.ctime(),rows=data,
                               TeamSelect=tDatas,)
    elif 'Delete' in request.form:
        keys = request.form.getlist('movies_to_delete')
        for key in keys:
            sponsorTable.delete_sponsor(key)
        sponsorTable.close_con()
        return redirect(url_for('sponsorsList'))
    elif 'Add' in request.form:
        name=request.form['Name']
        country=request.form['Country']
        team=request.form['Team']
        sponsorTable.add_sponsor(name,country,team)
        sponsorTable.close_con()
        return redirect(url_for('sponsorsList'))
    elif'Find' in request.form:
        name=request.form['FName']
        country=request.form['FCountry']
        team=request.form['FTeam']
        ts=teams.Teams(dsn)
        now = datetime.datetime.now()
        tDatas=ts.select_teams()
        data=sponsorTable.Find_sponsors(name,country,team)
        return render_template('sponsors.html', current_time=now.ctime(),rows=data,TeamSelect=tDatas)