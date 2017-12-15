from flask import *
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123nanana@localhost/dblogs'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(50), unique=False)
    middlename = db.Column(db.String(50), unique=False)
    lastname = db.Column(db.String(50), unique=False)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String, unique=True)
    address = db.Column(db.String, unique=False)
    contactno = db.Column(db.String, unique=False)

    def __init__(self, firstname, middlename, lastname, username, password, address, contactno):
        self.firstname = firstname
        self.middlename = middlename
        self.lastname = lastname
        self.username = username
        self.password = password
        self.address = address
        self.contactno = contactno

    def __repr__(self):
        return '<User %r>' % self.username




# Returns the add_user.html
@app.route('/')
def index():
    return render_template('add_user.html')


# Displays the table
@app.route('/view')
def view():
    myUser = User.query.all()
    return render_template('view.html', myUser=myUser)



# Adds a user
@app.route('/post_user', methods=['POST'])
def post_user():
    user = User(request.form['firstname'], request.form['middlename'], request.form['lastname'], request.form['username'], request.form['password'], request.form['address'], request.form['contactno'])
    db.session.add(user)
    db.session.commit()
    return render_template('add_user.html')



# Gets the id of the user then pass it to the updateform.html
@app.route('/edit')
def edit():
        id = request.args.get('id')
        return render_template('updateform.html', id=id)



# Updates the information entered in updateform.html
@app.route('/update_row', methods=['GET','POST'])
def update_row():
    id = request.args.get('id')
    if request.method == 'POST':
        record = User.query.filter_by(id=id).first_or_404()

        record.firstname = request.form.get('firstname')
        record.middlename = request.form.get('middlename')
        record.lastname = request.form.get('lastname')
        record.username = request.form.get('username')
        record.password = request.form.get('password')
        record.address = request.form.get('address')
        record.contactno = request.form.get('contactno')

        db.session.commit()

    return render_template('add_user.html')


if __name__ == '__main__':
    app.run(debug=True)