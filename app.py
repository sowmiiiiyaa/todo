from flask import Flask, g, render_template, request, redirect, url_for
import sqlite3
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE_PATH = os.path.join(BASE_DIR, 'instance', 'todos.db')

app = Flask(__name__, static_folder='static', template_folder='templates')
app.config['SECRET_KEY'] = 'dev'


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        os.makedirs(os.path.dirname(DATABASE_PATH), exist_ok=True)
        db = g._database = sqlite3.connect(DATABASE_PATH)
        db.row_factory = sqlite3.Row
    return db


def init_db():
    db = get_db()
    db.execute('''CREATE TABLE IF NOT EXISTS todos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        completed INTEGER NOT NULL DEFAULT 0,
        created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
    )''')
    db.commit()


# Initialize the database inside an application context so it's ready
# before the server starts. `before_first_request` may not be available
# in some Flask builds, so use an explicit app context here.
with app.app_context():
    init_db()


@app.teardown_appcontext
def close_db(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.route('/', methods=['GET'])
def index():
    db = get_db()
    cur = db.execute('SELECT * FROM todos ORDER BY completed, created DESC')
    todos = cur.fetchall()
    return render_template('index.html', todos=todos)


@app.route('/add', methods=['POST'])
def add():
    title = request.form.get('title', '').strip()
    if title:
        db = get_db()
        db.execute('INSERT INTO todos (title, completed) VALUES (?, 0)', (title,))
        db.commit()
    return redirect(url_for('index'))


@app.route('/toggle/<int:todo_id>', methods=['POST'])
def toggle(todo_id):
    db = get_db()
    cur = db.execute('SELECT completed FROM todos WHERE id=?', (todo_id,))
    row = cur.fetchone()
    if row:
        new = 0 if row['completed'] else 1
        db.execute('UPDATE todos SET completed=? WHERE id=?', (new, todo_id))
        db.commit()
    return redirect(url_for('index'))


@app.route('/delete/<int:todo_id>', methods=['POST'])
def delete(todo_id):
    db = get_db()
    db.execute('DELETE FROM todos WHERE id=?', (todo_id,))
    db.commit()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
