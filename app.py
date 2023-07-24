# (previous code...)
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = '5d721da37d29209cbcf47b4ea1a0b754'  
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db' 
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

# Routes and Views:

@app.route('/')
def home():
    return "Welcome to the Home Page!"

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Retrieve form data
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        # Check if passwords match and meet criteria (from lab7)
        if password != confirm_password or len(password) < 8:
            flash('Passwords must match and be at least 8 characters long.', 'error')
            return redirect(url_for('signup'))

        # Bonus (+10) - Check if email already exists
        if User.query.filter_by(email=email).first():
            flash('Email address already used. Please choose another one.', 'error')
            return redirect(url_for('signup'))

        # Save the user to the database
        user = User(first_name=first_name, last_name=last_name, email=email, password=password)
        db.session.add(user)
        db.session.commit()

        return redirect(url_for('thankyou'))

    return render_template('signup.html')


@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        # Retrieve form data
        email = request.form['email']
        password = request.form['password']

        # Check if user exists and passwords match
        user = User.query.filter_by(email=email).first()
        if user and user.password == password:
            return redirect(url_for('secret_page'))
        else:
            flash('Invalid email or password.', 'error')
            return redirect(url_for('signin'))

    return render_template('signin.html')

@app.route('/thankyou')
def thankyou():
    return render_template('thankyou.html')

@app.route('/secretPage')
def secret_page():
    return render_template('secretPage.html')

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
