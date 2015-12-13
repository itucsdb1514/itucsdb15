from flask import url_for,redirect,render_template,request
from tables import betrates, matches
import datetime

def betratesList(dsn):
    betrateTable = betrates.Betrates(dsn)
    if request.method == 'GET':
        now = datetime.datetime.now()
        matchesTable = matches.Matches(dsn)
        data2 = matchesTable.select_Joint_Match()
        data=betrateTable.select_Joint_Betrate()
        return render_template('betrates.html', current_time=now.ctime(),rows=data, update = False, MatchesSelect=data2)
    elif 'Delete' in request.form:
        keys = request.form.getlist('movies_to_delete')
        for key in keys:
            betrateTable.delete_betrate(key)
        betrateTable.close_con()
        return redirect(url_for('betratesList'))
    elif 'Add' in request.form:
        match = request.form['SelectMatchOP1']
        home=request.form['Home']
        away=request.form['Away']
        draw=request.form['Draw']
        betrateTable.add_betrate(home,away,draw,match)
        betrateTable.close_con()
        return redirect(url_for('betratesList'))
    elif 'Update2' in request.form:
        keys = request.form.getlist('movies_to_delete')
        for key in keys:
            home=request.form['Home'+key]
            away=request.form['Away'+key]
            draw=request.form['Draw'+key]
            betrateTable.update_betrate(key,home,away, draw)
        betrateTable.close_con()
        return redirect(url_for('betratesListUpdate'))
    elif 'Find' in request.form:
        now = datetime.datetime.now()
        match1=request.form['Match1F']
        match2=request.form['Match2F']
        home=request.form['HomeF']
        away=request.form['AwayF']
        draw = request.form['DrawF']
        data=betrateTable.find_Joint_Betrate(home,away,draw,match1, match2)
        matchesTable=matches.Matches(dsn)
        data2 =matchesTable.select_Joint_Match()
        temp=render_template('betrates.html', current_time=now.ctime(),rows=data, update=False,MatchesSelect=data2)
        betrateTable.close_con()
        return temp

def updateBetratesList(dsn):
    betrateTable = betrates.Betrates(dsn)
    if request.method=='GET':
        now = datetime.datetime.now()
        data=betrateTable.select_Joint_Betrate()
        temp=render_template('betrates.html', current_time=now.ctime(),rows=data,update=True)
        betrateTable.close_con()
        return temp