from flask import Flask, render_template, request, redirect, url_for, jsonify, Blueprint
from app.models import db, Category, Product

# Создание Blueprint
bp = Blueprint('main', __name__)

# Главная страница
@bp.route('/')
def index():
    return render_template('index.html')

# Страница категорий
@bp.route('/categories')
def categories():
    categories = Category.query.all()
    return render_template('categories.html', categories=categories)

# Страница товаров по категории
@bp.route('/category/<int:category_id>')
def products(category_id):
    sort = request.args.get('sort', 'name')
    min_price = request.args.get('min_price')
    max_price = request.args.get('max_price')
    search_query = request.args.get('search')

    products = Product.query.filter_by(category_id=category_id)

    if min_price:
        products = products.filter(Product.price >= float(min_price))
    if max_price:
        products = products.filter(Product.price <= float(max_price))
    if search_query:
        products = products.filter(Product.name.ilike(f"%{search_query}%"))

    if sort == 'name':
        products = products.order_by(Product.name.asc())
    elif sort == 'price_asc':
        products = products.order_by(Product.price.asc())
    elif sort == 'price_desc':
        products = products.order_by(Product.price.desc())

    products = products.all()
    category = Category.query.get_or_404(category_id)

    return render_template('products.html', products=products, category=category)

# Детальная страница товара
@bp.route('/product/<int:product_id>')
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)
    return render_template('product_detail.html', product=product)

# Удаление товара
@bp.route('/delete_product/<int:product_id>', methods=['POST'])
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    return redirect(url_for('main.categories'))

# Автокомплит
@bp.route('/autocomplete')
def autocomplete():
    query = request.args.get('query', '')
    if not query:
        return jsonify([])

    products = Product.query.filter(Product.name.ilike(f"%{query}%")).all()
    suggestions = [product.name for product in products]

    return jsonify(suggestions)

# Страница добавления товара
@bp.route('/add-product', methods=['GET', 'POST'])
def add_product():
    categories = Category.query.all()  # <<< добавляем загрузку категорий
    return render_template('add_product.html', categories=categories)
