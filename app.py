from flask import Flask
from extensions import mysql

app = Flask(__name__)
app.secret_key = "supersecretkey"

import os

UPLOAD_FOLDER = 'static/images'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'YourSQLPassword'
app.config['MYSQL_DB'] = 'ecommerce_db'

mysql.init_app(app)  

from routes.auth_routes import auth_bp
from routes.product_routes import product_bp
from routes.cart_routes import cart_bp

app.register_blueprint(auth_bp)
app.register_blueprint(product_bp)
app.register_blueprint(cart_bp)

if __name__ == '__main__':
    app.run(debug=True)

