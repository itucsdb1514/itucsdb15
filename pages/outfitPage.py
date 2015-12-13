from flask import url_for,redirect,render_template,request
from tables import outfitTable,teams
import datetime

def outfitPage(dsn,id):
    outfits=outfitTable.outfits(dsn)
    if request.method == 'GET':
        now = datetime.datetime.now()
        datas= outfits.select_outfits(id);
        ts=teams.Teams(dsn)
        tDatas=ts.select_teams()
        page= render_template('outfit.html', current_time=now.ctime(),
                              rows=datas, update = False,TeamID=id,
                              teamSelect=tDatas,
                              )
        outfits.close_con();
        return page
    elif 'Add' in request.form:
        teamID=request.form['Team']
        link=request.form['Link']

        outfits.add_outfits(teamID,link)

        outfits.close_con()
        return redirect(url_for('outfitpage',id=id))
    elif 'Delete' in request.form:
        keys = request.form.getlist('movies_to_delete')
        for key in keys:
            outfits.delete_outfits(key)
        outfits.close_con()
        return redirect(url_for('outfitpage',id=id))
    elif 'Update' in request.form:
        keys = request.form.getlist('movies_to_delete')
        for key in keys:
           link=request.form['ULink'+key]
           outfits.update_outfits(link,key)
        outfits.close_con()
        return redirect(url_for('outfitpage',id=id))
def outfitPageUpdate(dsn,id):
    outfits=outfitTable.outfits(dsn)
    if request.method == 'GET':
        now = datetime.datetime.now()
        datas= outfits.select_outfits(id);
        ts=teams.Teams(dsn)
        tDatas=ts.select_teams()
        page= render_template('outfit.html', current_time=now.ctime(),
                              rows=datas, update = True,TeamID=id,
                              teamSelect=tDatas,
                              )
        outfits.close_con();
        return page