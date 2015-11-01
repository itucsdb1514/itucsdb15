import datetime
import json
import os
import re

from flask import Flask
from flask import render_template


app = Flask(__name__)


@app.route('/')
def home_page():
    now = datetime.datetime.now()
    return render_template('home.html', current_time=now.ctime())

def get_sqldb_dsn(vcap_services):
    """Returns the data source name for IBM SQL DB."""
    parsed = json.loads(vcap_services)
    credentials = parsed["sqldb"][0]["credentials"]
    user = credentials["username"]
    password = credentials["password"]
    host = credentials["hostname"]
    port = credentials["port"]
    dbname = credentials["db"]
    dsn = """DATABASE={};HOSTNAME={};PORT={};UID={};PWD={};""".format(dbname, host, port, user, password)
    return dsn


if __name__ == '__main__':
    VCAP_APP_PORT = os.getenv('VCAP_APP_PORT')
    if VCAP_APP_PORT is not None:
        port, debug = int(VCAP_APP_PORT), False
    else:
        port, debug = 5000, True
    VCAP_SERVICES = os.getenv('VCAP_SERVICES')
    if VCAP_SERVICES is not None:
        app.config['dsn'] = get_sqldb_dsn(VCAP_SERVICES)
    else:
        app.config['dsn'] = """DATABASE=itucsdb;HOSTNAME=localhost;PORT=50000;UID=vagrant;PWD=vagrant;"""

    app.run(host='0.0.0.0', port=port, debug=debug)
