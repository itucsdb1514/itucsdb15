
from flask import url_for,redirect,render_template,request
from tables import stats, teams
import datetime

def statsList(dsn):
    statTable = stats.Stats(dsn)
    if request.method == 'GET':
        now = datetime.datetime.now()
        teamsTable=teams.Teams(dsn)
        data2 =teamsTable.select_teams()
        data=statTable.select_Joint_Stat()
        return render_template('stats.html', current_time=now.ctime(),rows=data, update=False,TeamsSelect=data2)
    elif 'Delete' in request.form:
        keys = request.form.getlist('movies_to_delete')
        for key in keys:
            statTable.delete_stat(key)
        statTable.close_con()
        return redirect(url_for('statsList'))
    elif 'Add' in request.form:
        team=request.form['SelectTeamName']
        player=request.form['Player']
        stat=request.form['Stat']
        statTable.add_stat(team, stat, player)
        statTable.close_con()
        return redirect(url_for('statsList'))
    elif 'Update2' in request.form:
        keys = request.form.getlist('movies_to_delete')
        for key in keys:
           stat=request.form['Stat'+key]
           statTable.update_stat(key,stat)
        statTable.close_con()
        return redirect(url_for('statsListUpdate'))
    elif 'Find' in request.form:
        now = datetime.datetime.now()
        team=request.form['TeamF']
        player=request.form['PlayerF']
        stat=request.form['StatF']
        data=statTable.find_Joint_Stat(team,stat, player)
        teamsTable=teams.Teams(dsn)
        data2 =teamsTable.select_teams()
        temp=render_template('stats.html', current_time=now.ctime(),rows=data, update=False,TeamsSelect=data2)
        statTable.close_con()
        return temp

def updateStatsList(dsn):
    statTable = stats.Stats(dsn)
    if request.method == 'GET':
        now = datetime.datetime.now()
        data=statTable.select_Joint_Stat()
        temp=render_template('stats.html', current_time=now.ctime(),rows=data, update=True)
        statTable.close_con()
        return temp







