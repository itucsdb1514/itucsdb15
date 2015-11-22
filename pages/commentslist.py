
from flask import url_for,redirect,render_template,request
from tables import comments,players
import datetime

def commentsList(dsn):
    commentTable = comments.Comments(dsn)
    if request.method == 'GET':
        now = datetime.datetime.now()
        playersTable=players.Players(dsn)
        data2 =playersTable.select_players()
        data=commentTable.select_Joint_Comment()
        return render_template('comments.html', current_time=now.ctime(),rows=data, update=False,PlayersSelect=data2)
    elif 'Delete' in request.form:
        keys = request.form.getlist('movies_to_delete')
        for key in keys:
            commentTable.delete_comment(key)
        commentTable.close_con()
        return redirect(url_for('commentsList'))
    elif 'Add' in request.form:
        player=request.form['SelectPlayerName']
        notes=request.form['Notes']
        point=request.form['Point']
        commentTable.add_comment(player,notes,point)
        commentTable.close_con()
        return redirect(url_for('commentsList'))
    elif 'Update2' in request.form:
        keys = request.form.getlist('movies_to_delete')
        for key in keys:
           notes=request.form['Notes'+key]
           point=request.form['Point'+key]
           commentTable.update_comment(key,notes,point)
        commentTable.close_con()
        return redirect(url_for('commentsListUpdate'))
    elif 'Find' in request.form:
        now = datetime.datetime.now()
        player=request.form['PlayerF']
        notes=request.form['NotesF']
        point=request.form['PointF']
        data=commentTable.find_Joint_Comment(player,notes,point)
        playersTable=players.Players(dsn)
        data2 =playersTable.select_players()
        temp=render_template('comments.html', current_time=now.ctime(),rows=data, update=False,PlayersSelect=data2)
        commentTable.close_con()
        return temp

def updateCommentsList(dsn):
    commentTable = comments.Comments(dsn)
    if request.method == 'GET':
        now = datetime.datetime.now()
        data=commentTable.select_Joint_Comment()
        temp=render_template('comments.html', current_time=now.ctime(),rows=data, update=True)
        commentTable.close_con()
        return temp
