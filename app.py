# from flask import Flask, render_template, request, redirect, url_for, flash, session
# import mysql.connector
# from datetime import datetime

# app = Flask(__name__)
# app.secret_key = "supersecretkey"  # Required for session and flashing messages

# # ✅ Function to connect to MySQL database
# def get_db_connection():
#     try:
#         conn = mysql.connector.connect(
#             host="Abhay143.mysql.pythonanywhere-services.com",
#             user="Abhay143",
#             password="abhay-is-good",
#             database="Abhay143$waffle_credit"
#         )
#         return conn
#     except mysql.connector.Error as err:
#         print(f"Database connection error: {err}")
#         return None

# # ✅ Admin Panel: Add or Deduct Credits & Log Transactions
# @app.route('/admin', methods=['GET', 'POST'])
# def admin_page():
#     if request.method == 'POST':
#         name = request.form['name']
#         credits = int(request.form['credits'])
#         action = request.form['action']  # "add" or "deduct"

#         conn = get_db_connection()
#         if conn is None:
#             return "Database connection failed"

#         cursor = conn.cursor()
#         cursor.execute("SELECT credits FROM customers WHERE name = %s", (name,))
#         result = cursor.fetchone()

#         if result:
#             if action == "add":
#                 cursor.execute("UPDATE customers SET credits = credits + %s WHERE name = %s", (credits, name))
#                 transaction_type = "Credit Added"
#             elif action == "deduct":
#                 if result[0] >= credits:  # Ensure enough balance
#                     cursor.execute("UPDATE customers SET credits = credits - %s WHERE name = %s", (credits, name))
#                     transaction_type = "Credit Deducted"
#                 else:
#                     flash("Not enough credits to deduct!", "danger")
#                     return redirect(url_for('admin_page'))

#             # Log transaction in history
#             timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#             cursor.execute("INSERT INTO transactions (name, amount, type, timestamp) VALUES (%s, %s, %s, %s)",
#                            (name, credits, transaction_type, timestamp))

#             conn.commit()
#             cursor.close()
#             conn.close()
#             flash("Transaction successful!", "success")
#         else:
#             flash("User not found!", "danger")

#     return render_template('admin.html')

# # ✅ Route to View All Users
# @app.route('/users')
# def view_users():
#     conn = get_db_connection()
#     if conn is None:
#         return "Database connection failed"

#     cursor = conn.cursor()
#     cursor.execute("SELECT * FROM customers")
#     users = cursor.fetchall()
#     cursor.close()
#     conn.close()

#     return render_template('view_users.html', users=users)

# # ✅ User Registration (Prevents Duplicate Names)
# @app.route('/register', methods=['GET', 'POST'])
# def register():
#     if request.method == 'POST':
#         name = request.form['name']

#         conn = get_db_connection()
#         if conn is None:
#             return "Database connection failed"

#         cursor = conn.cursor()
#         cursor.execute("SELECT * FROM customers WHERE name = %s", (name,))
#         if cursor.fetchone():
#             flash("Username already exists! Please choose another.", "danger")
#             return redirect(url_for('register'))

#         # Insert new user with 25 signup bonus points
#         cursor.execute("INSERT INTO customers (name, credits) VALUES (%s, 25)", (name,))
#         conn.commit()
#         cursor.close()
#         conn.close()

#         flash("Account created successfully! You earned 25 points.", "success")
#         return redirect(url_for('user_page'))

#     return render_template('register.html')

# # ✅ Route for Users to Check Their Credit
# @app.route('/user', methods=['GET', 'POST'])
# def user_page():
#     if request.method == 'POST':
#         name = request.form['name']

#         conn = get_db_connection()
#         if conn is None:
#             return "Database connection failed"

#         cursor = conn.cursor()
#         cursor.execute("SELECT credits FROM customers WHERE name = %s", (name,))
#         result = cursor.fetchone()

#         cursor.close()
#         conn.close()

#         if result:
#             credits = result[0]
#             return redirect(url_for('greeting', name=name, credits=credits))
#         else:
#             return "User not found", 404

#     return render_template('user.html')

# # ✅ Route to Show Greeting with User's Credits
# @app.route('/greeting')
# def greeting():
#     name = request.args.get('name')
#     credits = request.args.get('credits')
#     return render_template('greeting.html', name=name, credits=credits)

# # ✅ View Transaction History
# @app.route('/transactions')
# def transaction_history():
#     conn = get_db_connection()
#     if conn is None:
#         return "Database connection failed"

#     cursor = conn.cursor()
#     cursor.execute("SELECT * FROM transactions ORDER BY timestamp DESC")
#     transactions = cursor.fetchall()
#     cursor.close()
#     conn.close()

#     return render_template('transactions.html', transactions=transactions)

# # ✅ Gamification: Tasks for Earning Points
# @app.route('/tasks', methods=['GET', 'POST'])
# def tasks():
#     if request.method == 'POST':
#         name = request.form['name']
#         task_completed = request.form['task']  # Example: "Instagram Follow"

#         conn = get_db_connection()
#         if conn is None:
#             return "Database connection failed"

#         cursor = conn.cursor()
#         cursor.execute("SELECT credits FROM customers WHERE name = %s", (name,))
#         result = cursor.fetchone()

#         if result:
#             points_earned = 5  # Default task reward
#             cursor.execute("UPDATE customers SET credits = credits + %s WHERE name = %s", (points_earned, name))

#             # Log transaction
#             timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#             cursor.execute("INSERT INTO transactions (name, amount, type, timestamp) VALUES (%s, %s, %s, %s)",
#                            (name, points_earned, f"Task Completed: {task_completed}", timestamp))

#             conn.commit()
#             flash(f"You earned {points_earned} points!", "success")
#         else:
#             flash("User not found!", "danger")

#         cursor.close()
#         conn.close()

#     return render_template('tasks.html')

# # ✅ Delete User
# @app.route('/admin/delete/<int:user_id>', methods=['POST'])
# def delete_user(user_id):
#     conn = get_db_connection()
#     if conn is None:
#         return "Database connection failed"

#     cursor = conn.cursor()
#     cursor.execute("DELETE FROM customers WHERE id = %s", (user_id,))
#     conn.commit()

#     cursor.close()
#     conn.close()

#     flash("User deleted successfully!", "success")
#     return redirect(url_for('view_users'))

# if __name__ == "__main__":
#     app.run(debug=True)

from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host="Abhay143.mysql.pythonanywhere-services.com",          # Replace with your host
            user="Abhay143",      # Replace with your username
            password="abhay-is-good",  # Replace with your password
            database="Abhay143$waffle_credit"   # Replace with your database name
        )
        return conn
    except mysql.connector.Error as err:
        print(f"Database connection error: {err}")
        return None

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        name = request.form['name']
        credits = int(request.form['credits'])

        conn = get_db_connection()
        if conn is None:
            return "Database connection failed"

        cursor = conn.cursor()
        cursor.execute("SELECT credits FROM customers WHERE name = %s", (name,))
        result = cursor.fetchone()

        if result:
            # Update user's credits if they exist
            cursor.execute(
                "UPDATE customers SET credits = credits + %s WHERE name = %s",
                (credits, name)
            )
        else:
            # Insert new user if they don't exist
            cursor.execute(
                "INSERT INTO customers (name, credits) VALUES (%s, %s)",
                (name, credits)
            )

        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('view_users'))

    return render_template('admin.html')

@app.route('/users')
def view_users():
    conn = get_db_connection()
    if conn is None:
        return "Database connection failed"

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM customers")
    users = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template('view_users.html', users=users)

# Route for user to check their credit
@app.route('/user', methods=['GET', 'POST'])
def user_page():
    if request.method == 'POST':
        name = request.form['name']

        conn = get_db_connection()
        if conn is None:
            return "Database connection failed"

        cursor = conn.cursor()
        cursor.execute("SELECT credits FROM customers WHERE name = %s", (name,))
        result = cursor.fetchone()

        cursor.close()
        conn.close()

        if result:
            credits = result[0]
            return redirect(url_for('greeting', name=name, credits=credits))
        else:
            return "User not found", 404

    return render_template('user.html')

# Route to show greeting with user's credits
@app.route('/greeting')
def greeting():
    name = request.args.get('name')
    credits = request.args.get('credits')
    return render_template('greeting.html', name=name, credits=credits)

# Delete user from the database
@app.route('/admin/delete/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    conn = get_db_connection()
    if conn is None:
        return "Database connection failed"

    cursor = conn.cursor()
    cursor.execute("DELETE FROM customers WHERE id = %s", (user_id,))
    conn.commit()

    cursor.close()
    conn.close()

    return redirect(url_for('view_users'))

if __name__ == "__main__":
    app.run(debug=True)






