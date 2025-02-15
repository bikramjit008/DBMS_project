from flask import Flask, render_template, request, redirect, session
import mysql.connector
import os


app = Flask(__name__)
app.secret_key = os.urandom(24)


conn = mysql.connector.connect(host='localhost', user="root",
                               password="bikutubai@008", database="Toll_Tax")

cursor = conn.cursor()


@app.route('/')
def home():
    return render_template('interface.html')


@app.route('/signup')
def sign_up():
    return render_template('signup.html')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/user')
def user():
    if 'user_id' in session:
        return render_template('user_interface.html')
    else:
        return redirect('/')


@app.route('/vehicle_register')
def vehicle():
    return render_template('vehicle_register.html')


@app.route('/payment')
def payment():
    return render_template('Pay_toll.html')


@app.route('/login_validation', methods=['POST'])
def login_validation():
    userid = request.form.get('user_id')
    password = request.form.get('password')
    cursor.execute("""SELECT * FROM `User` WHERE `user_ID` LIKE '{}' AND `Password` LIKE '{}'"""
                   .format(userid, password))
    users = cursor.fetchall()
    if len(users) > 0:
        session['user_id'] = users[0][0]
        return redirect('/user')
    else:
        return redirect('/')


@app.route('/add_user', methods=['POST'])
def add_user():
    userid = request.form.get('auser_id')
    name = request.form.get('auser_name')
    email = request.form.get('auser_email')
    password = request.form.get('apassworrd')

    cursor.execute("""INSERT INTO `User` (`user_ID`, `user_Name`, `user_Email`, `Password`) VALUES
    ('{}', '{}', '{}', '{}')""".format(userid, name, email, password))
    conn.commit()

    cursor.execute("""SELECT * FROM `User` WHERE `user_ID` LIKE '{}'""".format(userid))
    myuser = cursor.fetchall()
    session['user_id'] = myuser[0][0]
    return redirect('login')


@app.route('/add_vehicle_details', methods=['POST'])
def add_vehicle():
    reg_no = request.form.get('reg_no')
    veh_type = request.form.get('v_type')
    mod_no = request.form.get('m_no')
    user_id = session['user_id']

    cursor.execute("""INSERT INTO `Vehicle` (`reg_no`, `vehicle_Type`, `model_No`, `user_ID`) VALUES
    ('{}', '{}', '{}', '{}')""".format(reg_no, veh_type, mod_no, user_id))
    conn.commit()
    session['reg_no'] = reg_no
    return redirect('/user')


if __name__ == "__main__":
    app.run(debug=True)
