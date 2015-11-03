
from flask import url_for,redirect,render_template,request
from tables import comments

def commentsList(dsn):
    companies = comments.Comments(dsn)
    if request.method == 'GET':
        now = datetime.datetime.now()
        data=companies.select_comments()
        return render_template('comments.html', current_time=now.ctime())
    elif 'Delete' in request.form:
        keys = request.form.getlist('movies_to_delete')
        for key in keys:
            companies.delete_comment(key)
        companies.close_con()
        return redirect(url_for('commentsList'))
    elif 'Add' in request.form:
        player=request.form['Player']
        notes=request.form['Notes']
        point=request.form['Point']
        companies.add_comment(player,notes,point)
        companies.close_con()
        return redirect(url_for('commentsList'))
