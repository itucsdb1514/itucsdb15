
from flask import url_for,redirect,render_template,request
from tables import sponsors
import datetime

def sponsorsList(dsn):
    sponsorTable = sponsors.Sponsors(dsn)
    if request.method == 'GET':
        now = datetime.datetime.now()
        data=sponsorTable.select_sponsors()
        return render_template('sponsors.html', current_time=now.ctime(),rows=data)
    elif 'Delete' in request.form:
        keys = request.form.getlist('movies_to_delete')
        for key in keys:
            sponsorTable.delete_sponsor(key)
        sponsorTable.close_con()
        return redirect(url_for('sponsorsList'))
    elif 'Add' in request.form:
        name=request.form['Name']
        country=request.form['Country']
        age=request.form['Count']
        sponsorTable.add_sponsor(name,country,age)
        sponsorTable.close_con()
        return redirect(url_for('sponsorsList'))
