from flask import render_template
import datetime

def HomePageFunc():
    now = datetime.datetime.now()
    return render_template('home.html', current_time=now.ctime())