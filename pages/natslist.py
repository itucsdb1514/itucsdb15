
from flask import url_for,redirect,render_template,request
from tables import nats, players
import datetime

def natsList(dsn):
    natTable = nats.Nats(dsn)
    if request.method == 'GET':
        now = datetime.datetime.now()
        playersTable=players.Players(dsn)
        data2 =playersTable.select_players()
        data=natTable.select_Joint_Nat()
        return render_template('nats.html', current_time=now.ctime(),rows=data, update=False,PlayersSelect=data2)
    elif 'Delete' in request.form:
        keys = request.form.getlist('movies_to_delete')
        for key in keys:
            natTable.delete_nat(key)
        natTable.close_con()
        return redirect(url_for('natsList'))
    elif 'Add' in request.form:
        player=request.form['SelectPlayerName']
        nat=request.form['Nat']
        natTable.add_nat(player, nat)
        natTable.close_con()
        return redirect(url_for('natsList'))
    elif 'Update2' in request.form:
        keys = request.form.getlist('movies_to_delete')
        for key in keys:
           nat=request.form['Nat'+key]
           natTable.update_nat(key,nat)
        natTable.close_con()
        return redirect(url_for('natsListUpdate'))
    elif 'Find' in request.form:
        now = datetime.datetime.now()
        player=request.form['PlayerF']
        nat=request.form['NatF']
        data=natTable.find_Joint_Nat(player,nat)
        playersTable=players.Players(dsn)
        data2 =playersTable.select_players()
        temp=render_template('nats.html', current_time=now.ctime(),rows=data, update=False,PlayersSelect=data2)
        natTable.close_con()
        return temp

def updateNatsList(dsn):
    natTable = nats.Nats(dsn)
    if request.method == 'GET':
        now = datetime.datetime.now()
        data=natTable.select_Joint_Nat()
        temp=render_template('nats.html', current_time=now.ctime(),rows=data, update=True)
        natTable.close_con()
        return temp







