
from flask import url_for,redirect,render_template,request
from tables import teams


def teamsList(dsn):
    takımlar = teams.Teams(dsn)
    if request.method == 'GET':
        now = datetime.datetime.now()
        data=takımlar.select_teams()
        return render_template('teams.html', current_time=now.ctime())
    elif 'Delete' in request.form:
        keys = request.form.getlist('movies_to_delete')
        for key in keys:
            takımlar.delete_team(key)
        takımlar.close_con()
        return redirect(url_for('teamsList'))
    elif 'Add' in request.form:
        name=request.form['Name']
        country=request.form['Country']
        year=request.form['Year']
        takımlar.add_team(name,country,year)
        takımlar.close_con()
        return redirect(url_for('teamsList'))
