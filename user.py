from flask import Flask, request, Response
import base64
import mysql.connector
from mysql.connector import Error
from flask import abort
#from flask_basicauth import BasicAuth

from functools import wraps
import uuid
import time
from flask import jsonify
import bcrypt
import re 



app = Flask(__name__)




# 
user_name = ''
def check(authorization_header):
    # username = "f"
    # password = "f"
    encoded_uname_pass = authorization_header.split()[-1]
    data = base64.b64decode(encoded_uname_pass)
    
    #split the data on username:password 
    user_data = (str(data.decode('utf-8'))).split(":")
    global user_name 
    user_name = user_data[0]
    in_password = user_data[1]
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="Pari146!",
    database="network1"
    )

    mycursor = mydb.cursor()

    sql = "SELECT * FROM user_value WHERE email_address = %s"
    adr = (user_name,)

    mycursor.execute(sql, adr)
    rows = mycursor.fetchall()
    if len(rows) > 0:
      for x in rows:
        
        salt = x[7]
        data_password = x[4]
        #salt = bcrypt.gensalt()

        hashed = bcrypt.hashpw(in_password.encode('utf8'), salt.encode('utf8'))
        hash_password = hashed.decode('utf-8')
        
        if data_password == hash_password:

          return True

        else:
          abort(400)

    else:
      abort(400)



def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        authorization_header = request.headers.get('Authorization')
        if authorization_header and check(authorization_header):
            return f(*args, **kwargs)
        else:
            resp = Response()
            resp.headers['WWW-Authenticate'] = 'Basic'
            return resp, 401
        return f(*args, **kwargs)
    return decorated      

def valid_cred(email_address,password):
  regex_email = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
  regex_password = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{8,30}$"
  password_check = re.compile(regex_password)
  
  
  if((re.search(regex_email,email_address) == None) or (re.search(regex_password, password)==None)): 
    return False
  else:
    return True

    

#creation of user account
accounts=[]
@app.route("/user",methods=["POST"])
def addAccount():
  #take user input
  try:
    first_name = request.json['first_name']
    last_name = request.json['last_name']
    email_address = request.json['email_address']

    password = request.json['password']
  #throw bort(400) for less length password NIST
    account_created = time.time()
    account_updated = time.time()
    id = uuid.uuid4()
    flag = valid_cred(email_address,password)
    
    if flag != True:
      abort(400)
  except:
      abort(400)

  #post values in MySql database tables

  mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="Pari146!",
  database="network1"
  )

  mycursor = mydb.cursor()
  
  salt = bcrypt.gensalt()
  hashed = bcrypt.hashpw(password.encode('utf8'), salt)
  
  hash_password = hashed.decode('utf-8')
  sql = "INSERT INTO user_value (id,first_name,last_name,email_address,password,account_created,account_updated,salt) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
  val = (str(id),first_name,last_name,email_address,hash_password,account_created,account_updated,salt)
  

  
  try:
    
    mycursor.execute(sql, val)
    mydb.commit()
    data = {'id':id,
     'first_name':first_name,
     'last_name' : last_name,
     'email_address' : email_address,
     'account_created':account_created,
     'account_updated':account_updated
      }
    return jsonify(data)


  except:
    abort(400) 


  # try:

  #     sql = "INSERT INTO user_value (user_id,first_name,last_name,email_address,password,account_created,account_updated) VALUES (%s,%s,%s,%s,%s,%s,%s)"
  #     val = (user_id,first_name,last_name,email_address,password,account_created,account_updated)
  #     mycursor.execute(sql, val)

  #     mydb.commit()
  #     data = {'first_name':first_name,
  #         'last_name' : last_name,
  #         'email_address' : email_address,
  #         'user_id':user_id }
  #     return jsonify(data)
  # except:
  #     abort(400)





#update funnction

@app.route("/user",methods=["PUT"])
@login_required
def updateAccount():
  #take user input
  #pass a global username after validation from above
  try:
    first_name = request.json['first_name']
    last_name = request.json['last_name']
    email_address = user_name

    if request.json['email_address'] != user_name:
      return abort(400)
  
  
    password = request.json['password']
  #account_created = time.time()
    account_updated = time.time()
  except:
    abort(400)
  #user_id = uuid.uuid4()
  

  #post values in MySql database tables

  mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="Pari146!",
  database="network1"
  )

  
  salt = bcrypt.gensalt()
  hashed = bcrypt.hashpw(password.encode('utf8'), salt)
  
  hash_password = hashed.decode('utf-8')
  sql = "UPDATE  user_value SET first_name = %s,last_name = %s,password = %s, account_updated = %s, salt = %s WHERE email_address = %s"
  val = (first_name,last_name,hash_password,account_updated,salt,email_address)
  

  
  try:
     mycursor = mydb.cursor()
     mycursor.execute(sql, val)
     mydb.commit()
     return '', 204


  except:
     abort(400) 


@app.route("/test1",methods=["GET"])
def test7():
  return True
#get user details
@app.route("/user",methods=["GET"])
@login_required
def getAccount():
  #take user input
  #pass a global username after validation from above
  
  email_address = user_name
  
  #user_id = uuid.uuid4()
  

  #post values in MySql database tables

  mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="Pari146!",
  database="network1"
  )

  mycursor = mydb.cursor()
  
  sql = "SELECT * FROM user_value WHERE email_address = %s"
  val = (email_address,)
  # mycursor.execute(sql, val)

  
  
  
  
  try:
    #print(x)
    mycursor.execute(sql, val)

  
  
    myresult = mycursor.fetchall()
    for x in myresult:
     data = {'id':x[0],
     'first_name':x[1],
     'last_name' : x[2],
     'email_address' : x[3],
     'account_created':x[5],
     'account_updated':x[6]
      }
    return jsonify(data)


  except:
    abort(400) 






@app.route("/")

#@basic_auth.required

def runDemo():
  query = "INSERT INTO user1(fname) " \
            "VALUES(%s)"
  fname='abcd'
  args = (fname)
  
 
  mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="Pari146!",
  database="network1"
  )

  mycursor = mydb.cursor()

  sql = "INSERT INTO p1 (perid,name) VALUES (%s,%s)"
  val = ("1","ui")
  mycursor.execute(sql, val)

  mydb.commit()
  return "done"
if __name__ == '__main__':
  app.run(port=8080)