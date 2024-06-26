from flask import Flask, render_template, request, redirect, url_for, flash
from models import Book
from database import db


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
    # app.config['SECRET_KEY'] = 'Sunny@7890'

    db.init_app(app)
    return app


app = create_app()


@app.before_request
def create_tables():
    print("Creating tables...")
    db.create_all()


@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')


@app.route('/')
def index():
    books = Book.query.all()
    return render_template('index.html', books=books)


@app.route('/add', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        genre = request.form['genre']
        price = request.form['price']
        new_book = Book(title=title, author=author, genre=genre, price=price)
        db.session.add(new_book)
        db.session.commit()
        flash('Book Added Successfully!')
        return redirect(url_for('index'))
    return render_template('add_book.html')


@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_book(id):
    book = Book.query.get_or_404(id)
    if request.method == 'POST':
        book.title = request.form['title']
        book.author = request.form['author']
        book.genre = request.form['genre']
        book.price = request.form['price']
        db.session.commit()
        flash('Book Updated Successfully!')
        return redirect(url_for('index'))
    return render_template('edit_book.html', book=book)


@app.route('/delete/<int:id>')
def delete_book(id):
    book = Book.query.get_or_404(id)
    db.session.delete(book)
    db.session.commit()
    flash('Book Deleted Successfully!')
    return redirect(url_for('index'))


@app.route('/contact_us', methods=['GET', 'POST'])
def contact_us():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']

        new_contact = contact_us(name=name, email=email, message=message)
        db.session.add(new_contact)
        db.session.commit()

        flash('Your message has been sent successfully!', 'success')
        return redirect(
            url_for('index')
        )  # Redirect to the index page or another page of your choice

    return render_template('contact_us.html')


@app.route('/send_message', methods=['POST'])
def send_message():
    name = request.form.get('name')  # Use.get() to avoid KeyError
    email = request.form.get('email')  # Use.get() to avoid KeyError
    message = request.form.get('message')  # Use.get() to avoid KeyError

    if not name or not email or not message:
        return "Please fill out all fields.", 400  # Return an error response if any required field is missing

    msg = Message("New Message from Your Website",
                  sender="book@example.com",
                  recipients=["recipient@example.com"])
    msg.body = f"From {name} <{email}>:\n\n{message}"
    msg.html = f"""
    <html>
        <body>
            <h1>New Message from {name}</h1>
            <p>{message}</p>
        </body>
    </html>
    """
    mail.send(msg)
    return "Message sent!", 200  # Return success response


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
