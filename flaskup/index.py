from flask import Flask, request, jsonify
import json
import datetime
from flask.ext.mysqldb import MySQL
from flask.ext.api import status
from flask_headers import headers

app = Flask(__name__)
 
# MySQL configurations
app.config['MYSQL_USER'] = 'team_a'
app.config['MYSQL_PASSWORD'] = '123$67'
app.config['MYSQL_DB'] = 'hackaton_hul_team_a'
app.config['MYSQL_HOST'] = '52.192.228.70'
app.config['MYSQL_PORT'] = 3306
app.config['MYSQL_CONNECT_TIMEOUT'] = 60
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)

TABLE_AUTH = "`T_CUSTOMER_AUTH`"
TABLE_COMPLAIN = "`T_INCIDENT_INFO`"
TABLE_CAL = "`T_CALENDAR_INFO`"
TABLE_PROMO = "`T_PROMOTION_INFO`"
TABLE_CUST = "`T_CUSTOMER_MSTR`"
TABLE_DELIVERY = "`T_DELIVERY_INFO`"
COL_CUST_ID = "`Customer_ID`"
COL_TOKEN = "`token`"


class ClientException(Exception):
    def __init__(self, val, status):
        self.val = val;
        self.status = status

    def __str__(self):
        return repr(self.val)


def get_table(where, table, join_table=None, join_keys=[], what="*"):
    cur = mysql.connection.cursor()
    condition = " AND ".join(["%s=%s" % (key, val) if key not in join_keys else "%s=%s" % (key, val) for key,val in where.items()])
    app.logger.error(condition)
    if join_table is None:
        cur.execute("SELECT * FROM %s WHERE (%s)" % (table, condition))
    else:
        cur.execute("SELECT * FROM %s, %s WHERE %s" % (table, join_table, condition))
    return cur.fetchall()


def cur_fetchall(command):
    cur = mysql.connection.cursor()
    cur.execute(command)
    mysql.connection.commit()
    return cur.fetchall()


def missing(req, rec):
    rem = set(req) - set(rec)
    if len(rem) == 0:
        return None
    else:
        raise ClientException("[" + ",".join(rem) + "] parameter(s) missing!",
        status.HTTP_400_BAD_REQUEST)


# converts an exception to a return
def exception_deco(func):
    def dwrapper():
        try:
            return func()
        except ClientException as e:
            return eval(str(e)), e.status
    return dwrapper


def get_post_params():
    return request.form


def get_get_params():
    return request.args

# throws exception if required parameters not present in post request
def requires_deco(method, *reqs):
    def deco(func):
        def dwrapper():
            missing(reqs, method().keys())
            return func()
        return dwrapper
    return deco


def auth_deco(param_method):
    def auth_deco_act(func):
        def wrapper():
            missing(["id", "token"], param_method().keys())
            users = get_auth_users(param_method)
            if len(users) == 0:
                raise ClientException("Invalid login details! id: %s token: %s"
                                      % (param_method()['id'], param_method()['token']),
                                      status.HTTP_401_UNAUTHORIZED)
            return func()
        return wrapper
    return auth_deco_act


def get_auth_users(param_method):
    cust_id = param_method()['id']
    token = param_method()['token']
    missing(["id", "token"], param_method().keys())
    users = get_table(where={COL_CUST_ID:"'" + cust_id + "'", "`token`":"'" + token + "'"}, table=TABLE_AUTH)
    return users


def sanitise_datetime(dict_rows):
    for row in dict_rows:
        for col, val in row.items():
            if isinstance(val, datetime.date):
                row[col] = val.isoformat()


@app.route("/login", methods=["POST"])
def login_t():
    return login()


@app.route("/req_otp", methods=["POST"])
def req_otp_t():
    return req_otp()

    
@app.route("/details", methods=["GET"])
@headers({'Cache-Control':'public, max-age=31556926'})
def cust_details_t():
    return cust_details()


@app.route("/calendar", methods=["GET"])
@headers({'Cache-Control':'public, max-age=31556926'})
def calendar_t():
    return calendar()


@app.route("/promo", methods=["GET"])
@headers({'Cache-Control':'public, max-age=31556926'})
def promo_t():
    return promo()


@app.route("/complaint", methods=["GET", "POST"])
@headers({'Cache-Control':'public, max-age=31556926'})
def complain_t():
    if request.method == 'GET':
        return get_complaint()
    else:
        return make_complaint()


@app.route("/invoice", methods=["GET"])
@headers({'Cache-Control':'public, max-age=31556926'})
def invoice_t():
    return invoice()


@app.route("/delivery", methods=["GET"])
@headers({'Cache-Control':'public, max-age=31556926'})
def delivery_t():
    return delivery()


@app.route("/sales", methods=["GET"])
@headers({'Cache-Control':'public, max-age=31556926'})
def sales_t():
    return sales()


@app.route("/gcmreg", methods=["POST"])
def gcmreg_t():
    return gcmreg()


@app.route("/credit", methods=["GET"])
@headers({'Cache-Control':'public, max-age=31556926'})
def credit_t():
    return credit()


@app.route("/cheque", methods=["GET"])
@headers({'Cache-Control':'public, max-age=31556926'})
def cheque_t():
    return cheque()


@exception_deco
@auth_deco(get_get_params)
def cheque():
    res = get_table({COL_CUST_ID:get_get_params()['id']}, table='`T_CHEQUE_UTILIZATION`')
    sanitise_datetime(res)
    return json.dumps(res)


@exception_deco
@auth_deco(get_get_params)
def credit():
    res = get_table({COL_CUST_ID:get_get_params()['id']}, table='`T_PENDING_CREDIT_DEBIT_NOTE`')
    sanitise_datetime(res)
    return json.dumps(res)


@exception_deco
@auth_deco(get_post_params)
@requires_deco(get_post_params, "gcmregid")
def gcmreg():
    gcmid = get_post_params()['gcmregid']
    res = cur_fetchall(
        ''' UPDATE %s
        SET gcmregid=%s
        WHERE %s=%s
        ''' % (TABLE_AUTH, gcmid, COL_CUST_ID, get_post_params()['id'])
    )
    return json.dumps(res)


@exception_deco
@auth_deco(get_get_params)
def sales():
    res = cur_fetchall(
        '''
        SELECT DISTINCT * FROM %s
        WHERE %s=%s
        ''' % ('`T_CAPITAL_PROJECTION`', COL_CUST_ID, get_get_params()['id'])
    )
    return json.dumps(res)


@exception_deco
@auth_deco(get_get_params)
def delivery():
    res = get_table({COL_CUST_ID:get_get_params()['id']}, table=TABLE_DELIVERY)

    sanitise_datetime(res)

    res = sorted(res, key=lambda x: x['DELIVERY_DATE'], reverse=True)

    return json.dumps(res)


@exception_deco
@auth_deco(get_get_params)
def invoice():
    res = cur_fetchall(
        '''SELECT *
        FROM T_INVOICE_DETAILS
        WHERE %s=%s
        ''' % (COL_CUST_ID, get_get_params()['id'])
    )
    return json.dumps(res)


@exception_deco
@auth_deco(get_post_params)
@requires_deco(get_post_params, "subject", "level")
def make_complaint():
    cust_id = get_post_params()['id']
    subject = get_post_params()['subject']
    level = get_post_params()['level']
    if level not in ['HIGH', 'LOW', 'MEDIUM']:
        raise ClientException('Invalid level value noob. Like really. What are you doing with your life',
                              status.HTTP_400_BAD_REQUEST)
    user = get_table({COL_CUST_ID:cust_id}, TABLE_CUST)[0]
    region = user['City'] if "region" not in get_post_params() else get_post_params()["region"]

    res = cur_fetchall(
        '''INSERT INTO %s
        VALUES (NULL, '%s', '%s', '%s', 'INCIDENT', '%s', 'PENDING', 'NONE', '%s')
        ''' % (TABLE_COMPLAIN, region, level, subject, datetime.date.today().isoformat(), user['Customer_ID'])
    )

    return json.dumps(res)


@exception_deco
@auth_deco(get_get_params)
def get_complaint():
    cust_id = get_get_params()['id']

    com = cur_fetchall(
        ''' SELECT *
        FROM %s
        WHERE %s=%s
        ''' % (TABLE_COMPLAIN, COL_CUST_ID, cust_id)
    )

    sanitise_datetime(com)

    type_map = {'HIGH':1, 'LOW':3, 'MEDIUM':2}
    status_map = {'PENDING':1, 'CLOSE':3, 'INPROCESS':2}

    com = sorted(com, key=lambda x: type_map[x['Incident_type']])
    com = sorted(com, key=lambda x: x['Created_On'], reverse=True)
    com = sorted(com, key=lambda x: status_map[x['Status']])

    return json.dumps(com)


@exception_deco
@requires_deco(get_get_params, "id", "token")
def promo():
    cust_id = get_get_params()['id']

    if len(get_auth_users(get_get_params)) == 0:
        raise ClientException("Invalid login details!", status.HTTP_401_UNAUTHORIZED)

    promo = cur_fetchall(
    '''
        SELECT *
        FROM %s
        WHERE %s=%s
    ''' % (TABLE_PROMO, COL_CUST_ID, cust_id)
    )

    sanitise_datetime(promo)

    return json.dumps(promo)


@exception_deco
@requires_deco(get_get_params, "id", "token")
def calendar():
    cust_id = get_get_params()['id']
    token = get_get_params()['token']

    if len(get_auth_users(get_get_params)) == 0:
        raise ClientException("Invalid login details!", status.HTTP_401_UNAUTHORIZED)

    cal = cur_fetchall(
    '''
        SELECT *
        FROM %s, %s
        WHERE %s=%s
        AND %s=%s
        AND %s=%s
    ''' % (TABLE_AUTH, TABLE_CAL,
           TABLE_AUTH +"." +COL_CUST_ID, TABLE_CAL + "." + COL_CUST_ID,
           TABLE_AUTH + "." + COL_CUST_ID, cust_id,
           COL_TOKEN, "'" + token +"'")
    )
    sanitise_datetime(cal)

    return json.dumps(cal)


@exception_deco
@requires_deco(get_get_params, "id", "token")
def cust_details():
    cust_id = get_get_params()['id']
    token = get_get_params()['token']

    users = cur_fetchall(
    '''
        SELECT * 
        FROM  `T_CUSTOMER_AUTH` ,  `T_CUSTOMER_MSTR` 
        WHERE T_CUSTOMER_AUTH.Customer_ID = T_CUSTOMER_MSTR.Customer_ID
        AND T_CUSTOMER_MSTR.Customer_ID =  '%s'
        AND token =  '%s'
    ''' % (cust_id, token))

    if len(users) == 0:
        raise ClientException("Invalid login details!", status.HTTP_401_UNAUTHORIZED)
    return jsonify(users[0])

@exception_deco
@requires_deco(get_post_params, "number", "otp")
def login():
    user = get_table({"number":request.form['number']}, TABLE_AUTH)

    if len(user) == 0:
        raise ClientException(json.dumps({'err':"Number not registered!"}), status.HTTP_404_NOT_FOUND)

    gcmid = "'" + get_post_params()["otp"] + "'"
    cur_fetchall(
    '''
    UPDATE %s
    SET gcmregid=%s
    WHERE %s=%s
    ''' % (TABLE_AUTH, gcmid, COL_CUST_ID, str(user[0]['Customer_ID'])))
    
    return jsonify(data=user[0])


@exception_deco
@requires_deco(get_post_params, "number")
def req_otp():
    req = ['number']
    missing(req, request.form.keys())
    user = get_table({"number":request.form['number']}, TABLE_AUTH)

    if len(user) == 0:
        raise ClientException(json.dumps({'err':"Number not registered!"}), status.HTTP_404_NOT_FOUND)
    
    return ''
    

@app.route("/")
def main():
    cur = mysql.connection.cursor()
    cur.execute('''SELECT * FROM T_CUSTOMER_MSTR''')
    rv = cur.fetchall()
    return jsonify(data=rv)


if __name__ == "__main__":
    app.run(debug=True)

