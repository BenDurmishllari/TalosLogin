from Talos import app, db, mail
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
                   abort,
                   session)
from flask_login import (login_user, 
                         logout_user, 
                         login_required, 
                         current_user)
from flask_mail import Mail, Message
import math, random 
import re


emailValidator = EmailValidator()
passwordValidator = PasswordValidator()

key = b'TX94plX7njPJ0e5H1egJXikQm7qy1t5k91DBAlPGiV8='
current_userData = {}


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
    global current_userData
    validationMessage = ""
    currentUserEmail = ""
    currentUserPassword = ""

    if request.method == 'POST':

        email = request.form['txtEmail']
        password = request.form['txtPassword']
        f = Fernet(key)
        users = User.query.all()
       
        string = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
        oneTimeUsedCode = "" 
        length = len(string) 
        for i in range(4): 
            oneTimeUsedCode += string[math.floor(random.random() * length)] 
        datas = {}
        for user in users:

            decryptUserNames = f.decrypt(user.name)
            decryptUserSurnames = f.decrypt(user.surname)
            decryptUserEmails = f.decrypt(user.email)
            decryptUserPasswords = f.decrypt(user.password)

            usersName = decryptUserNames.decode('ascii')
            usersSurname = decryptUserSurnames.decode('ascii')
            usersEmail = decryptUserEmails.decode('ascii')
            usersPassword = decryptUserPasswords.decode('ascii')

            datas[user.id] = usersName, usersSurname, usersEmail, usersPassword
        for k,v in datas.items():
            if email in v:
                rowID = k
                current_userData[rowID] = [v[0], v[1], v[2], v[3]]
                currentUserEmail = v[2]
            if password in v:
                currentUserPassword = v[3]
        

        if email == "" and password == "":
            validationMessage = "Please fil the fields"
        elif email == "":
            validationMessage = "Please fill the email field"
        elif password == "":
            validationMessage = "Please fill the password field"
        else:
            for k,v in current_userData.items():
                if email not in v and password not in v:
                    validationMessage = "Wrong credentials, please try again"
                elif email not in v:
                    validationMessage = "Wrong Email, please try again"
                elif password not in v:
                    validationMessage = "Wrong Password, please try again"
                else:
                    if email in v and password in v:
                        
                        user = User.query.filter_by(id = k).first()
                        session['current_userId'] = k
                        session['oneTimeCode'] = oneTimeUsedCode
                        current_userData[rowID].append(oneTimeUsedCode)
                        # print(current_userData)
                        login_user(user)
                        # print(user)
                        message = Message('Request to reset your password',
                            sender = 'badasslevelover9000@outlook.com', 
                            recipients = [currentUserEmail])


                        message.body = f''' Please add the code on the website in order to login:
                        
                        Code:''' + " " + oneTimeUsedCode  + f'''
                        
                        
                        This is an email to login on Talos website, if you didn't make this request ignore this email and contact the administrator
                        '''

                        mail.send(message)
                        # print(current_userData)
                        # print("-------------------")
                        # print(session['current_userId'])
                        # print("----------------")
                        # print(session['oneTimeCode'])
                        return redirect(url_for('verify'))
                    # else:
                    #     validationMessage = "Wrong credentials"

    return render_template('loginPage.html', validationMessage=validationMessage)

@app.route('/verify', methods=['GET', 'POST'])
def verify():

    global current_userData
    if request.method == 'POST':

        code = request.form['txtCode']
        oneTimeCodeFromSession = session.get('oneTimeCode')
        cUserIdFromSession = session.get('current_userId')

        for k,v in current_userData.items():
            codeFromData = v[4]
        
        if code == oneTimeCodeFromSession and code == codeFromData:
            return redirect(url_for('home'))
        else:
            print("malakia")


    return render_template ('authPage.html')

@app.route('/home', methods=['GET', 'POST'])
def home():

    return render_template ('homePage.html')



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

    