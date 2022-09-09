#####alle Benötigten Module werden importiert
from tokenize import String
from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from flask_mysqldb import MySQL
import MySQLdb.cursors
from . import mysql
from .models import User

auth = Blueprint('auth', __name__)

##Route für Logout mit Bedingungen
@auth.route('/logout')
def logout():
    session['loggedin'] = False
    session['userid'] = 0
    session['email'] = None
    return redirect(url_for('auth.login'))

##Route zum login wird gesetz
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM pythondb.user where Email = %s", (email,))
        result = cursor.fetchone()  
        user = User(id = result["Id"], email = result["Email"], password = result["Password"], firstname = result["Firstname"])
    
        if user.id != 0:     
            if check_password_hash(user.password, password):
                flash('Erfolgreich eingeloggt!', category='success')
                session['loggedin'] = True
                session['userid'] = user.id
                session['email'] = user.email
                return redirect(url_for('views.home'))
            else:
                flash('Passwort ist falsch, versuch es noch einmal.', category='error')
        else:
            flash('Email existiert nicht.', category='error')

    return render_template("login.html", user=current_user)


#####Password Policy & Mail Bedingungen
@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM pythondb.user where Email = %s", (email,))
        result = cursor.fetchall() 
        
        user = User(0,"","","")
        for row in result:          
            user = User(row['Id'], row['Email'], row['Password'], row['Firstname'])

        if user.id != 0:  
            flash('Email existiert bereits.', category='error')
        elif len(email) < 4:
            flash('Email must länger als 3 Zeichen sein', category='error')
        elif len(first_name) < 2:
            flash('Vorname muss länger als 1 Zeichen sein.', category='error')
        elif password1 != password2:
            flash('Passwords stimmt nicht überein.', category='error')
        elif len(password1) < 7:
            flash('Password muss länger als 7 Zeichen sein.', category='error')
        else:
            query = "INSERT INTO pythondb.user (Email, Password, Firstname) Values (%s, %s, %s)"
            val = (email, generate_password_hash(password1, method='sha256'), first_name)
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            result = cursor.execute(query, val)      
            mysql.connection.commit()
            cursor.close()  
            flash('Account erstellt!', category='success')          
            return redirect(url_for('auth.login'))

    return render_template("sign_up.html", user=current_user)

        
