from flask import Flask, render_template, request, session, jsonify,redirect,url_for

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# In-memory data storage
users = {}
books = [
    {"id": 1, "title": "Harry Potter and the Philosopher's Stone", "author": "J.K. Rowling"},
    {"id": 2, "title": "To Kill a Mockingbird", "author": "Harper Lee"},
    {"id": 3, "title": "1984", "author": "George Orwell"},
    {"id": 4, "title": "The Great Gatsby", "author": "F. Scott Fitzgerald"},
    {"id": 5, "title": "Moby Dick", "author": "Herman Melville"}
]

# Routes
@app.route('/')
def home():
    if 'username' in session:
        return redirect(url_for('search_books'))
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users:
            return "User already exists. Please log in."
        users[username] = password
        session['username'] = username
        return redirect(url_for('search_books'))
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username] == password:
            session['username'] = username
            return redirect(url_for('search_books'))
        return "Invalid credentials. Please try again."
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/search', methods=['GET', 'POST'])
def search_books():
    if 'username' not in session:
        return redirect(url_for('home'))
    return render_template('search.html')

@app.route('/search_ajax', methods=['GET'])
def search_ajax():
    query = request.args.get('query', '').lower()
    results = [book for book in books if query in book['title'].lower()]
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
