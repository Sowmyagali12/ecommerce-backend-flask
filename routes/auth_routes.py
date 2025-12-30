from flask import Blueprint, render_template, request, redirect, url_for, session
import bcrypt
from extensions import mysql


auth_bp = Blueprint('auth', __name__)



# ---------------------REGISTER------------------------------------------

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password'].encode('utf-8')

        hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())

        cur = mysql.connection.cursor()
        cur.execute(
            "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)",
            (name, email, hashed_password)
        )
        mysql.connection.commit()
        cur.close()

        return redirect(url_for('auth.login'))

    return render_template('register.html')




# ----------------------LOGIN-------------------------
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password'].encode('utf-8')

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE email=%s", (email,))
        user = cur.fetchone()
        cur.close()

        if user and bcrypt.checkpw(password, user[3].encode('utf-8')):
            session['user_id'] = user[0]
            return redirect(url_for('product.products'))

        return "Invalid login"

    return render_template('login.html')


@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))



