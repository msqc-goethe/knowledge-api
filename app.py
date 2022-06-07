from flask import Flask
import sqlite3
from flask import g
import json
from flask import request

app = Flask(__name__)


#DATABASE = "../pythonProject1/pythonsqlite.db"

#current Databasepath
DATABASE = "../IORExtractor/pythonsqlite.db"


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


#Seems like dummy code which can be copy and pasted
@app.route('/')
def hello_world():  # put application's code here
    cur = get_db().cursor()
    query = cur.execute("SELECT * FROM performances")
    colname = [d[0] for d in query.description]
    result_list = [ dict(zip(colname, r)) for r in query.fetchall() ]
    cur.close()
    cur.connection.close()
    return json.dumps(result_list)

#sets the route performances and selects every row from performances
@app.route('/performances')
def get_performances():  # put application's code here
    cur = get_db().cursor()
    query = cur.execute("SELECT * FROM performances")
    colname = [d[0] for d in query.description]
    result_list = [ dict(zip(colname, r)) for r in query.fetchall() ]
    cur.close()
    cur.connection.close()
    return json.dumps(result_list)


#sets filesystem route
#selects filesystem where the performance id is equal to the given performance id
@app.route('/filesystems/', methods=['GET', 'POST'])
def get_filesystem():
    cur = get_db().cursor()
    performance_id = request.args.get('id')
    sql = "SELECT * FROM filesystems WHERE performance_id ="+ performance_id
    query = cur.execute(sql)
    colname = [d[0] for d in query.description]
    result_list = [dict(zip(colname, r)) for r in query.fetchall()]
    cur.close()
    cur.connection.close()
    return json.dumps(result_list)

#sets the summaries route
#selects summaries where the perfromance id is equal to the given performance id
@app.route('/summaries/', methods=['GET', 'POST'])
def get_summaries():  # put application's code here
    cur = get_db().cursor()
    id = request.args.get('id')
    sql = "SELECT * FROM summaries WHERE performance_id ="+ id
    query = cur.execute(sql)
    colname = [d[0] for d in query.description]
    result_list = [dict(zip(colname, r)) for r in query.fetchall()]
    cur.close()
    cur.connection.close()
    return json.dumps(result_list)

#add comments here
@app.route('/summaries/multi', methods=['GET', 'POST'])
def get_multi_summaries():  # put application's code here
    cur = get_db().cursor()
    ids = request.args.get('ids')
    # print(ids)
    sql = " SELECT * FROM summaries WHERE performance_id in (" + ids +")"
    print(sql)
    query = cur.execute(sql)
    colname = [d[0] for d in query.description]
    result_list = [dict(zip(colname, r)) for r in query.fetchall()]
    cur.close()
    cur.connection.close()
    return json.dumps(result_list)

@app.route('/summaries/multi/reads', methods=['GET', 'POST'])
def get_multi_summaries_reads():  # put application's code here
    cur = get_db().cursor()
    ids = request.args.get('ids')
    read_or_write = request.args.get('read_or_write')
    # print(ids)
    if not read_or_write == "":
        sql = " SELECT * FROM summaries join results on summaries.id = results.summary_id WHERE performance_id in (" + ids +") AND operation == " +'\'' + read_or_write + '\''
    else:
        sql = " SELECT * FROM summaries join results on summaries.id = results.summary_id WHERE performance_id in (" + ids + ")"
    print(sql)
    query = cur.execute(sql)
    colname = [d[0] for d in query.description]
    result_list = [dict(zip(colname, r)) for r in query.fetchall()]
    cur.close()
    cur.connection.close()
    return json.dumps(result_list)

@app.route('/summaries/multi/writes', methods=['GET', 'POST'])
def get_multi_summaries_writes():  # put application's code here
    cur = get_db().cursor()
    ids = request.args.get('ids')
    # print(ids)
    sql = " SELECT * FROM summaries WHERE performance_id in (" + ids +") "
    print(sql)
    query = cur.execute(sql)
    colname = [d[0] for d in query.description]
    result_list = [dict(zip(colname, r)) for r in query.fetchall()]
    cur.close()
    cur.connection.close()
    return json.dumps(result_list)




@app.route('/results/', methods=['GET', 'POST'])
def get_results():  # put application's code here
    cur = get_db().cursor()
    summary_id = request.args.get('summary_id')
    #print(summary_id)
    # access = request.args.get('access')
    # query = cur.execute("SELECT * FROM results WHERE summary_id = ? AND  access = ?", id, access)
    sql = "SELECT * FROM results WHERE summary_id =" + summary_id
    query = cur.execute(sql)
    colname = [d[0] for d in query.description]
    result_list = [dict(zip(colname, r)) for r in query.fetchall()]
    cur.close()
    cur.connection.close()
    return json.dumps(result_list)


#TODO create more routes

if __name__ == '__main__':
    app.run()
