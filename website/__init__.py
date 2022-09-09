from flask import Flask
from os import path
from flask_mysqldb import MySQL
from website.models import User, Note


####SQL DB wird erstellt
app = Flask(__name__)  

mysql = MySQL()
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'nvd4FAn6bhSZeLL8Ki'
app.config['MYSQL_DB'] = 'pythondb'
mysql = MySQL(app)

###APP wird erstellt & Vorlagen für das Design
def create_app():     
    app.config['SECRET_KEY'] = 'IFA_DB_2022_VCID$'   
    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    
    return app



