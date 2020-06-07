from Talos import app, db
from Talos.model import User
from Talos.validators import EmailValidator, PasswordValidator
from password_strength import PasswordStats
from cryptography.fernet import Fernet
from flask import (render_template, 
                   redirect, 
                   url_for, 
                   request, 
                   flash, 
                   request, 
                   abort)
import re


emailValidator = EmailValidator()
passwordValidator = PasswordValidator()

key = b'TX94plX7njPJ0e5H1egJXikQm7qy1t5k91DBAlPGiV8='



# @app.after_request
# def add_header(r):
#     """
#     Add headers to both force latest IE rendering engine or Chrome Frame,
#     and also to cache the rendered page for 10 minutes.
#     """
#     r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
#     r.headers["Pragma"] = "no-cache"
#     r.headers["Expires"] = "0"
#     r.headers['Cache-Control'] = 'public, max-age=0'
#     return r

btnChecker = False

@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    global key
    validationMessage = ""
    currentUserEmail = ""
    currentUserPassword = ""
    if request.method == 'POST':

        email = request.form['txtEmail']
        password = request.form['txtPassword']
        f = Fernet(key)
        users = User.query.all()
        datas = {}
        for user in users:

            decryptUserEmail = f.decrypt(user.email)
            decryptUserPassword = f.decrypt(user.password)

            usersEmail = decryptUserEmail.decode('ascii')
            usersPassword = decryptUserPassword.decode('ascii')

            datas[usersEmail] = usersPassword 
        print(datas)
        for k,v in datas.items():
            if email in k:
                currentUserEmail = k
            if password in v:
                currentUserPassword = v
        # print(currentUserEmail)
        # print(currentUserPassword)
        
        if email == "" and password == "":
            validationMessage = "Please fil the fields"
        elif email == "":
            validationMessage = "Please fill the email field"
        elif password == "":
            validationMessage = "Please fill the password field"
        elif email not in currentUserEmail:
            validationMessage = "Wrong Email, please try again"
        elif password not in currentUserPassword:
            validationMessage = "Wrong Password, please try again"
        else:
            if email == currentUserEmail and password == currentUserPassword:
                
                return redirect(url_for('verify'))
    


    return render_template('loginPage.html', validationMessage=validationMessage)

@app.route('/verify', methods=['GET', 'POST'])
def verify():
    return render_template ('authPage.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    validationMessage = ""
    global btnChecker
    passwordStrenght = 0
    passFlag = False
    global key
    if request.method == 'POST':

        name = request.form['txtName']
        surname = request.form['txtSurname']
        email = request.form['txtEmail']
        password = request.form['txtPassword']
        confirmPassword = request.form['txtconfirmPassword']
        

        if 'btnCheckPassword' in request.form:
            btnChecker = True
            passFlag = True
            results = passwordValidator.checkPassword(password)
            # passwordStrenght = round(passwordStrongLevel.checkStrongLevelPassword(password).strength(),2)
            # print(passwordStrenght)
            validationMessage = results[0]
            passwordlvl = results[1]
            # error otan patas to koubi vale try
            passwordStrenght = round(passwordlvl.strength(), 2)
        
        if 'btnRegister' in request.form:
            if btnChecker == True:
        
                if name  != "" and surname  != "" and email  != "" and password  != "" and confirmPassword != "":
                  
                    if password == confirmPassword:
                        checkInputEmail = emailValidator.checkEmail(email)
                        if checkInputEmail == "Email is valid!":

                            # key = Fernet.generate_key()
                            f = Fernet(key)
                            encryptName = f.encrypt(name.encode('ascii'))
                            encryptSurname = f.encrypt(surname.encode('ascii'))
                            encryptEmail = f.encrypt(email.encode('ascii'))
                            encryptPassword = f.encrypt(password.encode('ascii'))


                            user = User(name = encryptName,
                                        surname = encryptSurname,
                                        email = encryptEmail,
                                        password = encryptPassword)

                            db.session.add(user)
                            db.session.commit()
                            return redirect (url_for('login'))
                        else:
                            validationMessage = checkInputEmail
                    else:
                        validationMessage = "Password don't match"
                else:
                    if name == "" and surname == "" and email == "" and password == "" and confirmPassword == "":
                        flash('Please fil all the fields', 'danger')
                    else:
                        if name == "":
                            validationMessage = "Please add your name!"
                        if surname == "" :
                            validationMessage = "Please add your surname!"
                        if email == "":
                            validationMessage = "Please add your email!"
                        if password == "":
                            validationMessage = "Please add your password!"
                        if confirmPassword == "":
                            validationMessage = "Please confirm password!"
            else:
                validationMessage = "Please check your password before register"
            

    return render_template('registerPage.html', validationMessage=validationMessage, passwordStrenght=passwordStrenght,passFlag=passFlag )

    