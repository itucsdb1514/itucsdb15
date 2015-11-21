
from flask import url_for,redirect,render_template,request
from tables import stadiums
import datetime

def stadiumsList(dsn):
    stadiumTable = stadiums.Stadiums(dsn)
    if request.method == 'GET':
        now = datetime.datetime.now()
        data=stadiumTable.select_stadiums()
        return render_template('stadiums.html', current_time=now.ctime(),rows=data)
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