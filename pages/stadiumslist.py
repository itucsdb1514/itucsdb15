
from flask import url_for,redirect,render_template,request
from tables import stadiums

def stadiumsList(dsn):
    fields = stadiums.Stadiums(dsn)
    if request.method == 'GET':
        now = datetime.datetime.now()
        data=fields.select_stadiums()
        return render_template('stadiums.html', current_time=now.ctime())
    elif 'Delete' in request.form:
        keys = request.form.getlist('movies_to_delete')
        for key in keys:
            fields.delete_stadium(key)
        fields.close_con()
        return redirect(url_for('stadiumsList'))
    elif 'Add' in request.form:
        name=request.form['Name']
        city=request.form['City']
        year=request.form['Year']
        fields.add_stadium(name,city,year)
        fields.close_con()
        return redirect(url_for('stadiumsList'))
