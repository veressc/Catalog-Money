from flask import Blueprint, render_template
from .models import Category
from . import db

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/categories')
def categories():
    categories = Category.query.all()
    return render_template('categories.html', categories=categories)
