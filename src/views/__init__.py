from flask import Blueprint, render_template
import json
from .methods import getContentHTML
from ..account.security import isauth
views = Blueprint('views', __name__, template_folder='./templates')


@views.route('/')
@isauth
def index(user):
    with open('./src/views/contents_en.json', 'rt') as source:
        h = getContentHTML(json.load(source)['index'])
        return render_template('index.html', htmlFromContent=h, user=user)


@views.route('/about')
@isauth
def about(user):
    with open('./src/views/contents_en.json', 'rt') as source:
        h = getContentHTML(json.load(source)['about'])
        return render_template('about.html', htmlFromContent=h, user=user)


@views.route('/blog')
@isauth
def blog(user):
    fetched_blogs = [
        {
            "title": "Some quick example text to build on the card title and make up the bulk of the card's content.",
            "image": "https://via.placeholder.com/728x400.png"
        },
        {
            "title": "Some quick example text to build on the card title and make up the bulk of the card's content.",
            "image": "https://via.placeholder.com/728x400.png"
        },
        {
            "title": "Some quick example text to build on the card title and make up the bulk of the card's content.Some quick example text to buildadgadgokpokpokakmglkm",
            "image": "https://via.placeholder.com/728x400.png"
        },
        {
            "title": "Some quick example text to build on the card title aaaaaaaaaaaa make up the bulk of the card's content.",
            "image": "https://via.placeholder.com/728x400.png"
        },
        {
            "title": "Some quick example text to build on the card title and make up the bulk of the card's content.",
            "image": "https://via.placeholder.com/728x400.png"
        }
    ]
    _blogs = []
    temp = []
    for i in range(len(fetched_blogs)):
        _temp = fetched_blogs[i]
        _temp["title"] = _temp["title"][0:126]
        if len(fetched_blogs[i]["title"]) >= 126:
            _temp["title"] += "..."
        temp.append(_temp)
        if i % 3 == 2:
            _blogs.append(temp)
            temp = []
    _blogs.append(temp)
    return render_template('blog.html', _blogs=_blogs, user=user)


@views.route('/contact')
@isauth
def contact(user):
    return render_template('contact.html',user=user)


@views.route('/pricing')
@isauth
def pricing(user):
    with open('./src/views/contents_en.json', 'rt') as source:
        h = getContentHTML(json.load(source)['pricing'])
        return render_template('pricing.html', htmlFromContent=h,user=user)
