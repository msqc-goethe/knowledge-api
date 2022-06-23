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

@app.route('/iofh')
def get_IOFHs():  # put application's code here
    cur = get_db().cursor()
    query = cur.execute("SELECT i.id, i.\"start\" , i.\"end\", ir.id as run_id, ir.procs , ir.version ,ir.config_hash, ir.result_dir , ir.mode, is2.MD , is2.BW , is2.SCORE , s.name, s.kernel_version ,s.processor_architecture , s.processor_model ,s.processor_frequency ,s.processor_threads, s.processor_vendor, s.processor_L2 , s.processor_L3 , s.processor_coresPerSocket , s.distribution ,s.distribution_version , s.memory_capacity FROM IOFHs i INNER JOIN IOFHsRuns ir ON ir.IOFH_id  = i.id INNER JOIN IOFHsScores is2 ON is2.IOFH_id = ir.IOFH_id INNER JOIN sysinfos s  ON s.IOFH_id = is2.IOFH_id;")
    colname = [d[0] for d in query.description]
    result_list = [dict(zip(colname, r)) for r in query.fetchall()]
    cur.close()
    cur.connection.close()
    return json.dumps(result_list)

@app.route('/iofh_testcases')
def iofh_testcases():  # put application's code here
    cur = get_db().cursor()
    run_id = request.args.get('run_id')
    query = cur.execute("SELECT id, name, t_start, exe, stonewall, score, t_delta, t_end FROM IOFHsTestcases WHERE IOFHsRun_id  ="+ run_id+";")
    colname = [d[0] for d in query.description]
    result_list = [dict(zip(colname, r)) for r in query.fetchall()]
    cur.close()
    cur.connection.close()
    return json.dumps(result_list)


@app.route('/iofh_testcase_results')
def iofh_testcase_results():  # put application's code here
    cur = get_db().cursor()
    run_id = request.args.get('run_id')
    query = cur.execute("SELECT ires.IOFHsTestcase_id as testcase_id, ires.id as res_id, ires.access, ires.bwMiB, ires.iops, "
                        "ires.latency, ires.blockKiB, ires.xferKiB, ires.openTime, ires.wrRdTime, ires.closeTime, ires.totalTime, "
                        "ires.iter, iopt.id  as opt_id, iopt.api, iopt.apiVersion, iopt.testFileName , iopt.access , "
                        "iopt.\"type\" , iopt.segments , iopt.orderingInaFile, iopt.orderingInterFile, iopt.taskOffset , "
                        "iopt.nodes, iopt.tasks , iopt.clientsPerNode , iopt.repetitions , iopt.xfersize , iopt.blocksize , "
                        "iopt.aggregateFilesize , iopt.stonewallingTime , iopt.stoneWallingWearOut  "
                        "FROM IOFHsResults ires INNER JOIN IOFHsOptions iopt  ON ires.IOFHsTestcase_id  = iopt.IOFHsTestcase_id INNER JOIN IOFHsTestcases it"
                        "  ON it.id  = iopt.IOFHsTestcase_id where it.IOFHsRun_id == "+run_id+";")
    colname = [d[0] for d in query.description]
    result_list = [dict(zip(colname, r)) for r in query.fetchall()]
    cur.close()
    cur.connection.close()
    return json.dumps(result_list)


@app.route('/iofh_testcase_options')
def iofh_testcase_options():  # put application's code here
    cur = get_db().cursor()
    run_id = request.args.get('run_id')
    query = cur.execute("SELECT iopt.IOFHsTestcase_id as testcase_id, iopt.id  as opt_id, iopt.api, iopt.apiVersion, iopt.testFileName , iopt.access , "
                        "iopt.\"type\" , iopt.segments , iopt.orderingInaFile, iopt.orderingInterFile, iopt.taskOffset , "
                        "iopt.nodes, iopt.tasks , iopt.clientsPerNode , iopt.repetitions , iopt.xfersize , iopt.blocksize , "
                        "iopt.aggregateFilesize , iopt.stonewallingTime , iopt.stoneWallingWearOut "
                        "FROM IOFHsOptions iopt INNER JOIN IOFHsTestcases it ON iopt.IOFHsTestcase_id  = it.id where it.IOFHsRun_id == "+run_id+";")
    colname = [d[0] for d in query.description]
    result_list = [dict(zip(colname, r)) for r in query.fetchall()]
    cur.close()
    cur.connection.close()
    return json.dumps(result_list)



# @app.route('/iofh_testcase_results')
# def iofh_testcase_results():  # put application's code here
#     cur = get_db().cursor()
#     run_id = request.args.get('run_id')
#     query = cur.execute("SELECT ires.IOFHsTestcase_id as testcase_id, ires.id as res_id, iopt.id  as opt_id, ires.access, ires.bwMiB, ires.iops, it.name, it.t_start, it.exe, it.stonewall, it.score, "
#                         "it.t_delta, it.t_end, ires.latency, ires.blockKiB, ires.xferKiB, ires.openTime, ires.wrRdTime, ires.closeTime, ires.totalTime, ires.iter, "
#                         "iopt.api, iopt.apiVersion, iopt.testFileName , iopt.access , iopt.\"type\" , iopt.segments , iopt.orderingInaFile, iopt.orderingInterFile, iopt.taskOffset,"
#                         "iopt.nodes, iopt.tasks , iopt.clientsPerNode , iopt.repetitions , iopt.xfersize , iopt.blocksize , iopt.aggregateFilesize , iopt.stonewallingTime , "
#                         "iopt.stoneWallingWearOut FROM IOFHsResults ires INNER JOIN IOFHsOptions iopt  ON ires.IOFHsTestcase_id  = iopt.IOFHsTestcase_id INNER JOIN IOFHsTestcases it "
#                         "ON it.id  = iopt.IOFHsTestcase_id where it.IOFHsRun_id =="+run_id+";")
#     colname = [d[0] for d in query.description]
#     result_list = [dict(zip(colname, r)) for r in query.fetchall()]
#     cur.close()
#     cur.connection.close()
#     return json.dumps(result_list)


@app.route('/performances')
def get_performances():  # put application's code here
    cur = get_db().cursor()
    query = cur.execute("SELECT * FROM performances")
    colname = [d[0] for d in query.description]
    result_list = [ dict(zip(colname, r)) for r in query.fetchall() ]
    cur.close()
    cur.connection.close()
    return json.dumps(result_list)


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
    sql = " SELECT * FROM summaries WHERE performance_id in (" + ids +")"
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


if __name__ == '__main__':
    app.run()
