import psycopg2
import psycopg2.extras
from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('transaction.html')

@app.route('/transact', methods=['POST', 'GET'])
def transact():
    if request.method == 'POST':
        try:
            start_date = request.form['start']
            end_date = request.form['end']

            print start_date
            print end_date
            conn = psycopg2.connect(database="test", user="postgres", password="coycoy6197", host="localhost", port="5432")
            cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cur.execute("""SELECT * FROM payments WHERE date BETWEEN  %s AND %s""", (start_date,end_date))
            rows = cur.fetchall()
            conn.close()
            print rows

        except:
            print ("Error")

        finally:
            msg = ("From " + start_date + " To " + end_date + "")
            return render_template('result.html', rows=rows, msg=msg)

if __name__ == "__main__":
    app.run(debug=True)
