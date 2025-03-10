from flask import Flask, render_template, session, redirect, request
import secrets
from user import create_user_table, User
from payment import Pay_user, create_user_pay_table

create_user_table()

app = Flask("main")
app.secret_key = secrets.token_hex(32)


@app.route("/")
def index_page():
    username = session.get("username")
    if not username:
        return redirect("login")
    user = User.get_user_by_username(username)
    return render_template("index.html", user=user)


@app.route("/register", methods=['POST', 'GET'])
def register_page():
    if request.method == 'GET':
        return render_template("register.html")
    
    if request.method == 'POST':
        username = request.form.get("username").lower()
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        user = User.get_user_by_username(username)
        
        if user:
            return render_template(
                "register.html", error="Пользователь с таким ником уже есть"
            )
        
        if password != confirm_password:
            return render_template(
                "register.html", error="Пароли не совпадают"
            )
        
        User.create(username, password)
        session["username"] = username
        return redirect('/')


@app.route("/login", methods=['POST', 'GET'])
def login_page():
    if request.method == 'GET':
        return render_template("login.html")
    
    if request.method == 'POST':
        username = request.form.get("username").lower()
        password = request.form.get("password")

        user = User.get_user_by_username(username)
        
        if not user:
            return render_template(
                "login.html", error="Пользователь с таким ником не найден"
            )
        
        if user.password != password:
            return render_template(
                "login.html", error="Неверный пароль"
            )
        print(username)
        session["username"] = username
        return redirect('/profile')


@app.route("/logout")
def logout_page():
    del session["username"]
    return redirect("/login")

@app.route("/profile")
def profile_page():
    username = session.get("username")
    if not username:
        return redirect("login")
    user = User.get_user_by_username(username)
    return render_template("profile.html", user=user)

@app.route("/buy", methods=['POST','GET'])
def buy_page():
    username = session.get("username")
    if not username:
        return redirect("login")
    
    if request.method == 'POST':
        quanity = request.form.get(quanity)
        nomer = request.form.get(nomer)
        date = request.form.get(date)
        code = request.form.get(code)

        Pay_user.create_pay(quanity, nomer, date, code)
        return redirect('/profile')

    user = User.get_user_by_username(username)
    return render_template("buy.html", user=user)

app.run(host="0.0.0.0", port=8080, debug=True)
