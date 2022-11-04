from flask import redirect, request, render_template
from flask_app.models import user
from flask_app import app

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create', methods=['POST'])
def create():
    if not user.User.validate(request.form):
     return redirect('/')
    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email']
    }
    user.User.create_user(data)
    return redirect('/dashboard')

@app.route('/invalid_user')
def invalid_user():
    return render_template('invalid_user.html')

@app.route('/dashboard')
def dashboard():
    all_users = user.User.get_all_users()
    return render_template('dashboard.html', all_users=all_users)