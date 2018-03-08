# -*- coding: utf-8 -*- u
import os
from firebase import firebase
from flask import Flask, render_template, request, flash,session,redirect,url_for
import psycopg2
import json
from pprint import pprint
import datetime




from firebase import firebase
firebase = firebase.FirebaseApplication('https://hoteltwoway-65c5b.firebaseio.com', None)

app = Flask(__name__)



@app.route('/', methods=['GET','POST'])
def home(username=None):
    if request.method == 'POST':
        session.pop('user', None)
        user_candidate= request.form['username']
        pass_candidate = request.form['password']
        conn = psycopg2.connect(database = "ispector", user = "postgres", password = "carrotcake092814", host = "127.0.0.1", port = "5432")
        print "Opened database successfully"
        print user_candidate
        print pass_candidate
        cur = conn.cursor()

        user1=cur.execute("""SELECT * FROM users WHERE user_id=%s""", (user_candidate,))
        pass1=cur.execute("""SELECT * FROM users WHERE pass=%s""",(pass_candidate,))
        data=cur.fetchone()
        conn.close()
        print user1
        print pass1
        print data
        try:
            
            if user_candidate is '':
                return render_template("req_username.html")
            elif pass_candidate is '':
                return render_template("req_password.html")
            elif user_candidate not in data and pass_candidate not in data:
                session['user'] = request.form['username']
                return render_template("error_input.html")
            elif user_candidate  in data and pass_candidate  in data:
                session['user'] = request.form['username']
                return render_template("index.html")
            elif user_candidate not in username:
                return render_template("error_input.html")
        except Exception:
            return render_template("error_input.html")
    else:
        return render_template("login.html")


@app.route('/landing')
def landing():
    if g.user:
        return render_template("index.html")

    return redirect(url_for('home'))


@app.route('/logout')
def logout():
    session.pop('user',None)
    return redirect(url_for('home'))




@app.route("/room1")
def room1():



#USE THIS LATER
#%b %d, %Y %I:%M:%S %p
    result1date = firebase.get('/Rooms/Room1/', None)

    for key in result1date.keys():
        key = sorted(result1date.keys())[-2]
    	currentdate = key

        print currentdate

    result1 = firebase.get('/Rooms/Room1/' + currentdate + '/Inspection/Scan-in/Inspector/', None)
    result2 = firebase.get('/Rooms/Room1/' + currentdate + '/Inspection/Scan-out/Inspector/', None)
    print result1


    print currentdate

    for key in result1.keys():
       inspector = key
    timeout = result2[inspector]["Time"]

    # for key in result1date.keys():
    #    Date = key

 


  

    for key in result1datetime.keys():
        key = sorted(result1datetime.keys())[-2]
        time = key
        print time

   

    print time

 





    FMT = '%b %d, %Y %I:%M:%S %p'
    timedif = datetime.datetime.strptime(time, FMT) - datetime.datetime.strptime(timeout, FMT)

    










    return render_template('newnew.html', result1=result1, result2=result2,inspector=inspector, date=currentdate, time=time, timeout=timeout, timedif = timedif)



if __name__ == '__main__':
   app.secret_key = 'super secret key'
   app.run()