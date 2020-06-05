from Talos import app
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

    return render_template('registerPage.html')

    