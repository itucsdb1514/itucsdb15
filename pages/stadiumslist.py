
from flask import url_for,redirect,render_template,request
from tables import stadiums
import datetime

def stadiumsList(dsn):
    stadiumTable = stadiums.Stadiums(dsn)
    if request.method == 'GET':
        now = datetime.datetime.now()
        data=stadiumTable.select_stadiums()
        return render_template('stadiums.html', current_time=now.ctime(),rows=data, update=False)
    elif 'Delete' in request.form:
        keys = request.form.getlist('movies_to_delete')
        for key in keys:
            stadiumTable.delete_stadium(key)
        stadiumTable.close_con()
        return redirect(url_for('stadiumsList'))
    elif 'Add' in request.form:
        name=request.form['Name']
        city=request.form['City']
        year=request.form['Year']
        stadiumTable.add_stadium(name,city,year)
        stadiumTable.close_con()
        return redirect(url_for('stadiumsList'))
    elif 'Update2' in request.form:
        keys = request.form.getlist('movies_to_delete')
        for key in keys:
           name=request.form['Name'+key]
           city=request.form['City'+key]
           year=request.form['Year'+key]
           stadiumTable.update_stadium(key, name, city, year)
        stadiumTable.close_con()
        return redirect(url_for('stadiumsListUpdate'))
    elif 'Find' in request.form:
        now = datetime.datetime.now()
        name=request.form['NameF']
        city=request.form['CityF']
        year=request.form['YearF']
        data=stadiumTable.find_Stadiums(name, city, year)
        temp=render_template('stadiums.html', current_time=now.ctime(),rows=data, update=False)
        stadiumTable.close_con()
        return temp

def updateStadiumsList(dsn):
    stadiumTable = stadiums.Stadiums(dsn)
    if request.method == 'GET':
        now = datetime.datetime.now()
        data=stadiumTable.select_stadiums()
        temp=render_template('stadiums.html', current_time=now.ctime(),rows=data, update=True)
        stadiumTable.close_con()
        return temp