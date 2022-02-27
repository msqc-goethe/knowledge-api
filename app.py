from flask import Flask
import sqlite3
from flask import g
import json
from flask import request

app = Flask(__name__)

DATABASE = "../pythonProject1/pythonsqlite.db"


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.route('/')
def hello_world():  # put application's code here
    cur = get_db().cursor()
    query = cur.execute("SELECT * FROM performances")
    colname = [d[0] for d in query.description]
    result_list = [ dict(zip(colname, r)) for r in query.fetchall() ]
    cur.close()
    cur.connection.close()
    return json.dumps(result_list)


@app.route('/performances')
def get_performances():  # put application's code here
    cur = get_db().cursor()
    query = cur.execute("SELECT * FROM performances")
    colname = [d[0] for d in query.description]
    result_list = [ dict(zip(colname, r)) for r in query.fetchall() ]
    cur.close()
    cur.connection.close()
    return json.dumps(result_list)


@app.route('/summaries/', methods=['GET', 'POST'])
def get_summaries():  # put application's code here
    cur = get_db().cursor()
    id = request.args.get('id')
    query = cur.execute("SELECT * FROM summaries WHERE performance_id = ?", id)
    colname = [d[0] for d in query.description]
    result_list = [dict(zip(colname, r)) for r in query.fetchall()]
    cur.close()
    cur.connection.close()
    return json.dumps(result_list)


@app.route('/results/', methods=['GET', 'POST'])
def get_results():  # put application's code here
    cur = get_db().cursor()
    summary_id = request.args.get('summary_id')
    # access = request.args.get('access')
    # query = cur.execute("SELECT * FROM results WHERE summary_id = ? AND  access = ?", id, access)
    query = cur.execute("SELECT * FROM results WHERE summary_id = ?", summary_id)
    colname = [d[0] for d in query.description]
    result_list = [dict(zip(colname, r)) for r in query.fetchall()]
    cur.close()
    cur.connection.close()
    return json.dumps(result_list)


if __name__ == '__main__':
    app.run()
