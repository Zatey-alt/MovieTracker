from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user, login_user, logout_user
from models import User, Movie
from . import db

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template('home.html')



@views.route('/main')
def main():
    if current_user.is_authenticated:
        # Display a welcome message if the user is logged in
        return render_template('main.html', message=f'Welcome back, {current_user.username}!')
    else:
        return render_template('login.html')


@views.route('/add-movie', methods=['GET', 'POST'])
@login_required
def add_movie():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')

        new_movie = Movie(title=title, description=description, user_id=current_user.id)
        db.session.add(new_movie)
        db.session.commit()

        return redirect(url_for('views.home'))

    return render_template('add_movie.html', user=current_user)


@views.route('/delete-movie/<id>')
@login_required
def delete_movie(id):
    movie = Movie.query.filter_by(id=id).first()

    if movie:
        if movie.user_id == current_user.id:
            db.session.delete(movie)
            db.session.commit()

    return redirect(url_for('views.home'))

@views.route('/update-movie/<id>', methods=['GET', 'POST'])
@login_required
def update_movie(id):
    movie = Movie.query.filter_by(id=id).first()

    if movie:
        if movie.user_id == current_user.id:
            if request.method == 'POST':
                title = request.form.get('title')
                description = request.form.get('description')

                movie.title = title
                movie.description = description
                db.session.commit()

                return redirect(url_for('views.home'))

            return render_template('update_movie.html', movie=movie)

    return redirect(url_for('views.home'))

