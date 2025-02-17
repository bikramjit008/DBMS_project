from flask import Flask, render_template, request, redirect, session, flash
import mysql.connector
import os
from datetime import datetime
import random


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
        uid_ = session['user_id']
        cursor.execute("""SELECT * FROM `User` WHERE `user_ID` LIKE '{}'""".format(uid_))
        user_det = cursor.fetchall()
        cursor.execute("""SELECT * FROM `Vehicle` WHERE `user_ID` LIKE '{}'""".format(user_det[0][0]))
        veh_det = cursor.fetchall()
        so = len(veh_det) > 0
        if so:
            regn_no = veh_det[0][0]
            cursor.execute("""SELECT * FROM `Payment` WHERE `reg_No` LIKE '{}'""".format(regn_no))
            ss = cursor.fetchall()
            pay = len(ss) > 0
        else:
            pay = False
        return render_template('user_interface.html', det=user_det, p=pay, v=so)
    else:
        return redirect('/')


@app.route('/vehicle_register')
def vehicle():
    uid = session['user_id']
    cursor.execute("""SELECT * FROM `Vehicle` WHERE `user_ID` LIKE '{}'""".format(uid))
    regno = cursor.fetchall()
    if len(regno) > 0:
        flash("Your Vehicle is already registered.", 'error')
        return redirect('/user')
    else:
        return render_template('vehicle_register.html')


@app.route('/payment')
def payment():
    uid = session['user_id']
    cursor.execute("""SELECT * FROM `Vehicle` WHERE `user_ID` LIKE '{}'""".format(uid))
    regno = cursor.fetchall()
    return render_template('Pay_toll.html', regn=regno[0][0], date=datetime.now().date())


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
    return redirect('/user')


@app.route('/payment_validation', methods=['GET', 'POST'])
def payment_validation():
    uid = session['user_id']
    cursor.execute("""SELECT * FROM `Vehicle` WHERE `user_ID` LIKE '{}'""".format(uid))
    regno = cursor.fetchall()
    if len(regno) > 0:
        return redirect('/payment')
    else:
        flash("Please register your Vehicle first.", 'error')
        return redirect('/user')


@app.route('/payment_details', methods=['POST'])
def pay_det():
    reg_no = request.form.get('reg_no')
    dist = request.form.get('dis')
    amo = request.form.get('amount')
    date = datetime.now().date()
    pid = random.randint(10**9, 10**10 - 1)
    cursor.execute("""INSERT INTO `Payment` (`payment_Id`, `payment_Amount`, `distance`, `payment_Date`,`reg_No`) VALUES
        ('{}', '{}', '{}', '{}','{}')""".format(pid, amo, dist, date, reg_no))
    conn.commit()
    return redirect('/user')


if __name__ == "__main__":
    app.run(debug=True)
