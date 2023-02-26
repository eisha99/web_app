
#setting up flask
from flask_sqlalchemy import SQLAlchemy
import os 
from flask import Flask, render_template, request, redirect, url_for, flash, session, abort
from app import db,app
from app.db_models import User, Task
from flask_login import current_user, login_user, logout_user, login_required


@app.route('/')
def index():
    """ 
     This is the main page of the website. It handles logins for the users
    """
    #checks whether the user is in session (logged in)
    if 'username' not in session:
        return render_template('welcome.html') #automatically takes one to welcome page first
    else:
        tasks = db.session.query(Task).filter(Task.username==session.get('username'))
        #print(session["username"])

    return render_template("index.html", user=session.get('username'))


@app.route('/resources')
def resources():
    """ 
     This is the resources page, it redirects users to Youtube videos and application guides.
    """
    return render_template('resources.html') 

@app.route('/mentorship')
def mentorship():
    """ 
     This is the mentorship page where users can sign up for a mentee or mentor position.
    """
    return render_template('mentorship.html') 


@app.route('/chats')
def chats():
    """ 
     This is the chats page where studwent can access our Whatsapp and Telegram channels.
    """
    return render_template('chats.html') 

@app.route('/opportunities')
def opportunities():
    """ 
     This is where we will link our expert chat system that redirects students to the most suitable scholarship opportunities
    """
    return render_template('opportunities.html') 

# TODO add encryption for the password
@app.route('/signup', methods=["GET","POST"])
def sign_up():
    """ 
     Creating a page for signing up users
    """
    if request.method == 'POST':
        user = db.session.query(User).filter(User.username==request.form['username']).first()
        if not user: #we request a username and password from the user
            user = User(username = request.form['username'], password = request.form['password'])
            db.session.add(user) #the sessions starts for the user
            db.session.commit()
            session['username'] = user.username
            flash('Successful login!')
            return redirect(url_for('index'))
        else: #if there is an existing username then we ask the user to provide a different one
            flash('This username is taken. Please use a different one!')
            return render_template("signup.html")
    else:
        return render_template("signup.html")

@app.route('/login', methods = ['GET','POST'])
def login(): 
    """ 
        Creating a page for logging in
    """
    error = None
    if request.method == 'POST':
        user = db.session.query(User).filter(User.username==request.form['username']).first()
        if not user:
            flash('Username is invalid')
            error = 'Error: invalid username/password'
            # no need to redirect bc already on login page
        elif user.password == request.form['password']:

            # log in
            #app.logger.info(session['username'])
            session['username'] = user.username
            app.logger.info(session['username'])
            #flash('Login successful')

            return redirect(url_for("index")) #once successfully logged in the user can view the website
        else:
            flash('The password is incorrect!')
            error = 'Invalid username/password'

    return render_template("login.html", error = error)

@app.route('/logout')
def log_out():
    """
        Creating a page for logout for users
    """
    
    session.pop('username', None) #we simply remove the username
    return redirect(url_for('index'))



if __name__ == '__main__':
    app.run(debug=True)


