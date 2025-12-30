from flask import Blueprint, redirect, request, url_for, session, render_template
from extensions import mysql


cart_bp = Blueprint('cart', __name__)



# -----------------------add to cart----------------------

@cart_bp.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    user_id = session['user_id']
    product_id = request.form['product_id']

    cur = mysql.connection.cursor()

    # 1. Check if product already in cart
    cur.execute("""
        SELECT quantity FROM cart
        WHERE user_id = %s AND product_id = %s
    """, (user_id, product_id))

    item = cur.fetchone()

    if item:
        # 2. If exists → increase quantity
        cur.execute("""
            UPDATE cart
            SET quantity = quantity + 1
            WHERE user_id = %s AND product_id = %s
        """, (user_id, product_id))
    else:
        # 3. If not exists → insert
        cur.execute("""
            INSERT INTO cart (user_id, product_id, quantity)
            VALUES (%s, %s, 1)
        """, (user_id, product_id))

    mysql.connection.commit()
    cur.close()

    return redirect(url_for('product.products'))




# -------------------cart route------------------------
@cart_bp.route('/cart')
def view_cart():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    user_id = session['user_id']

    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT
            p.id,
            p.image,
            p.name,
            p.price,
            c.quantity,
            (p.price * c.quantity) AS item_total
        FROM cart c
        JOIN products p ON c.product_id = p.id
        WHERE c.user_id = %s
    """, (user_id,))

    cart_items = cur.fetchall()
    cur.close()

    # ✅ Correct grand total (sum of item_total)
    grand_total = sum(item[5] for item in cart_items)

    return render_template(
        'cart.html',
        cart=cart_items,
        total_bill=grand_total
    )



# -----------------remove from cart----------------------
@cart_bp.route('/remove_from_cart', methods=['POST'])
def remove_from_cart():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    product_id = request.form['product_id']
    user_id = session['user_id']

    cur = mysql.connection.cursor()
    cur.execute("""
        DELETE FROM cart 
        WHERE user_id = %s AND product_id = %s
    """, (user_id, product_id))

    mysql.connection.commit()
    cur.close()

    return redirect(url_for('cart.view_cart'))


