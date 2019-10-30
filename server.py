"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import Flask, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension

from model import User, Rating, Movie, connect_to_db, db


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""
    return render_template('homepage.html')


@app.route("/users")
def user_list():
    """Show list of users."""
    users = User.query.all()
    return render_template("user_list.html", users=users)



@app.route('/register', methods=['GET'])
def register_form():

    return render_template('register_form.html')



@app.route('/register', methods=['POST'])
def register_process():

    user_email = request.form.get('email')
    # print(user_email)
    user_password = request.form.get('password')

    user_age = request.form.get('age')

    user_zipcode = request.form.get('zipcode')

    user = User(email = user_email, 
                password = user_password, 
                age = user_age, 
                zipcode = user_zipcode)

    db.session.add(user)
    db.session.commit()

    return redirect('/')  



@app.route('/login', methods=['GET'])
def login_form():

    return render_template('login_form.html')



@app.route('/login', methods=['POST'])
def validate_user():
    user_email = request.form.get('email')
    user_password = request.form.get('password')

    user = User.query.filter_by(email=user_email).first()

    if user.password == user_password:
        session['user_id'] = user.user_id
        flash('Logged in.')
        return redirect('/')
    else:
        flash('incorrect password')
        return redirect('/login')

@app.route('/users/<int:user_id>')
def display_user_info(user_id):

#age, zipcode, list of movies

    user = User.query.filter_by(user_id = user_id).first()
    age = user.age
    zipcode = user.zipcode
    rated_movies = user.ratings


    return render_template('user_info.html', 
                            user_id= user_id,
                            user_age = age, 
                            user_zipcode=zipcode, 
                            user_ratings = rated_movies)


@app.route('/movies')
def list_all_movies():

    movies = Movie.query.all()

    return render_template('movies_list.html', movies = movies)





if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')
