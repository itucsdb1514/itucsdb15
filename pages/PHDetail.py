from flask import url_for,redirect,render_template,request
from tables import playerHistory,players,teams
import datetime

def PHDetail(dsn,id):
    playerH=playerHistory.playerHistory(dsn)
    if request.method == 'GET':
        now = datetime.datetime.now()
        datas= playerH.Select_PlayersHisory(id);
        ps=players.Players(dsn)
        ts=teams.Teams(dsn)
        tDatas=ts.select_teams()
        pDatas=ps.select_players()
        page= render_template('PHDetails.html', current_time=now.ctime(),
                              rows=datas, update = False,historyID=id,PlayerSelect=pDatas,TeamSelect=tDatas)
        playerH.close_con();
        return page
    elif 'Delete' in request.form:
        keys = request.form.getlist('movies_to_delete')
        for key in keys:
            playerH.delete_History(key)
        playerH.close_con()
        return redirect(url_for('playerHistory',id=id))
    elif 'Add' in request.form:
        playerID=request.form['Player']
        teamID=request.form['Team']
        start=request.form['start']
        end=request.form['end']
        try:
            playerH.add_History(playerID,teamID,start,end)
        except dbapi2.DatabaseError:
            pass

        playerH.close_con()
        return redirect(url_for('playerHistory',id=id))