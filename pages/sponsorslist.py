
from flask import url_for,redirect,render_template,request
from tables import sponsors

def sponsorsList(dsn):
    companies = sponsors.Sponsors(dsn)
    if request.method == 'GET':
        now = datetime.datetime.now()
        data=companies.select_sponsors()
        return render_template('sponsors.html', current_time=now.ctime())
    elif 'Delete' in request.form:
        keys = request.form.getlist('movies_to_delete')
        for key in keys:
            companies.delete_sponsor(key)
        companies.close_con()
        return redirect(url_for('sponsorsList'))
    elif 'Add' in request.form:
        name=request.form['Name']
        country=request.form['Country']
        age=request.form['Count']
        companies.add_sponsor(name,country,age)
        companies.close_con()
        return redirect(url_for('sponsorsList'))
