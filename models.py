import psycopg2
from flask_sqlalchemy import SQLAlchemy
from configparser import ConfigParser
from forms import CreateAccount
from flask_bootstrap import Bootstrap
from flask_wtf import Form
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired
# from app import db
# from app import app

# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:carrotcake092814@localhost:5432/AF51'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SECRET_KEY'] = 'flaskimplement'
# app.debug = True
# db = SQLAlchemy(app)


#ent = Entry(receiptno, payor,officer, paymentmethod, collectiondate,message, nature_list)


class Entry(object):
    def __init__(self, receiptno, payor, officer, paymentmethod, collectiondate, message):

        self.receiptno = receiptno
        self.payor = payor
        self.officer = officer
        self.paymentmethod = paymentmethod
        self.collectiondate = collectiondate
        self.message = message

class FormForm(object):
    def __init__(self, payor, paymentmethod, receiptno, officer, collectiondate, nature, message):
      
        self.payor = payor
        self.paymentmethod = paymentmethod
        self.receiptno = receiptno
        self.officer = officer
        self.collectiondate = collectiondate
        self.nature = nature
        self.message = message


class EntryP(object):
    def __init__(self, nofcollection, nover, over, officer):

        self.nofcollection = nofcollection
        self.nover = nover
        self.over = over
        self.officer = officer



class formType(object):
    def __init__(self, noc, amount):

        self.noc = noc
        self.amount = amount


class EntryF(object):
    def __init__(self, noc, amount):

        self.noc = noc
        self.amount = amount


class EntryB(object):
    def __init__(self, cn, txp, tn, rp, ba, bgy, ctgy, ha, memo, vu, officer):

        self.cn = cn
        self.txp = txp
        self.tn = tn
        self.rp = rp
        self.ba = ba
        self.bgy = bgy
        self.ctgy = ctgy
        self.memo = memo
        self.vu = vu
        self.officer = officer




class Register(Form):
    firstname = StringField('firstname',validators=[InputRequired()])
    middlename = StringField('middlename',validators=[InputRequired()])
    lastname = StringField('lastname',validators=[InputRequired()])
    username = StringField('username',validators=[InputRequired()])
    password = StringField('password',validators=[InputRequired()])
    officerrole = StringField('officerrole',validators=[InputRequired()])









 
if __name__ == '__main__':
    connect()
