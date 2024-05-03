from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3 as sql
import subprocess
import sys
import datetime

app = Flask(__name__)

# cur.execute('create table user(Firstname varchar(50), Lastname varchar(50), Email varchar(50), Phone int, Username varchar(50), Password varchar(50), Age int, Nation varchar(50));')
# conn.commit()

session=[]
reminders = []
# Color_Constants
PRIMARY_COLOR = '#3498db'
SECONDARY_COLOR = '#e74c3c'
BACKGROUND_COLOR = '#ecf0f1'
TEXT_COLOR = '#2c3e50'

@app.route('/')
def cover():
    return render_template('home.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/home2',methods=['GET','POST'])
def home2():
    if request.method == 'POST' and 'Tower-of-hanoi' in request.form:
        subprocess.run(['python', 'Tower-of-hanoi.py'])
    elif request.method == 'POST' and 'space_invaders' in request.form:
        subprocess.run(['python', 'space_invaders.py'])
    elif request.method == 'POST' and 'wordle' in request.form:
        subprocess.run(['python', 'wordle.py'])
    elif request.method == 'POST' and 'flappy_bird' in request.form:
        subprocess.run(['python', 'FlappyBird.py'])
    return render_template('home2.html')

@app.route('/act_kids',methods=['GET','POST'])
def act_kids():
    return render_template('act_kids.html')

@app.route('/act_adults',methods=['GET','POST'])
def act_adults():
    return render_template('act_adults.html')

@app.route('/logout',methods=['GET','POST'])
def logout():
    return render_template('home.html')

@app.route('/login',methods=['GET','POST'])
def login():
    conn = sql.connect('geek.db')
    cur = conn.cursor()
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        res=cur.execute('select Username,Password from user')
        for i in res:
            print(i)
            if username==i[0] and password==i[1]:
                msg = 'Logged in successfully !'
                conn.close()
                session.append(username)
                return redirect("/home2") 
        else:
            msg = 'Incorrect username / password !'
        conn.close()
    return render_template('login.html', msg = msg)

@app.route('/signup', methods =['GET', 'POST'])
def signup():
    conn = sql.connect('geek.db')
    cur = conn.cursor()
    msg = ''
    flag=False
    if request.method == 'POST' and 'username' in request.form and 'confirmPassword' in request.form and 'password' in request.form and 'email' in request.form and  'phone' in request.form  and 'firstname' in request.form and 'lastname' in request.form and 'age' in request.form and 'nation' in request.form:
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        phone = request.form['phone']
        username = request.form['username']
        password = request.form['password']
        c_password = request.form['confirmPassword']
        age = request.form['age']
        nation = request.form['nation']
        print(c_password,password)
        if(password!=c_password):
            msg='The 2 passwords are not the same. Please enter the same password !'
            return render_template('signup.html',msg=msg)
        res=cur.execute('select Username from user')
        for i in res:
            if(username in i):
                msg='Username already exists'
                flag=True
                break
        if(flag==False):
            cur.execute('insert into user(Firstname, Lastname, Email, Phone, Username, Password, Age, Nation) values(?,?,?,?,?,?,?,?)',(firstname,lastname,email,phone,username,password,age,nation))
            msg = 'You have successfully registered !'
            conn.commit()
            conn.close()
            return render_template('login.html')
    else:
        msg = 'Please fill out the form !'
        return render_template('signup.html', msg = msg)
    return render_template('signup.html', msg = msg)

@app.route('/profile')
def profile():
    conn = sql.connect('geek.db')
    cur = conn.cursor()
    res=cur.execute('select * from user where username==(?)',(session[0],))
    user=[i for i in res]
    print(user)
    conn.close()
    return render_template('profile.html',user=user)

@app.route('/index')
def index():
    return render_template('index.html', reminders=reminders, primary_color=PRIMARY_COLOR, secondary_color=SECONDARY_COLOR, background_color=BACKGROUND_COLOR, text_color=TEXT_COLOR)

@app.route('/set_reminder', methods=['POST'])
def set_reminder():
    text = request.form.get('reminder')
    date_str = request.form.get('date')
    time_str = request.form.get('time')
    duration = int(request.form.get('duration'))

    if text and date_str and time_str:
        datetime_str = f'{date_str} {time_str}'
        reminder_datetime = datetime.datetime.strptime(datetime_str, '%Y-%m-%d %H:%M')
        end_datetime = reminder_datetime + datetime.timedelta(minutes=duration)

        reminders.append({
            'text': text,
            'datetime': reminder_datetime.strftime('%Y-%m-%d %H:%M'),
            'duration': duration
        })

        

    return redirect(url_for('index'))

@app.route('/delete_reminder/<int:index>')
def delete_reminder(index):
    reminders.pop(index)
    return redirect(url_for('index'))

if __name__=="__main__":
    app.run(debug=True)
