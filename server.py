import datetime
import json
import os
import re

from flask import Flask
from flask import render_template,request,url_for,redirect
from pages import HomePage,initPage,sponsorslist, playerslist, teamslist, stadiumslist, commentslist
from tables import sponsors
from tables import players
from tables import teams
from tables import stadiums
from tables import comments

app = Flask(__name__)


@app.route('/')
def home():
    return HomePage.HomePageFunc()

@app.route('/initDB')
def InitDb():
    return initPage.InitPageFunc(app.config['dsn'])

@app.route('/sponsorsList', methods=['GET', 'POST'])
def sponsorsList():
    dsn=app.config['dsn']
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

@app.route('/stadiumsList', methods=['GET', 'POST'])
def stadiumsList():
    dsn=app.config['dsn']
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

@app.route('/playersList', methods=['GET', 'POST'])
def playersList():
    dsn=app.config['dsn']
    playerTable = players.Players(dsn)
    if request.method == 'GET':
        now = datetime.datetime.now()
        data=playerTable.select_players()
        return render_template('players.html', current_time=now.ctime(),rows=data)
    elif 'Delete' in request.form:
        keys = request.form.getlist('movies_to_delete')
        for key in keys:
            playerTable.delete_player(key)
        playerTable.close_con()
        return redirect(url_for('playersList'))
    elif 'Add' in request.form:
        name=request.form['Name']
        country=request.form['Country']
        age=request.form['Age']
        playerTable.add_player(name,country,age)
        playerTable.close_con()
        return redirect(url_for('playersList'))

@app.route('/teamsList', methods=['GET', 'POST'])
def teamsList():
    dsn=app.config['dsn']
    teamTable = teams.Teams(dsn)
    if request.method == 'GET':
        now = datetime.datetime.now()
        data=teamTable.select_teams()
        return render_template('teams.html', current_time=now.ctime(),rows=data)
    elif 'Delete' in request.form:
        keys = request.form.getlist('movies_to_delete')
        for key in keys:
            teamTable.delete_team(key)
        teamTable.close_con()
        return redirect(url_for('teamsList'))
    elif 'Add' in request.form:
        name=request.form['Name']
        country=request.form['Country']
        year=request.form['Year']
        teamTable.add_team(name,country,year)
        teamTable.close_con()
        return redirect(url_for('teamsList'))

@app.route('/commentsList', methods=['GET', 'POST'])
def commentsList():
    dsn=app.config['dsn']
    commentTable = comments.Comments(dsn)
    if request.method == 'GET':
        now = datetime.datetime.now()
        data=commentTable.select_comments()
        return render_template('comments.html', current_time=now.ctime(),rows=data)
    elif 'Delete' in request.form:
        keys = request.form.getlist('movies_to_delete')
        for key in keys:
            commentTable.delete_comment(key)
        commentTable.close_con()
        return redirect(url_for('commentsList'))
    elif 'Add' in request.form:
        player=request.form['Player']
        notes=request.form['Notes']
        point=request.form['Point']
        commentTable.add_comment(player,notes,point)
        commentTable.close_con()
        return redirect(url_for('commentsList'))



def get_elephantsql_dsn(vcap_services):
    parsed = json.loads(vcap_services)
    uri = parsed["elephantsql"][0]["credentials"]["uri"]
    match = re.match('postgres://(.*?):(.*?)@(.*?)(:(\d+))?/(.*)', uri)
    user, password, host, _, port, dbname = match.groups()
    dsn = """user='{}' password='{}' host='{}' port={}
    dbname='{}'""".format(user, password, host, port, dbname)
    return dsn

if __name__ == '__main__':
    VCAP_APP_PORT = os.getenv('VCAP_APP_PORT')
    if VCAP_APP_PORT is not None:
        port, debug = int(VCAP_APP_PORT), False
    else:
        port, debug = 5000, True
    VCAP_SERVICES = os.getenv('VCAP_SERVICES')
    if VCAP_SERVICES is not None:
        app.config['dsn'] = get_elephantsql_dsn(VCAP_SERVICES)
    else:
        app.config['dsn'] =  """host='localhost' port=54321  password='vagrant' user='vagrant' dbname='itucsdb'"""
    app.run(host='0.0.0.0', port=port, debug=debug)
