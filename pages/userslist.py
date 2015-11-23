
from flask import url_for,redirect,render_template,request
from tables import users
import datetime

def usersList(dsn):
    userTable = users.Users(dsn)
    if request.method == 'GET':
        now = datetime.datetime.now()
        data=userTable.select_users()
        return render_template('users.html', current_time=now.ctime(),rows=data, update=False)
    elif 'Delete' in request.form:
        keys = request.form.getlist('movies_to_delete')
        for key in keys:
            userTable.delete_user(key)
        userTable.close_con()
        return redirect(url_for('usersList'))
    elif 'Add' in request.form:
        uname=request.form['Uname']
        utype=request.form['Utype']
        birth=request.form['Birth']
        userTable.add_user(uname,utype,birth)
        userTable.close_con()
        return redirect(url_for('usersList'))
    elif 'Update2' in request.form:
        keys = request.form.getlist('movies_to_delete')
        for key in keys:
           uname=request.form['Uname'+key]
           utype=request.form['Utype'+key]
           birth=request.form['Birth'+key]
           userTable.update_user(key, uname, utype, birth)
        userTable.close_con()
        return redirect(url_for('usersListUpdate'))
    elif 'Find' in request.form:
        now = datetime.datetime.now()
        uname=request.form['UnameF']
        utype=request.form['UtypeF']
        birth=request.form['BirthF']
        data=userTable.find_Users(uname, utype, birth)
        temp=render_template('users.html', current_time=now.ctime(),rows=data, update=False)
        userTable.close_con()
        return temp

def updateUsersList(dsn):
    userTable = users.Users(dsn)
    if request.method == 'GET':
        now = datetime.datetime.now()
        data=userTable.select_users()
        temp=render_template('users.html', current_time=now.ctime(),rows=data, update=True)
        userTable.close_con()
        return temp



