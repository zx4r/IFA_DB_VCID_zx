from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for, session
from flask_login import login_required, current_user
from .models import Note, User
from . import mysql
import MySQLdb.cursors
import json

views = Blueprint('views', __name__)
noteList = []

@views.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST' and session['userid'] != 0:
        note = request.form.get('note')
        if note is None:
            getAllNotes(session)
            return render_template("home.html", noteAllList = noteList)
        if len(note) < 1:
            flash('Beitrag zu kurz!', category='error')
            getAllNotes(session)
            return render_template("home.html", noteAllList = noteList)
        else: 
            query = "INSERT INTO pythondb.note (Data, UserId) Values (%s, %s)"
            val = (note, session['userid'])
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute(query, val)      
            mysql.connection.commit()
            cursor.close()
            flash('Beitrag hinzugefügt!', category='success')  
            getAllNotes(session)
            return render_template("home.html", noteAllList = noteList)    
    if  session.get('userid') == None or session.get('userid') == 0:
        return redirect(url_for('auth.logout'))
    else:
        getAllNotes(session)
        return render_template("home.html", noteAllList = noteList)

@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("Delete from pythondb.note where Id = %s", (note['noteId'],))
    mysql.connection.commit()
    cursor.close()
    return jsonify({})

@views.route('/news', methods=['GET', 'POST'])
def news():
    flash('Das Menü wird hier dargestellt')
    return render_template("news.html", user=current_user)

def getAllNotes(session):
    del noteList[:]
    if  session.get('userid') == None or session['userid'] == 0:
        return   
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM pythondb.note where UserId = %s", (session['userid'],))
    result = cursor.fetchall() 
    for item in result:
        noteList.append(item)
    return

