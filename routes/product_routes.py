import os
from flask import Blueprint, render_template, request, redirect, url_for, session, current_app
from werkzeug.utils import secure_filename
from extensions import mysql



product_bp = Blueprint('product', __name__)


# -------------------display products--------------
@product_bp.route('/products')
def products():
    # 1. User must be logged in
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    # 2. Fetch all products from DB
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM products")
    products = cur.fetchall()
    cur.close()

    # 3. Send products to template
    return render_template('products.html', products=products)





# --------------------add_product------------------

@product_bp.route('/add_product', methods=['GET', 'POST'])
def add_product():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    cur = mysql.connection.cursor()
    cur.execute("SELECT is_admin FROM users WHERE id=%s", (session['user_id'],))
    is_admin = cur.fetchone()[0]

    if not is_admin:
        return "Access Denied"

    if request.method == 'POST':
        name = request.form['name']
        category = request.form['category']
        price = request.form['price']
        description = request.form['description']

        image_file = request.files['image']

        # Make filename safe
        filename = secure_filename(image_file.filename)

        # Save image to static/images
        image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        image_file.save(image_path)

        # Store filename in DB
        cur.execute("""
            INSERT INTO products (name, category, price, image, description)
            VALUES (%s, %s, %s, %s, %s)
        """, (name, category, price, filename, description))

        mysql.connection.commit()
        cur.close()

        return redirect(url_for('product.add_product'))

    cur.close()
    return render_template('add_product.html')



