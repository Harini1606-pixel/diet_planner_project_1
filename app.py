from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# ---------------- DATABASE ---------------- #

def init_db():
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        password TEXT
    )
    """)

    conn.commit()
    conn.close()

init_db()

# ---------------- LOGIN PAGE ---------------- #

@app.route('/')
def login():
    return render_template("login.html")


# ---------------- REGISTER PAGE ---------------- #

@app.route('/register')
def register():
    return render_template("register.html")


# ---------------- REGISTER USER ---------------- #

@app.route('/register_user', methods=['POST'])
def register_user():

    username = request.form['username']
    password = request.form['password']

    conn = sqlite3.connect('database.db')
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO users(username,password) VALUES (?,?)",
        (username, password)
    )

    conn.commit()
    conn.close()

    return redirect('/')


# ---------------- LOGIN USER ---------------- #

@app.route('/login_user', methods=['POST'])
def login_user():

    username = request.form['username']
    password = request.form['password']

    conn = sqlite3.connect('database.db')
    cur = conn.cursor()

    cur.execute(
        "SELECT * FROM users WHERE username=? AND password=?",
        (username, password)
    )

    user = cur.fetchone()
    conn.close()

    if user:
        return redirect('/dashboard')
    else:
        return "Invalid Login"


# ---------------- DASHBOARD ---------------- #

@app.route('/dashboard')
def dashboard():
    return render_template("dashboard.html")


# ---------------- BMI PAGE ---------------- #

@app.route('/bmi')
def bmi():
    return render_template("bmi.html")


# ---------------- RESULT + DIET PLAN ---------------- #

@app.route('/result', methods=['POST'])
def result():

    height = float(request.form['height'])
    weight = float(request.form['weight'])

    bmi = weight / ((height / 100) ** 2)

    # BMI Category
    if bmi < 18.5:
        category = "Underweight"
        diet = """
        Breakfast: Milk, Banana, Peanut Butter Toast
        Lunch: Rice, Chicken/Paneer, Vegetables
        Dinner: Chapati, Dal, Salad
        Snacks: Nuts, Smoothies
        """

    elif 18.5 <= bmi < 24.9:
        category = "Normal Weight"
        diet = """
        Breakfast: Oats, Fruits, Boiled Eggs
        Lunch: Brown Rice, Dal, Vegetables
        Dinner: Chapati, Paneer/Chicken, Salad
        Snacks: Fruits, Yogurt
        """

    elif 25 <= bmi < 29.9:
        category = "Overweight"
        diet = """
        Breakfast: Green Tea, Oats, Fruits
        Lunch: Brown Rice, Vegetables, Dal
        Dinner: Salad, Soup, Grilled Chicken
        Snacks: Nuts, Apple
        """

    else:
        category = "Obese"
        diet = """
        Breakfast: Lemon Water, Oats
        Lunch: Salad, Vegetables, Dal
        Dinner: Soup, Boiled Vegetables
        Snacks: Fruits
        """

    return render_template(
        "result.html",
        bmi=round(bmi, 2),
        category=category,
        diet=diet
    )


# ---------------- RUN SERVER ---------------- #

if __name__ == "__main__":
    app.run(debug=True)

