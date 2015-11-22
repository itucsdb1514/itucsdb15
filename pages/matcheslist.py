from flask import url_for,redirect,render_template,request
from tables import matches, stadiums
import datetime

def matchesList(dsn):
    matchTable = matches.Matches(dsn)
    if request.method == 'GET':
        now = datetime.datetime.now()
        stadiumsTable = stadiums.Stadiums(dsn)
        data2 = stadiumsTable.select_stadiums()
        data=matchTable.select_Joint_Match()
        return render_template('matches.html', current_time=now.ctime(),rows=data, update = False, StadiumsSelect=data2)
    elif 'Delete' in request.form:
        keys = request.form.getlist('movies_to_delete')
        for key in keys:
            matchTable.delete_match(key)
        matchTable.close_con()
        return redirect(url_for('matchesList'))
    elif 'Add' in request.form:
        stadium = request.form['SelectStadiumName']
        op1=request.form['OP1']
        op2=request.form['OP2']
        year=request.form['Year']
        matchTable.add_match(op1,op2,year,stadium)
        matchTable.close_con()
        return redirect(url_for('matchesList'))
    elif 'Update2' in request.form:
        keys = request.form.getlist('movies_to_delete')
        for key in keys:
            op1=request.form['OP1'+key]
            op2=request.form['OP2'+key]
            
            matchTable.update_match(key,op1,op2)
        matchTable.close_con()
        return redirect(url_for('matchesListUpdate'))
    elif 'Find' in request.form:
        now = datetime.datetime.now()
        stadium=request.form['StadiumF']
        op1=request.form['OP1F']
        op2=request.form['OP2F']
        year = request.form['YearF']
        data=matchTable.find_Joint_Match(op1,op2,year,stadium)
        stadiumsTable=stadiums.Stadiums(dsn)
        data2 =stadiumsTable.select_stadiums()
        temp=render_template('matches.html', current_time=now.ctime(),rows=data, update=False,StadiumsSelect=data2)
        matchTable.close_con()
        return temp

def updateMatchesList(dsn):
    matchTable = matches.Matches(dsn)
    if request.method=='GET':
        now = datetime.datetime.now()
        data=matchTable.select_Joint_Match()
        temp=render_template('matches.html', current_time=now.ctime(),rows=data,update=True)
        matchTable.close_con()
        return temp