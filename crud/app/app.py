from flask import Blueprint, Flask, request, session, redirect, url_for, abort, render_template, flash
from pymysql import MySQLError
from models import User
import config
from exts import db
from blueprints.user import bp



app = Flask(__name__)
app.config.from_object(config)
db.__init__(app)
app.register_blueprint(bp)


@app.route('/',methods=['GET', 'POST'])
def index():
    
    return render_template("index.html")


# @app.before_request
# def before_request():
#     try:
        
#         username = session.get("username")
#         print ("username")
        
#     except:
#         usernmae = None  
        
        
        
if __name__ == '__main__':
    app.run(port=8001,  debug=True)
