from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import string
import random

app = Flask(__name__)
# holds location of the sqldatabase
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///urls.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# database model
db = SQLAlchemy(app)


class Urls(db.Model):
    # column        name   type
    id_ = db.Column("id_", db.Integer, primary_key=True)
    # store long urls
    long = db.Column("long", db.String())
    # store short urls
    short = db.Column("short", db.String(3))

    # constructor

    def __int__(self, long, short):
        self.long = long
        self.short = short


# create all columns inside the database
@app.before_first_request
def create_tables():
    db.create_all()


def shorten_url():
    letters = string.ascii_lowercase + string.ascii_uppercase
    while True:
        rand_letters = random.choices(letters, k=3)
        rand_letters = "".join(rand_letters)
        short_url = Urls.query.filter_by(short=rand_letters).first()
        if not short_url:
            return rand_letters


@app.route('/', methods=['POST', 'GET'])
def home():
    if request.method == 'POST':
        url_received = request.form["nm"]
        # check if url already exists in db
        found_url = Urls.query.filter_by(long=url_received).first()
        if found_url:
            # return short url if found
            return redirect(url_for("display_short_url", url=found_url.short))
        else:
            # create short url if not found
            short_url = shorten_url()
            new_url = Urls(url_received, short_url)
            db.session.add(new_url)
            db.session.commit()
            return redirect(url_for("display_short_url", url=short_url))

    else:
        return render_template("home.html")


@app.route('/display/<url>')
def display_short_url(url):
    return render_template('shorturl.html', short_url_display=url)


@app.route('/<shorturl>')
def redirection(short_url):
    long_url = Urls.query.filter_by(short=short_url).first()
    if long_url:
        return f'<h1>Url does not exist<h1>'

if __name__ == '__main__':
    app.run(debug=True)
