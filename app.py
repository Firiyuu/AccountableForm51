import psycopg2
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, g, session, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from forms import CreateAccount
from flask_bootstrap import Bootstrap
from flask_wtf import Form
from wtforms import StringField, PasswordField, IntegerField, DateField, FloatField
from wtforms.validators import InputRequired
from datetime import datetime
from configparser import ConfigParser
from models import Entry, EntryP, Register, EntryF, EntryB
import json
import time
from xml.etree import ElementTree
from decimal import Decimal
from bs4 import BeautifulSoup
import requests
import psycopg2.extras
from forms import *
import string
from random import *
from flask_weasyprint import HTML, render_pdf
from jinja2 import Template
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, ValidationError
from wtforms.validators import DataRequired, Length, EqualTo

# from escpos.printer import Usb


app = Flask(__name__, static_url_path="")
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:carrotcake092814@localhost:5432/AF51'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'flaskimplement'
app.debug = True
db = SQLAlchemy(app)
bootstrap = Bootstrap(app)


class User(db.Model):
    __tablename__ = "User"

    id = db.Column(db.Integer, primary_key=True)

    firstname = db.Column(db.String(80), unique=False)
    middlename = db.Column(db.String(80), unique=False)
    lastname = db.Column(db.String(80), unique=False)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(80), unique=True)
    officerrole = db.Column(db.String(80), unique=False)

    def __init__(self, firstname='', middlename='', lastname='', username='', password='', officerole=''):
        self.firstname = firstname
        self.middlename = middlename
        self.lastname = lastname
        self.username = username
        self.password = password
        self.officerrole = officerole

    def __repr__(self):
        return '<User %r>' % self.username

class CreateAccount(FlaskForm):
    firstname = StringField('FIRST NAME', validators=[DataRequired(), Length(min=1, max=50)])
    middlename = StringField('MIDDLE NAME', validators=[DataRequired(), Length(min=1, max=50)])
    lastname = StringField('LAST NAME', validators=[DataRequired(), Length(min=1, max=50)])
    username = StringField('USERNAME', validators=[DataRequired(), Length(min=4, max=25)])
    # password = PasswordField('PASSWORD', validators=[DataRequired(), Length(min=6, max=32)])
    # repeatpass = PasswordField('REPEAT PASSWORD', validators=[DataRequired(), EqualTo('password', message="Password must MATCH")])
    # officerrole = StringField('Officer Type of Role', validators=[DataRequired(), Length(min=3, max=50)])

    def validate_username(self, field):
      if User.query.filter_by(username=field.data).first():
        raise ValidationError('Username already in use.')

class nlogs(db.Model):

    __tablename__ = "nlogs"


    username = db.Column(db.String(80), unique=False)
    actions = db.Column(db.String(80), unique=False)
    natureOfCollection = db.Column(db.String(80), unique=False)
    amount = db.Column(db.String(80), unique=False)
    payor = db.Column(db.String(80), unique=False)
    transtime = db.Column(db.String(80), primary_key=True)

    def __init__(self, username, actions, natureOfCollection, amount, payor, transtime):

        self.username = username
        self.actions = actions
        self.natureOfCollection = natureOfCollection
        self.amount = amount
        self.payor = payor
        self.transtime = transtime

class FormForm(db.Model):

    __tablename__ = "form"

    payor = db.Column(db.String(80), unique=False)
    paymentmethod = db.Column(db.String(80), unique=False)
    receiptno = db.Column(db.Integer(), unique=True, primary_key=True)
    officer = db.Column(db.String(80), unique=False)
    collectiondate = db.Column(db.Date(), unique=False)
    nature = db.Column(db.String(80), unique=False)
    message = db.Column(db.String(80), unique=False)
    amount = db.Column(db.String(80), unique=False)

    def __init__(self, payor, paymentmethod, receiptno, officer, collectiondate, nature, message, amount):
      
        self.payor = payor
        self.paymentmethod = paymentmethod
        self.receiptno = receiptno
        self.officer = officer
        self.collectiondate = collectiondate
        self.nature = nature
        self.message = message
        self.amount = amount


class formType(db.Model):

    __tablename__ = "formType"

    id = db.Column(db.Integer, primary_key=True)

    noc = db.Column(db.String(80), unique=False)
    amount = db.Column(db.String(80), unique=False)

    def __init__(self, noc, amount):

        self.noc = noc
        self.amount = amount


print "Program Start"
 
def config(filename='database.ini', section='postgresql'):
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)
 
    # get section, default to postgresql
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))
 
    return db


print "Table created successfully"

def connect():
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # read connection parameters
        params = config()
 
        # connect to the PostgreSQL server
        print "Connecting to the PostgreSQL database..."
        conn = psycopg2.connect(**params)
 
        # create a cursor
        cur = conn.cursor()
        
 # execute a statement
        print 'PostgreSQL database version:'
        cur.execute('SELECT version()')
 
        # display the PostgreSQL database server version
        db_version = cur.fetchone()
        print db_version
       
     # close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print error
    finally:
        if conn is not None:
            conn.close()
            print "Database connection closed."


print "Program End"


def create_table():
    conn=psycopg2.connect("dbname='AF51' user='postgres' password='carrotcake092814' host='localhost' port='5432'")
    cur=conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS delinquincy(payer TEXT, due_date date, penalty integer )")
    conn.commit()
    conn.close()




def add_parameter(ent):
   conn = psycopg2.connect(database = "AF51", user = "postgres", password = "carrotcake092814", host = "127.0.0.1", port = "5432")
   print "Opened database successfully"
   cur = conn.cursor()

   cur.execute('''INSERT INTO parameters (nature,over,notover,officer) VALUES (%s,%s,%s,%s)''', (ent.nofcollection, ent.over, ent.nover, ent.officer))            
               
   print "Good"
   conn.commit()
   conn.close()



def add_entry(ent):
   conn = psycopg2.connect(database = "AF51", user = "postgres", password = "carrotcake092814", host = "127.0.0.1", port = "5432")
   print "Opened database successfully"
   cur = conn.cursor()
   


   cur.execute('''INSERT INTO form (receiptno, payor, officer, paymentmethod, message) VALUES (%s,%s,%s,%s,%s)''', ent)            
               
   print "Good"
   conn.commit()
   conn.close()

  

def add_parameterB(ent):
   conn = psycopg2.connect(database = "AF51", user = "postgres", password = "carrotcake092814", host = "127.0.0.1", port = "5432")
   print "Opened database successfully"
   cur = conn.cursor()
   


   cur.execute('''INSERT INTO "BPI" (cn,txp,tn,rp,ba,bgy,ctgy,ha,memo,vu,isdby) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)''', ent)           
               
   print "Good"
   conn.commit()
   conn.close()



def add_entryF(ent):
   conn = psycopg2.connect(database = "AF51", user = "postgres", password = "carrotcake092814", host = "127.0.0.1", port = "5432")
   print "Opened database successfully"
   cur = conn.cursor()
   
   cur.execute('''INSERT INTO formType (noc, amount) VALUES (%s,%s)''', (nofcollection, amt))            
               
   print "Good"
   conn.commit()
   conn.close()

def add_logForm(ent):
   conn = psycopg2.connect(database = "AF51", user = "postgres", password = "carrotcake092814", host = "127.0.0.1", port = "5432")
   print "Opened database successfully"
   cur = conn.cursor()
   


   cur.execute('''INSERT INTO nlogs (username, actions, natureOfCollection, amount, payor, transtime) VALUES (%s,%s,%s,%s,%s,current_timestamp)''', (entlogs.username,entlogs.actions,entlogs.nature1,entlogs.nature1amt,entlogs.payor,))            
               
   print "Good"
   conn.commit()
   conn.close()
 
@app.route('/')
def start():
  return render_template("start.html")

@app.route('/login', methods=['GET','POST'])
def home(username=None):
    if request.method == 'POST':
        session.pop('user', None)
        user_candidate= request.form['username']
        pass_candidate = request.form['password']
        conn = psycopg2.connect(database = "AF51", user = "postgres", password = "carrotcake092814", host = "127.0.0.1", port = "5432")
        print "Opened database successfully"
        print user_candidate
        print pass_candidate
        cur = conn.cursor()


        user1=cur.execute("""SELECT * FROM "User" WHERE username=%s""", (user_candidate,))
        pass1=cur.execute("""SELECT * FROM "User" WHERE password=%s""",(pass_candidate,))
        
        data=cur.fetchone()
                       
        conn.close()

        print user1
        print pass1
        print data
        try:    
            conn = psycopg2.connect(database = "AF51", user = "postgres", password = "carrotcake092814", host = "127.0.0.1", port = "5432")
            cur = conn.cursor()
            
            if user_candidate is '':
                return render_template("req_username.html")
            elif pass_candidate is '':
                return render_template("req_password.html")
            elif user_candidate not in data and pass_candidate not in data:
                session['user'] = request.form['username']
                return render_template("error_input.html")
            elif user_candidate  in data and pass_candidate  in data:
                session['user'] = request.form['username']
                conn = psycopg2.connect(database = "AF51", user = "postgres", password = "carrotcake092814", host = "127.0.0.1", port = "5432")
                print "Opened database successfully" 
                cur = conn.cursor()
                print(session['user'])
                cur.execute('SELECT "officerrole" from "User" WHERE "username" = %s', [session['user']])
                role = cur.fetchone()[0]
                print role
                print "================"
                if role == "Superadmin":
                  return render_template("header-second-bar.html", user = user_candidate)
                elif role =="Officer":
                  return render_template("header-second-baruser.html", user = user_candidate)
                elif role =="Admin":
                  return render_template("header-second-baradmin.html", user = user_candidate)
                else:
                  return render_template("header-second-barcashier.html", user = user_candidate)



            elif user_candidate not in username:
                return render_template("error_input.html")
        except Exception:
            return render_template("error_input.html")
    else:

        return render_template("login.html")


@app.route('/home')
def homenotlogin():
    if g.user:
       conn = psycopg2.connect(database = "AF51", user = "postgres", password = "carrotcake092814", host = "127.0.0.1", port = "5432")
       print "Opened database successfully" 
       cur = conn.cursor()
       print(session['user'])
       cur.execute('SELECT "officerrole" from "User" WHERE "username" = %s', [g.user])
       role = cur.fetchone()[0]
       print role
       print "================"
       user = str(g.user)
       if role == "Superadmin":
          return render_template("header-second-bar.html", user = g.user)
       elif role =="Officer":
          return render_template("header-second-baruser.html", user = g.user)
       elif role =="Admin":
          return render_template("header-second-baradmin.html", user = g.user)
       else:
          return render_template("header-second-barcashier.html", user = g.user)
    return redirect(url_for('home'))


@app.route('/landing')
def landing():
    if g.user:
       user = str(g.user)
       print user
       return render_template("header-second-bar.html", user = user)

    return redirect(url_for('home'))

@app.before_request
def before_request():
    g.user = None
    if 'user' in session:
        g.user = session['user']

@app.route('/logout')
def logout():
    session.pop('user',None)
    return redirect(url_for('home'))




@app.route('/logs')
def logs():
    if g.user:
       conn = psycopg2.connect(database = "AF51", user = "postgres", password = "carrotcake092814", host = "127.0.0.1", port = "5432")
       print "Opened database successfully" 
       cur = conn.cursor()
       print(session['user'])
       cur.execute('SELECT "officerrole" from "User" WHERE "username" = %s', [g.user])
       role = cur.fetchone()[0]
       print role
       print "================"
       user = str(g.user)
       if role == "Superadmin":
             #---------------
          try:
             conn = psycopg2.connect(database = "AF51", user = "postgres", password = "carrotcake092814", host = "127.0.0.1", port = "5432")
             cur = conn.cursor()
             cur.execute("SELECT * from nlogs ORDER BY transtime DESC")
             rows = cur.fetchall()
             print rows
          except:
             print ("Failed to open")

          return render_template('logs.html', rows=rows, user = g.user)

       elif role == "Admin":
          try:
             conn = psycopg2.connect(database = "AF51", user = "postgres", password = "carrotcake092814", host = "127.0.0.1", port = "5432")
             cur = conn.cursor()
             cur.execute("SELECT * from nlogs ORDER BY transtime DESC")
             rows = cur.fetchall()
             print rows
          except:
             print ("Failed to open")

          return render_template('logsadmin.html', rows=rows, user = g.user)        
       else:
          redirect(url_for('home'))

    return redirect(url_for('home'))





@app.route('/user')
def user():

 if g.user:
       conn = psycopg2.connect(database = "AF51", user = "postgres", password = "carrotcake092814", host = "127.0.0.1", port = "5432")
       print "Opened database successfully" 
       cur = conn.cursor()
       print(session['user'])
       cur.execute('SELECT "officerrole" from "User" WHERE "username" = %s', [g.user])
       role = cur.fetchone()[0]
       print role
       print "================"
       user = str(g.user)
       if role == "Superadmin":
             conn = psycopg2.connect(database = "AF51", user = "postgres", password = "carrotcake092814", host = "127.0.0.1", port = "5432")
             print "Opened database successfully" 
             cur = conn.cursor()
             g.user = str(g.user)
             print g.user
             rows = cur.execute("""SELECT * from "User" WHERE "username" = %s""",[g.user])
             print rows
             rows = cur.fetchall()
             print rows
             return render_template("user.html", rows=rows, user = g.user)

       elif role =="Officer":
             conn = psycopg2.connect(database = "AF51", user = "postgres", password = "carrotcake092814", host = "127.0.0.1", port = "5432")
             print "Opened database successfully" 
             cur = conn.cursor()
             g.user = str(g.user)
             print g.user
             rows = cur.execute("""SELECT * from "User" WHERE "username" = %s""",[g.user])
             print rows
             rows = cur.fetchall()
             print rows
             return render_template("useruser.html", rows=rows, user = g.user)

       elif role =="Admin":
             conn = psycopg2.connect(database = "AF51", user = "postgres", password = "carrotcake092814", host = "127.0.0.1", port = "5432")
             print "Opened database successfully" 
             cur = conn.cursor()
             g.user = str(g.user)
             print g.user
             rows = cur.execute("""SELECT * from "User" WHERE "username" = %s""",[g.user])
             print rows
             rows = cur.fetchall()
             print rows
             return render_template("useradmin.html", rows=rows, user = g.user)
       else:
             conn = psycopg2.connect(database = "AF51", user = "postgres", password = "carrotcake092814", host = "127.0.0.1", port = "5432")
             print "Opened database successfully" 
             cur = conn.cursor()
             g.user = str(g.user)
             print g.user
             rows = cur.execute("""SELECT * from "User" WHERE "username" = %s""",[g.user])
             print rows
             rows = cur.fetchall()
             print rows
             return render_template("usercashier.html", rows=rows, user = g.user)
          
 return redirect(url_for('home'))


conn = psycopg2.connect(database = "AF51", user = "postgres", password = "carrotcake092814", host = "127.0.0.1", port = "5432")
cur = conn.cursor()

cur.execute('SELECT receiptno FROM form ORDER BY receiptno DESC')
receiptno = cur.fetchone()
receiptno = int(receiptno[0]) + 1




@app.route('/payments/report/<receiptno>.pdf', methods=['POST','GET'])
def inspection_report(receiptno=None):
  if request.method == 'POST':
        switch = request.form['row_print']
        conn = psycopg2.connect(database = "AF51", user = "postgres", password = "carrotcake092814", host = "127.0.0.1", port = "5432")
        print "Opened database successfully" 
        cur = conn.cursor()
        cur.execute("""SELECT * FROM form WHERE receiptno=%s""",(switch,))
        rows = cur.fetchone();
        print rows
        context = {}
        context['payor'] = rows[0]
        context['payments'] = rows[1]
        context['receiptno'] = rows[2]
        context['officer'] = rows[3]
        context['date'] = rows[4]
        context['remarks'] = rows[6]



        nature = str(rows[5]).split(",")
        amount = str(rows[7]).split(",")

        context['amounts'] = amount

        context['natures'] = nature

        amounts = str(rows[7]).split(",")
        total =0
        for amount in amounts:
          total += float(amount)

        context['total'] = total
        html = render_template('inspection_report.html', **context)
        return render_pdf(HTML(string=html))
  else:
    return redirect(url_for('masterlistpayments'))


@app.route('/<path:path>')
def static_file(path):
    return app.send_static_file(path)

@app.route('/form')
def formfinal():
    if g.user:


       conn = psycopg2.connect(database = "AF51", user = "postgres", password = "carrotcake092814", host = "127.0.0.1", port = "5432")
       print "Opened database successfully" 
       cur = conn.cursor()
       print(session['user'])
       cur.execute('SELECT "officerrole" from "User" WHERE "username" = %s', [g.user])
       role = cur.fetchone()[0]
       print role
       print "================"
       user = str(g.user)
       if role == "Superadmin":
           user = str(g.user)
           actions="Applied"
           naive_dt = time.strftime("%m/%d/%Y")
           conn = psycopg2.connect(database = "AF51", user = "postgres", password = "carrotcake092814", host = "127.0.0.1", port = "5432")
           print "Opened database successfully" 
           cur = conn.cursor()
           cur.execute("""SELECT * FROM parameters""")
           rows = cur.fetchall();
           print rows      
           return render_template("indextest.html", rows=rows, user=user, receiptno=receiptno, date = naive_dt, cur=cur)

       elif role =="Officer":
           user = str(g.user)
           actions="Applied"
           naive_dt = time.strftime("%m/%d/%Y")
           conn = psycopg2.connect(database = "AF51", user = "postgres", password = "carrotcake092814", host = "127.0.0.1", port = "5432")
           print "Opened database successfully" 
           cur = conn.cursor()
           cur.execute("""SELECT * FROM parameters""")
           rows = cur.fetchall();
           print rows      
           return render_template("indextestuser.html", rows=rows, user=user, receiptno=receiptno, date = naive_dt, cur=cur)
       else:
         return redirect(url_for('home'))
      

    return redirect(url_for('home'))



@app.route('/addrec',methods = ['POST', 'GET'])
def addrec():

   if g.user:
        if request.method == 'POST':

#UPPER PANE
            jsdata1 = request.form['javascript_data1']
            jsdata2 = request.form['javascript_data2']

            payor = request.form['payor']         
            officer = g.user
            receiptno = int(request.form['OR'])
            paymentmethod = request.form['paymentmethod']
            naive_dt = time.strftime("%m/%d/%Y")
            collectiondate = naive_dt = datetime.now() 
            message = request.form['message']

            typeForm = FormForm(payor=payor, paymentmethod=paymentmethod, receiptno=receiptno, officer=officer, collectiondate=collectiondate, nature=jsdata1, message=message, amount = jsdata2)
            db.session.add(typeForm)
            db.session.commit()
            global receiptno
            receiptno +=1



            return redirect(url_for('formfinal'))

   return redirect(url_for('home'))



@app.route('/addparameters/delete/', methods=['GET','POST'])
def delete_row():

   if request.method == 'POST':
  
         conn = psycopg2.connect(database = "AF51", user = "postgres", password = "carrotcake092814", host = "127.0.0.1", port = "5432")
         print "Opened database successfully" 
         cur = conn.cursor()
         todelete =  request.form['row_delete']
         print todelete
         cur.execute("DELETE FROM parameters WHERE nature=%s",(todelete,))
         action = "deleted in NOC"
         noc = ''
         amt = todelete
         payor = ''
         cur.execute('''INSERT INTO nlogs (username, actions, "natureOfCollection", amount, payor, transtime) VALUES (%s,%s,%s,%s,%s,current_timestamp)''', (g.user,action,noc,amt,payor,)) 
         conn.commit()
         return redirect(url_for('addparameter'))



@app.route('/addparameters',methods = ['POST', 'GET'])
def addparameter():

 if g.user:


   conn = psycopg2.connect(database = "AF51", user = "postgres", password = "carrotcake092814", host = "127.0.0.1", port = "5432")
   print "Opened database successfully" 
   cur = conn.cursor()
   print(session['user'])
   cur.execute('SELECT "officerrole" from "User" WHERE "username" = %s', [g.user])
   role = cur.fetchone()[0]
   print role
   print "================"
   user = str(g.user)
   if role == "Superadmin":
      if request.method == 'POST':

        
            nofcollection = request.form['param']
            over = float(request.form['param2'])
            over = format(over,'.2f')
            nover = float(request.form['param3'])
            nover = format(nover,'.2f')
            officer = g.user

            ent = EntryP(nofcollection,over,nover,officer)
            add_parameter(ent)

      current_time = datetime.now()

      Date = current_time.strftime('%m/%d/%Y')
      conn = psycopg2.connect(database = "AF51", user = "postgres", password = "carrotcake092814", host = "127.0.0.1", port = "5432")
      print "Opened database successfully" 
      cur = conn.cursor()

      cur.execute("""SELECT * FROM parameters""")
      rows = cur.fetchall();
      print rows

  
      return render_template("admintest.html", date=Date, rows=rows, user = g.user)
   elif role =="Admin":
      if request.method == 'POST':

        
            nofcollection = request.form['param']
            over = float(request.form['param2'])
            over = format(over,'.2f')
            nover = float(request.form['param3'])
            nover = format(nover,'.2f')
            officer = g.user

            ent = EntryP(nofcollection,over,nover,officer)
            add_parameter(ent)

      current_time = datetime.now()

      Date = current_time.strftime('%m/%d/%Y')
      conn = psycopg2.connect(database = "AF51", user = "postgres", password = "carrotcake092814", host = "127.0.0.1", port = "5432")
      print "Opened database successfully" 
      cur = conn.cursor()

      cur.execute("""SELECT * FROM parameters""")
      rows = cur.fetchall();
      print rows

  
      return render_template("admintestadmin.html", date=Date, rows=rows, user = g.user)


   else:
          return redirect(url_for('home'))

 return redirect(url_for('home'))




        
@app.route("/businesspermits/makedeliquent", methods=['POST','GET'])
def make_del():

   if request.method == 'POST':
  
         conn = psycopg2.connect(database = "AF51", user = "postgres", password = "carrotcake092814", host = "127.0.0.1", port = "5432")
         print "Opened database successfully" 
         cur = conn.cursor()
         # todelete =  request.form['row_delete']
         # print todelete

         payor=request.form['payor']
         date=request.form['date']
         penalty=request.form['penalty']
         conn = psycopg2.connect("dbname = 'AF51' user = 'postgres' password = 'carrotcake092814' host = 'localhost' port = '5432'")
         cur=conn.cursor()
         ent = payor,date,penalty
         cur.execute('''INSERT INTO deliquincy (payer,due_date,penalty) VALUES (%s,%s,%s)''', ent)
         cur.execute("""DELETE FROM "BPI" WHERE rp=%s""",(payor,))
         action = "transfered business permit to delinquent"
         noc = ''
         amt = payor
         payor = ''
         cur.execute('''INSERT INTO nlogs (username, actions, "natureOfCollection", amount, payor, transtime) VALUES (%s,%s,%s,%s,%s,current_timestamp)''', (g.user,action,noc,amt,payor,)) 
         conn.commit()
         conn.close()
         return redirect(url_for('masterlistpermits'))





@app.route('/logs/delete/', methods=['GET','POST'])
def delete_rowLGS():

   if request.method == 'POST':
  
         conn = psycopg2.connect(database = "AF51", user = "postgres", password = "carrotcake092814", host = "127.0.0.1", port = "5432")
         print "Opened database successfully" 
         cur = conn.cursor()
         todelete =  request.form['row_delete']
         print todelete
         cur.execute("""DELETE FROM nlogs WHERE username=%s""",(todelete,))
         conn.commit()
         return redirect(url_for('logs'))



@app.route('/payments/delete/',methods = ['POST', 'GET'])
def delete_PMNTS():
   if request.method == 'POST':
  
         conn = psycopg2.connect(database = "AF51", user = "postgres", password = "carrotcake092814", host = "127.0.0.1", port = "5432")
         print "Opened database successfully" 
         cur = conn.cursor()
         todelete =  request.form['row_delete']
         print todelete
         cur.execute("""DELETE FROM form WHERE receiptno=%s""",(todelete,))
         conn.commit()
         return redirect(url_for('masterlistpayments'))





#------------------------------------------

@app.route('/businesspermits/delete/', methods=['GET','POST'])
def delete_rowBM():

   if request.method == 'POST':
  
         conn = psycopg2.connect(database = "AF51", user = "postgres", password = "carrotcake092814", host = "127.0.0.1", port = "5432")
         print "Opened database successfully" 
         cur = conn.cursor()
         todelete =  request.form['row_delete']
         print todelete


         noc = ''
         action = 'delete in business permit'
         payor = ''
         amt = todelete
         cur.execute('''INSERT INTO nlogs (username, actions, "natureOfCollection", amount, payor, transtime) VALUES (%s,%s,%s,%s,%s,current_timestamp)''', (g.user,action,noc,amt,payor,)) 





         cur.execute("""DELETE FROM "BPI" WHERE cn=%s""",(todelete,))
         conn.commit()
         return redirect(url_for('masterlistpermits'))




@app.route('/issuebusinesspermit',methods = ['POST', 'GET'])
def issuebusinesspermit():

 if g.user:

       conn = psycopg2.connect(database = "AF51", user = "postgres", password = "carrotcake092814", host = "127.0.0.1", port = "5432")
       print "Opened database successfully" 
       cur = conn.cursor()
       print(session['user'])
       cur.execute('SELECT "officerrole" from "User" WHERE "username" = %s', [g.user])
       role = cur.fetchone()[0]
       print role
       print "================"
       user = str(g.user)
       if role == "Superadmin":
          if request.method == 'POST':

        
                cn = request.form['param']
                print cn+"___________________________________________________________________"
                txp = request.form['param2']
                tn = request.form['param3']
                rp = request.form['param4']
                ba = request.form['param5']
                bgy = request.form['param6']
                ctgy = request.form['param7']
                ha = request.form['param8']
                memo = request.form['param9']
                vu = request.form['param10']
                officer = str(g.user)

                ent = cn,txp,tn,rp, ba, bgy,ctgy,ha,memo,vu,officer
                add_parameterB(ent)

                current_time = datetime.now()


  
          return render_template("BPI.html", user=g.user)
       elif role =="Officer":
          if request.method == 'POST':

        
                cn = request.form['param']
                print cn+"___________________________________________________________________"
                txp = request.form['param2']
                tn = request.form['param3']
                rp = request.form['param4']
                ba = request.form['param5']
                bgy = request.form['param6']
                ctgy = request.form['param7']
                ha = request.form['param8']
                memo = request.form['param9']
                vu = request.form['param10']
                officer = str(g.user)

                ent = cn,txp,tn,rp, ba, bgy,ctgy,ha,memo,vu,officer
                add_parameterB(ent)

                current_time = datetime.now()


  
          return render_template("BPIuser.html", user=g.user)
       else:
          return redirect(url_for('home'))

  #---Safety

 return redirect(url_for('home'))
        






@app.route('/masterlist')
def masterlist():
    if g.user: 

       conn = psycopg2.connect(database = "AF51", user = "postgres", password = "carrotcake092814", host = "127.0.0.1", port = "5432")
       print "Opened database successfully" 
       cur = conn.cursor()
       print(session['user'])
       cur.execute('SELECT "officerrole" from "User" WHERE "username" = %s', [g.user])
       role = cur.fetchone()[0]
       print role
       print "================"
       user = str(g.user)
       if role == "Superadmin":
          return render_template("mastermain.html" , user = g.user)
       elif role =="Officer":
          return render_template("mastermainuser.html" , user = g.user)
       elif role =="Admin":
          return render_template("mastermainadmin.html", user = g.user)
       else:
          return redirect(url_for('home'))



     

    return redirect(url_for('home'))





@app.route('/businesspermits',methods = ['POST', 'GET'])
def masterlistpermits():
    if g.user:
       conn = psycopg2.connect(database = "AF51", user = "postgres", password = "carrotcake092814", host = "127.0.0.1", port = "5432")
       print "Opened database successfully" 
       cur = conn.cursor()
       print(session['user'])
       cur.execute('SELECT "officerrole" from "User" WHERE "username" = %s', [g.user])
       role = cur.fetchone()[0]
       print role
       print "================"
       user = str(g.user)
       if role == "Superadmin":
          if request.method == "POST":
             target=request.form['sent']
             print(target)
             conn = psycopg2.connect(database = "AF51", user = "postgres", password = "carrotcake092814", host = "127.0.0.1", port = "5432")
             print "Opened database successfully" 
             cur = conn.cursor()
             cur.execute("SELECT * from tax WHERE year = %s",[target])
             result=cur.fetchone()
             response= json.dumps(result)
             print(response)
             print("flag1")
             return response

          conn = psycopg2.connect(database = "AF51", user = "postgres", password = "carrotcake092814", host = "127.0.0.1", port = "5432")
          print "Opened database successfully" 
          cur = conn.cursor()
          cur.execute("""SELECT * FROM "BPI" """)
          rows = cur.fetchall();
          cur.execute("""SELECT * from tax""")
          gets=cur.fetchall()
          conn.close()
          print rows
          return render_template("bpmasterlist.html" , user=g.user, rows=rows, gets=gets)       
       elif role =="Officer":
          if request.method == "POST":
             target=request.form['sent']
             print(target)
             conn = psycopg2.connect(database = "AF51", user = "postgres", password = "carrotcake092814", host = "127.0.0.1", port = "5432")
             print "Opened database successfully" 
             cur = conn.cursor()
             cur.execute("SELECT * from tax WHERE year = %s",[target])
             result=cur.fetchone()
             response= json.dumps(result)
             print(response)
             print("flag1")
             return response

          conn = psycopg2.connect(database = "AF51", user = "postgres", password = "carrotcake092814", host = "127.0.0.1", port = "5432")
          print "Opened database successfully" 
          cur = conn.cursor()
          cur.execute("""SELECT * FROM "BPI" """)
          rows = cur.fetchall();
          cur.execute("""SELECT * from tax""")
          gets=cur.fetchall()
          conn.close()
          print rows
          return render_template("bpmasterlistuser.html" , user=g.user, rows=rows, gets=gets)           

       elif role =="Admin":
          if request.method == "POST":
             target=request.form['sent']
             print(target)
             conn = psycopg2.connect(database = "AF51", user = "postgres", password = "carrotcake092814", host = "127.0.0.1", port = "5432")
             print "Opened database successfully" 
             cur = conn.cursor()
             cur.execute("SELECT * from tax WHERE year = %s",[target])
             result=cur.fetchone()
             response= json.dumps(result)
             print(response)
             print("flag1")
             return response

          conn = psycopg2.connect(database = "AF51", user = "postgres", password = "carrotcake092814", host = "127.0.0.1", port = "5432")
          print "Opened database successfully" 
          cur = conn.cursor()
          cur.execute("""SELECT * FROM "BPI" """)
          rows = cur.fetchall();
          cur.execute("""SELECT * from tax""")
          gets=cur.fetchall()
          conn.close()
          print rows
          return render_template("bpmasterlistadmin.html" , user=g.user, rows=rows, gets=gets)
       else:
          return redirect(url_for('home'))

      #---Safety
        


  

    return redirect(url_for('home'))






@app.route('/payments',methods = ['POST', 'GET'])
def masterlistpayments():
    if g.user:
       conn = psycopg2.connect(database = "AF51", user = "postgres", password = "carrotcake092814", host = "127.0.0.1", port = "5432")
       print "Opened database successfully" 
       cur = conn.cursor()
       print(session['user'])
       cur.execute('SELECT "officerrole" from "User" WHERE "username" = %s', [g.user])
       role = cur.fetchone()[0]
       print role
       print "================"
       user = str(g.user)
       if role == "Superadmin":
          conn = psycopg2.connect(database = "AF51", user = "postgres", password = "carrotcake092814", host = "127.0.0.1", port = "5432")
          print "Opened database successfully" 
          cur = conn.cursor()

          cur.execute("""SELECT * FROM form """)
          rows = cur.fetchall();
          print rows

          return render_template("pmmasterlist.html" , user=g.user, rows=rows)    

       elif role =="Officer":
          conn = psycopg2.connect(database = "AF51", user = "postgres", password = "carrotcake092814", host = "127.0.0.1", port = "5432")
          print "Opened database successfully" 
          cur = conn.cursor()

          cur.execute("""SELECT * FROM form """)
          rows = cur.fetchall();
          print rows

          return render_template("pmmaslistuser.html" , user=g.user, rows=rows)        
       elif role =="Admin":
          conn = psycopg2.connect(database = "AF51", user = "postgres", password = "carrotcake092814", host = "127.0.0.1", port = "5432")
          print "Opened database successfully" 
          cur = conn.cursor()

          cur.execute("""SELECT * FROM form """)
          rows = cur.fetchall();
          print rows

          return render_template("pmmasterlistadmin.html" , user=g.user, rows=rows) 
       else:
          conn = psycopg2.connect(database = "AF51", user = "postgres", password = "carrotcake092814", host = "127.0.0.1", port = "5432")
          print "Opened database successfully" 
          cur = conn.cursor()

          cur.execute("""SELECT * FROM form """)
          rows = cur.fetchall();
          print rows

          return render_template("pmcashier.html" , user=g.user, rows=rows)


      #---Safety
        # conn = psycopg2.connect(database = "AF51", user = "postgres", password = "carrotcake092814", host = "127.0.0.1", port = "5432")
        # print "Opened database successfully" 
        # cur = conn.cursor()

        # cur.execute("""SELECT * FROM form """)
        # rows = cur.fetchall();
        # print rows

        # return render_template("pmmasterlist.html" , user=g.user, rows=rows)
    # else:
    #     conn = psycopg2.connect(database = "AF51", user = "postgres", password = "carrotcake092814", host = "127.0.0.1", port = "5432")
    #     print "Opened database successfully" 
    #     cur = conn.cursor()

    #     cur.execute("""SELECT * FROM form """)
    #     rows = cur.fetchall();
    #     print rows

    #     return render_template("pmmaslistuser.html" , user=g.user, rows=rows) 
    return redirect(url_for('home'))








@app.route('/query')
def query():
  if g.user:
       conn = psycopg2.connect(database = "AF51", user = "postgres", password = "carrotcake092814", host = "127.0.0.1", port = "5432")
       print "Opened database successfully" 
       cur = conn.cursor()
       print(session['user'])
       cur.execute('SELECT "officerrole" from "User" WHERE "username" = %s', [g.user])
       role = cur.fetchone()[0]
       print role
       print "================"
       user = str(g.user)
       if role == "Superadmin":
          return render_template('query.html', user =g.user)
       elif role =="Admin":
          return render_template('queryadmin.html', user =g.user)
       else:
          return redirect(url_for('home'))

    #---Safety
    # return render_template('query.html', user =g.user)
  return redirect(url_for('home'))


@app.route('/transact', methods=['POST', 'GET'])
def transact():
  if g.user:
       conn = psycopg2.connect(database = "AF51", user = "postgres", password = "carrotcake092814", host = "127.0.0.1", port = "5432")
       print "Opened database successfully" 
       cur = conn.cursor()
       print(session['user'])
       cur.execute('SELECT "officerrole" from "User" WHERE "username" = %s', [g.user])
       role = cur.fetchone()[0]
       print role
       print "================"
       user = str(g.user)
       if role == "Superadmin":
           if request.method == 'POST':
               try:
                   start_date = request.form['start']
                   end_date = request.form['end']
                   print start_date
                   print end_date
                   conn = psycopg2.connect(database="AF51", user="postgres", password="carrotcake092814", host="localhost", port="5432")
                   cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
                   cur.execute("""SELECT * FROM payments WHERE transactiondate BETWEEN  %s AND %s""", (start_date,end_date))
                   rows = cur.fetchall()
                   conn.close()
                   print rows

               except:
                   print ("Error")

               finally:
                   msg = ("From " + start_date + " To " + end_date + "")
                   return render_template('Qresult.html', user=g.user, rows=rows, msg=msg)
       elif role =="Admin":
           if request.method == 'POST':
               try:
                   start_date = request.form['start']
                   end_date = request.form['end']
                   print start_date
                   print end_date
                   conn = psycopg2.connect(database="AF51", user="postgres", password="carrotcake092814", host="localhost", port="5432")
                   cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
                   cur.execute("""SELECT * FROM payments WHERE transactiondate BETWEEN  %s AND %s""", (start_date,end_date))
                   rows = cur.fetchall()
                   conn.close()
                   print rows

               except:
                   print ("Error")

               finally:
                   msg = ("From " + start_date + " To " + end_date + "")
                   return render_template('Qresultadmin.html', user=g.user, rows=rows, msg=msg)      
       else:
          return redirect(url_for('home'))

  return redirect(url_for('home'))



#CREATE

@app.route('/adminsettings')
def adminsettings():
  if g.user:

       conn = psycopg2.connect(database = "AF51", user = "postgres", password = "carrotcake092814", host = "127.0.0.1", port = "5432")
       print "Opened database successfully" 
       cur = conn.cursor()
       print(session['user'])
       cur.execute('SELECT "officerrole" from "User" WHERE "username" = %s', [g.user])
       role = cur.fetchone()[0]
       print role
       print "================"
       user = str(g.user)
       if role == "Superadmin" or role == "Admin":
          return render_template('Chome.html', user =g.user)

       else:
          return redirect(url_for('home'))
  return redirect("/home")


@app.route('/create')
def create():
  if g.user:
       conn = psycopg2.connect(database = "AF51", user = "postgres", password = "carrotcake092814", host = "127.0.0.1", port = "5432")
       print "Opened database successfully" 
       cur = conn.cursor()
       print(session['user'])
       cur.execute('SELECT "officerrole" from "User" WHERE "username" = %s', [g.user])
       role = cur.fetchone()[0]
       print role
       print "================"
       user = str(g.user)
       form = CreateAccount()
       msg = ""
       if role == "Superadmin" or role == "Admin":
            return render_template('Ccreate.html', form=form, msg=msg)
       else:
            return redirect(url_for('home'))

  return redirect(url_for('home'))

@app.route('/createaccount', methods=['POST', 'GET'])
def createaccount():
  test = request.method
  form = CreateAccount()
  if g.user:
       conn = psycopg2.connect(database = "AF51", user = "postgres", password = "carrotcake092814", host = "127.0.0.1", port = "5432")
       print "Opened database successfully" 
       cur = conn.cursor()
       print(session['user'])
       cur.execute('SELECT "officerrole" from "User" WHERE "username" = %s', [g.user])
       role = cur.fetchone()[0]
       print role
       print "================"
       if role == "Superadmin" or role == "Admin":
        chars = string.ascii_letters + string.digits
        passwords = "".join(choice(chars) for x in range(randint(8, 10)))
        print "BUGBUG"
        if test == 'POST':
              print test
              if form.validate_on_submit():
                print test+"test"
                randompass = passwords
                role = "Admin"
                user = User(firstname=form.firstname.data, middlename=form.middlename.data, lastname=form.lastname.data,
                            username=form.username.data, password=randompass, officerole=role)
                db.session.add(user)
                db.session.commit()

                msg = "Account Successfully Created"
                return redirect('/print')
        else:
          return redirect(url_for('home'))

       return redirect(url_for('printall', form=form))
  return redirect(url_for('formfinal'))


@app.route('/print')
def printall():
  form = CreateAccount()
  if g.user:
       conn = psycopg2.connect(database = "AF51", user = "postgres", password = "carrotcake092814", host = "127.0.0.1", port = "5432")
       print "Opened database successfully" 
       cur = conn.cursor()
       print(session['user'])
       cur.execute('SELECT "officerrole" from "User" WHERE "username" = %s', [g.user])
       role = cur.fetchone()[0]
       print role

       print "================"
       if role == "Superadmin":
          myUser = User.query.all()
          return render_template('Cprintfinal.html', myUser=myUser,form=form)
       elif role == "Admin":
          myUser = User.query.all()
          return render_template('Cprintfinaladmin.html', myUser=myUser,form=form)        
       else:
          return redirect(url_for('home'))
  return redirect(url_for('home'))


@app.route('/delete', methods=['POST', 'GET'])
def delete():
  if g.user:
       conn = psycopg2.connect(database = "AF51", user = "postgres", password = "carrotcake092814", host = "127.0.0.1", port = "5432")
       print "Opened database successfully" 
       cur = conn.cursor()
       print(session['user'])
       cur.execute('SELECT "officerrole" from "User" WHERE "username" = %s', [g.user])
       role = cur.fetchone()[0]
       print role
       action = "edited info in delinquency"
       noc = ''

       payor = ''
       print "================" 
       if role == "Superadmin" or role == "Admin":

         if request.method == "POST":
             test = request.form['delete_row']
             amt = test
             user = User.query.filter_by(username=test).first()
             db.session.delete(user)
             cur.execute('''INSERT INTO nlogs (username, actions, "natureOfCollection", amount, payor, transtime) VALUES (%s,%s,%s,%s,%s,current_timestamp)''', (g.user,action,noc,amt,payor,)) 

             db.session.commit()
             return redirect('/print')
       else:
          return redirect(url_for('home'))
     








@app.route('/update', methods=['POST'])
def update():
  if g.user:
       conn = psycopg2.connect(database = "AF51", user = "postgres", password = "carrotcake092814", host = "127.0.0.1", port = "5432")
       print "Opened database successfully" 
       cur = conn.cursor()
       print(session['user'])
       cur.execute('SELECT "officerrole" from "User" WHERE "username" = %s', [g.user])
       role = cur.fetchone()[0]
       print role

       print "================" 
       if role == "Superadmin" or role == "Admin":
          user = request.args.get('id')
          if request.method == "POST":
              update = User.query.filter_by(username=user).first()

              update.firstname = request.form.get('firstname')
              update.middlename = request.form.get('midname')
              update.lastname = request.form.get('lastname')
              update.password = request.form.get('password')

              db.session.commit()
          return redirect('/print')
  else:
      return redirect(url_for('home'))







@app.route("/businesspermits/edit",methods=['POST','GET'])
def editRowBP():
  if g.user:
       conn = psycopg2.connect(database = "AF51", user = "postgres", password = "carrotcake092814", host = "127.0.0.1", port = "5432")
       print "Opened database successfully" 
       cur = conn.cursor()
       print(session['user'])
       cur.execute('SELECT "officerrole" from "User" WHERE "username" = %s', [g.user])
       action = "edited info in business permit"
       noc = ''

       payor = ''
       role = cur.fetchone()[0]
       print role
       print "================" 
       if role == "Superadmin" or role == "Admin":
          if request.method=="POST":
              cn=request.form['cont']
              tp=request.form['tpayer']
              tn=request.form['trname']
              rp=request.form['rep']
              ba=request.form['b_adr']
              bgy=request.form['brgy']
              ctgy=request.form['catg']
              ha=request.form['hadr']
              memo=request.form['memo']
              isdby=request.form['isby']
              amt = rp


              conn = psycopg2.connect("dbname = 'AF51' user = 'postgres' password = 'carrotcake092814' host = 'localhost' port = '5432'")
              cur=conn.cursor()
              cur.execute("""UPDATE "BPI" SET txp=%s , tn = %s, rp=%s, ba=%s, bgy=%s,ctgy=%s,ha=%s,memo=%s,isdby=%s  WHERE cn= %s""",(tp,tn,rp,ba,bgy,ctgy,ha,memo,isdby,cn))
              cur.execute('''INSERT INTO nlogs (username, actions, "natureOfCollection", amount, payor, transtime) VALUES (%s,%s,%s,%s,%s,current_timestamp)''', (g.user,action,noc,amt,payor,)) 

              conn.commit()
              conn.close()
              return redirect('/businesspermits')
       else:
          return redirect(url_for('home'))



@app.route("/businesspermits/pay",methods=['POST','GET'])
def pay():
  if g.user:
       conn = psycopg2.connect(database = "AF51", user = "postgres", password = "carrotcake092814", host = "127.0.0.1", port = "5432")
       print "Opened database successfully" 
       cur = conn.cursor()
       print(session['user'])
       cur.execute('SELECT "officerrole" from "User" WHERE "username" = %s', [g.user])
       role = cur.fetchone()[0]
       print role
       print "================" 
       if role == "Superadmin" or role == "Admin":

          if request.method=="POST":
              amount=request.form['postAmount']
              year=request.form['year']
              quarter=request.form['quarter']
              conn = psycopg2.connect("dbname = 'AF51' user = 'postgres' password = 'carrotcake092814' host = 'localhost' port = '5432'")
              cur=conn.cursor()
              if quarter == 'q1':
                  cur.execute("UPDATE tax SET quarter1=%s  WHERE year = %s",(amount,year))
                  conn.commit()
                  conn.close()
              elif quarter == 'q2':
                  cur.execute("UPDATE tax SET quarter2=%s  WHERE year = %s",(amount,year))
                  conn.commit()
                  conn.close()
              elif quarter == 'q3':
                  cur.execute("UPDATE tax SET quarter3=%s  WHERE year = %s",(amount,year))
                  conn.commit()
                  conn.close()
              elif quarter == 'q4':
                  cur.execute("UPDATE tax SET quarter4=%s WHERE year = %s",(amount,year))
                  conn.commit()
                  conn.close()
              return redirect('/businesspermits')
       else:
          return redirect(url_for('home'))





@app.route("/delinquency",methods=['POST','GET'])
def delinquincy_list():
  if g.user:
       conn = psycopg2.connect(database = "AF51", user = "postgres", password = "carrotcake092814", host = "127.0.0.1", port = "5432")
       print "Opened database successfully" 
       cur = conn.cursor()
       print(session['user'])
       cur.execute('SELECT "officerrole" from "User" WHERE "username" = %s', [g.user])
       role = cur.fetchone()[0]
       print role
       print "================"
       user = str(g.user)
       if role == "Superadmin":
           if request.method=='POST':
               target=request.form['sent']
               print(target)
               conn=psycopg2.connect("dbname = 'AF51' user = 'postgres' password = 'carrotcake092814' host = 'localhost' port = '5432'")
               cur=conn.cursor()
               cur.execute("SELECT *from tax WHERE year = %s",[target])
               result=cur.fetchone()
               response= json.dumps(result)
               print(response)
               return response

           conn=psycopg2.connect("dbname = 'AF51' user = 'postgres' password = 'carrotcake092814' host = 'localhost' port = '5432'")
           cur=conn.cursor()
           cur.execute("""SELECT * from deliquincy""")
           row=cur.fetchall()
           cur.execute("""SELECT * from tax""")
           gets=cur.fetchall()
           conn.close()
           rows=[{'name': name, 'date': date ,'penalty':penalty} for name,date,penalty in row]
           return render_template("test_del.html",user=g.user,rows=rows,gets=gets)


       elif role =="Officer":
           if request.method=='POST':
               target=request.form['sent']
               print(target)
               conn=psycopg2.connect("dbname = 'AF51' user = 'postgres' password = 'carrotcake092814' host = 'localhost' port = '5432'")
               cur=conn.cursor()
               cur.execute("SELECT *from tax WHERE year = %s",[target])
               result=cur.fetchone()
               response= json.dumps(result)
               print(response)
               return response

           conn=psycopg2.connect("dbname = 'AF51' user = 'postgres' password = 'carrotcake092814' host = 'localhost' port = '5432'")
           cur=conn.cursor()
           cur.execute("""SELECT * from deliquincy""")
           row=cur.fetchall()
           cur.execute("""SELECT * from tax""")
           gets=cur.fetchall()
           conn.close()
           rows=[{'name': name, 'date': date ,'penalty':penalty} for name,date,penalty in row]
           return render_template("to_deluser.html",user=g.user,rows=rows,gets=gets)
       elif role =="Admin":
           if request.method=='POST':
               target=request.form['sent']
               print(target)
               conn=psycopg2.connect("dbname = 'AF51' user = 'postgres' password = 'carrotcake092814' host = 'localhost' port = '5432'")
               cur=conn.cursor()
               cur.execute("SELECT *from tax WHERE year = %s",[target])
               result=cur.fetchone()
               response= json.dumps(result)
               print(response)
               return response

           conn=psycopg2.connect("dbname = 'AF51' user = 'postgres' password = 'carrotcake092814' host = 'localhost' port = '5432'")
           cur=conn.cursor()
           cur.execute("""SELECT * from deliquincy""")
           row=cur.fetchall()
           cur.execute("""SELECT * from tax""")
           gets=cur.fetchall()
           conn.close()
           rows=[{'name': name, 'date': date ,'penalty':penalty} for name,date,penalty in row]
           return render_template("test_deladmin.html",user=g.user,rows=rows,gets=gets)

       else:
          return redirect("/home")



  return redirect("/home")

@app.route("/delinquency/edit",methods=['POST','GET'])
def editRow():
    if request.method=="POST":
        payor=request.form['payor']
        date=request.form['date']
        penalty=request.form['penalty']
        conn = psycopg2.connect("dbname = 'AF51' user = 'postgres' password = 'carrotcake092814' host = 'localhost' port = '5432'")
        cur=conn.cursor()
        cur.execute("UPDATE deliquincy SET due_date=%s , penalty = %s WHERE payer = %s",(date,penalty,payor))
        action = "edited info in delinquency"
        noc = ''
        amt = payor
        payor = ''
        cur.execute('''INSERT INTO nlogs (username, actions, "natureOfCollection", amount, payor, transtime) VALUES (%s,%s,%s,%s,%s,current_timestamp)''', (g.user,action,noc,amt,payor,)) 
        conn.commit()
        conn.close()
        return redirect('/delinquency')

@app.route("/delinquency/delete", methods=['POST','GET'])
def deleteRow():
    if request.method=='POST':
        target=request.form['delete_row']
        conn = psycopg2.connect("dbname = 'AF51' user = 'postgres' password = 'carrotcake092814' host = 'localhost' port = '5432'")
        cur = conn.cursor()
        cur.execute("DELETE FROM deliquincy WHERE payer =%s",[target])
        action = "deleted in delinquency"
        noc = ''
        amt = target
        payor = ''
        cur.execute('''INSERT INTO nlogs (username, actions, "natureOfCollection", amount, payor, transtime) VALUES (%s,%s,%s,%s,%s,current_timestamp)''', (g.user,action,noc,amt,payor,))          
        conn.commit()
        conn.close()
        return redirect('/delinquency')







@app.route("/delinquency/pay",methods=['POST','GET'])
def payD():
    if request.method=="POST":
        amount=request.form['postAmount']
        year=request.form['year']
        quarter=request.form['quarter']
        conn = psycopg2.connect("dbname = 'AF51' user = 'postgres' password = 'carrotcake092814' host = 'localhost' port = '5432'")
        cur=conn.cursor()
        if quarter == 'q1':
            cur.execute("UPDATE tax SET quarter1=%s  WHERE year=%s",(amount,year))
            conn.commit()
            conn.close()
        elif quarter == 'q2':
            cur.execute("UPDATE tax SET quarter2=%s  WHERE year=%s",(amount,year))
            conn.commit()
            conn.close()
        elif quarter == 'q3':
            cur.execute("UPDATE tax SET quarter3=%s  WHERE year=%s",(amount,year))
            conn.commit()
            conn.close()
        elif quarter == 'q4':
            cur.execute("UPDATE tax SET quarter4=%s WHERE year=%s",(amount,year))
            conn.commit()
            conn.close()
        return redirect('/delinquency')






