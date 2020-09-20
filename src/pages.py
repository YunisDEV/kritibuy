from flask import Blueprint, render_template

pages = Blueprint('pages', __name__, template_folder='../public')


@pages.route('/')
def index():
    return render_template('views/index.html')


@pages.route('/about')
def about():
    return render_template('views/about.html')


@pages.route('/blog')
def blog():
    return render_template('views/blog.html')


@pages.route('/contact')
def contact():
    return render_template('views/contact.html')


@pages.route('/pricing')
def pricing():
    return render_template('views/pricing.html')


@pages.route('/login')
def login():
    return render_template('views/login.html')


@pages.route('/signup')
def signup():
    return render_template('views/signup.html')
