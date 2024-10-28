from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username == 'admin' and password == 'password':
            session['username'] = username
            return redirect(url_for('dashboard'))  # Chuyển hướng đến dashboard hoặc trang khác
        else:
            return 'Invalid username or password'  # Thông báo lỗi nếu đăng nhập không thành công

    return render_template('login.html')  # Hiển thị trang đăng nhập


@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        return f'Hello, {session["username"]}!'  # Hiển thị thông tin người dùng đã đăng nhập
    return redirect(url_for('login'))  # Nếu chưa đăng nhập, chuyển hướng đến trang đăng nhập


if __name__ == '__main__':
    app.run(debug=True)
