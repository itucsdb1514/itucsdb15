import datetime
import json
import os
import re

from flask import Flask
from flask import render_template
from pages import HomePage,initPage,sponsorslist

app = Flask(__name__)


@app.route('/')
def home():
    return HomePage.HomePageFunc()

@app.route('/initDB')
def InitDb():
    return initPage.InitPageFunc(app.config['dsn'])

@app.route('/sponsorsList', methods=['GET', 'POST'])
def sponsorsList():
    now = datetime.datetime.now()
    return render_template('sponsors.html', current_time=now.ctime())
    #return sponsorslist.sponsorsList(app.config['dsn'])

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
