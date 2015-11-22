from flask import url_for,redirect,render_template,request
from tables import coaches,teams
import datetime


def coachesList(dsn):
    coachTable = coaches.Coaches(dsn)
    if request.method == 'GET':
        now = datetime.datetime.now()
        teamsTable=teams.Teams(dsn)
        data2=teamsTable.select_teams()
        data=coachTable.select_Joint_Coach()
        return render_template('coaches.html', current_time=now.ctime(),rows=data, update=False,TeamsSelect=data2)
    elif 'Delete' in request.form:
        keys = request.form.getlist('movies_to_delete')
        for key in keys:
            coachTable.delete_coach(key)
        coachTable.close_con()
        return redirect(url_for('coachesList'))
    elif 'Add' in request.form:
        team=request.form['SelectTeamName']
        name=request.form['Name']
        country=request.form['Country']
        age=request.form['Age']
        coachTable.add_coach(team,name,country,age)
        coachTable.close_con()
        return redirect(url_for('coachesList'))
    elif 'Update2' in request.form:
        keys = request.form.getlist('movies_to_delete')
        for key in keys:
           name=request.form['Name'+key]
           country=request.form['Country'+key]
           age=request.form['Age'+key]
           coachTable.update_coach(key,name,country,age)
        coachTable.close_con()
        return redirect(url_for('coachesListUpdate'))
    elif 'Find' in request.form:
        now = datetime.datetime.now()
        team=request.form['TeamF']
        name=request.form['NameF']
        country=request.form['CountryF']
        age=request.form['AgeF']
        data=coachTable.find_Joint_Coach(team,name,country,age)
        teamsTable=teams.Teams(dsn)
        data2 =teamsTable.select_teams()
        temp=render_template('coaches.html', current_time=now.ctime(),rows=data, update=False,TeamsSelect=data2)
        coachTable.close_con()
        return temp

def updateCoachesList(dsn):
    coachTable = coaches.Coaches(dsn)
    if request.method == 'GET':
        now = datetime.datetime.now()
        data=coachTable.select_Joint_Coach()
        temp=render_template('coaches.html', current_time=now.ctime(),rows=data, update=True)
        coachTable.close_con()
        return temp





