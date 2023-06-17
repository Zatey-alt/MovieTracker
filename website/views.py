from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user, login_user, logout_user
from .models import User
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
