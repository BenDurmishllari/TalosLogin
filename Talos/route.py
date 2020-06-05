from Talos import app, db
from Talos.model import User
from flask import (render_template, 
                   redirect, 
                   url_for, 
                   request, 
                   flash, 
                   request, 
                   abort)


@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():

    

    

    return render_template('loginPage.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    validationMessage = ""
    if request.method == 'POST':
        
        name = request.form['txtName']
        surname = request.form['txtSurname']
        email = request.form['txtEmail']
        password = request.form['txtPassword']
        confirmPassword = request.form['txtconfirmPassword']

        if name  != "" and surname  != "" and email  != "" and password  != "" and confirmPassword != "":
            if password == confirmPassword:
                user = User(name = name,
                            surname = surname,
                            email = email,
                            password = password)

                db.session.add(user)
                db.session.commit()
                return redirect (url_for('login'))
            else:
                validationMessage = "Password don't match"
        else:
            print("1")
            if name == "" and surname == "" and email == "" and password == "" and confirmPassword == "":
                print("2")
                flash('Please fil all the fields', 'danger')
            else:
                if name == "":
                    print("3")
                    validationMessage = "Please add your name!"
                if surname == "" :
                    print("4")
                    validationMessage = "Please add your surname!"
                if email == "":
                    print("5")
                    validationMessage = "Please add your email!"
                if password == "":
                    print("6")
                    validationMessage = "Please add your password!"
                if confirmPassword == "":
                    print("7")
                    validationMessage = "Please confirm password!"
            

    return render_template('registerPage.html', validationMessage=validationMessage)

    