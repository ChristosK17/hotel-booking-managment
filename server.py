from flask import Flask, render_template, redirect, url_for, request, session
import random
import hotel

numbers = [32, 45, 34 , 345, 23, 45, 234, 5234, 532, 45, 2345, 234, 523, 453, 245]
types = ["Single", "Double", "Triple", "Quad", "Queen", "King", "Twin", "Hollywood Twin Room", "Double-double", "Studio", "Suite - Executive Suite", "Mini Suite - Junior Suite", "President Suite - Presidential Suite", "Apartments - Room for Extended Stay", "Connecting rooms", "Murphy Room", "Accessible Room - Disabled Room", "Cabana", "Adjoining rooms", "Adjacent rooms", "Villa", "Executive Floor - Floored Room", "Smoking", "Non-Smoking Room"]

mydb = hotel.DB()


app = Flask(__name__)

app.config['SECRET_KEY'] = "hard-to-guess"

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/login', methods=["GET", "POST"])
def login():
    error=None
    try:
        if request.method == "POST":
            username = request.form['USERNAME']
            password = request.form['PASSWORD']
            print(username, password)
            if username == "admin" and password == "admin":
                return redirect(url_for('controlpanel'))
            else:
                return redirect(url_for('home'))
        return render_template('login.html', error=error)

    except Exception as e:
        print(e)
        return render_template('login.html', error=error)

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/test')
def test():
    return render_template('test.html', user_name = random.randint(1, 10), numbers=numbers, user=random.randint(0, 1))

@app.route('/user/<name>')
def user(name):
    return "Καλή σου μέρα {}!".format(name)

@app.route('/controlpanel', methods=["GET", "POST"])
def controlpanel():
    error=None
    try:
        if request.method == "POST":
            print("getting info")
            try:
                id = int(request.form['ID'])
                beds = int(request.form['BEDS'])
                type = str(request.form['TYPE'])
                cost = int(request.form['COST'])
                state = int(0 if None == request.form.get('STATE') else 1)
                print(id, beds, type, cost, state)
                mydb.add_room(hotel.Room(id, beds, type, cost, state))
            except Exception as e:
                print("False data for ADD")

            try:
                e_id = int(request.form['eID'])
                e_state = int(0 if None == request.form.get('eSTATE') else 1)
                print(e_id, e_state)
                try:
                    mydb.update_room_availability(e_id, e_state)
                except Exception as e:
                    print("Error", e)
            except Exception as e:
                print("False data for EDIT")

            try:
                d_id = request.form['dID']
                print(d_id)
                try:
                    mydb.delete_room_by_id(d_id)
                except Exception as e:
                    print("Error", e)
            except Exception as e:
                print("False data for DELETE")

            
        return render_template('controlpanel.html', types=types, rooms=mydb.get_all("o"), error=error)
    except Exception as e:
        print(e)
        return render_template('controlpanel.html', types=types, rooms=mydb.get_all("o"), error=error)

@app.route('/getdata', methods=["GET", "POST"])
def getdata():
    error=None
    try:
        if request.method == "POST":
            userdata = request.form['levar']
            print(userdata)
        return render_template('getdata.html', error=userdata)

    except Exception as e:
        print(e)
        return render_template('getdata.html', error=error)

if __name__ == "__main__":
    app.run(debug=True)

