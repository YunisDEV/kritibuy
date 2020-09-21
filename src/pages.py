from flask import Blueprint, render_template
import json
from src.methods import getContentHTML

pages = Blueprint('pages', __name__, template_folder='../public')


@pages.route('/')
def index():
    with open('./src/page_contents/contents.json','rt') as source:
        h = getContentHTML(json.load(source)['index'])
        return render_template('views/index.html',htmlFromContent=h)


@pages.route('/about')
def about():
    with open('./src/page_contents/contents.json','rt') as source:
        h = getContentHTML(json.load(source)['about'])
        return render_template('views/about.html',htmlFromContent=h)


@pages.route('/blog')
def blog():
    return render_template('views/blog.html')


@pages.route('/contact')
def contact():
    return render_template('views/contact.html')


@pages.route('/pricing')
def pricing():
    with open('./src/page_contents/contents.json','rt') as source:
        h = getContentHTML(json.load(source)['pricing'])
        return render_template('views/pricing.html',htmlFromContent=h)


@pages.route('/login')
def login():
    return render_template('views/login.html')


@pages.route('/signup')
def signup():
    return render_template('views/signup.html')
