from flask import render_template, redirect, request, session, flash
from flask_app import app, bcrypt
from flask_app.models.user import User

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect('/dashboard')
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    if not User.validate_register(request.form):
        return redirect('/')
    
    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": bcrypt.generate_password_hash(request.form['password'])
    }
    user_id = User.save(data)
    session['user_id'] = user_id
    session['user_name'] = request.form['first_name']
    return redirect('/dashboard')

@app.route('/login', methods=['POST'])
def login():
    data = {"email": request.form['email']}
    user_in_db = User.get_by_email(data)
    
    if not user_in_db or not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash("Email o contraseña inválidos", "login")
        return redirect('/')
        
    session['user_id'] = user_in_db.id
    session['user_name'] = user_in_db.first_name
    return redirect('/dashboard')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')
