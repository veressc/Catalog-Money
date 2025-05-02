# routes.py
from flask import Flask, render_template, request, redirect, url_for, jsonify, Blueprint, current_app
from app.models import db, Category, Product
from werkzeug.utils import secure_filename
import os

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/categories')
def categories():
    categories = Category.query.all()
    return render_template('categories.html', categories=categories)

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

@bp.route('/product/<int:product_id>')
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)
    return render_template('product_detail.html', product=product)

@bp.route('/delete_product/<int:product_id>', methods=['POST'])
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)

    # Удаляем изображение, если оно есть
    if product.image_filename:
        image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], product.image_filename)
        if os.path.exists(image_path):
            os.remove(image_path)

    # Удаляем сам продукт из базы
    db.session.delete(product)
    db.session.commit()

    return redirect(url_for('main.products', category_id=product.category_id))
@bp.route('/autocomplete')
def autocomplete():
    query = request.args.get('query', '')
    if not query:
        return jsonify([])
    products = Product.query.filter(Product.name.ilike(f"%{query}%")).all()
    suggestions = [product.name for product in products]
    return jsonify(suggestions)

@bp.route('/add-product', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = float(request.form['price'])
        category_id = int(request.form['category_id'])

        # Получение файла изображения
        image = request.files.get('image')
        image_filename = None

        if image and '.' in image.filename and \
           image.filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}:
            filename = secure_filename(image.filename).replace(" ", "_")
            image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            image.save(image_path)
            image_filename = filename

        # Создание и сохранение нового товара
        new_product = Product(
            name=name,
            description=description,
            price=price,
            category_id=category_id,
            image_filename=image_filename
        )

        db.session.add(new_product)
        db.session.commit()

        return redirect(url_for('main.products', category_id=category_id))

    # GET-запрос: отображаем форму
    categories = Category.query.all()
    return render_template('add_product.html', categories=categories)


@bp.route('/add-category', methods=['GET', 'POST'])
def add_category():
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')

        if name:
            new_category = Category(name=name, description=description)
            db.session.add(new_category)
            db.session.commit()
            return redirect(url_for('main.categories'))

    return render_template('add_category.html')

@bp.route('/delete_category/<int:category_id>', methods=['POST'])
def delete_category(category_id):
    category = Category.query.get_or_404(category_id)
    Product.query.filter_by(category_id=category.id).delete()
    db.session.delete(category)
    db.session.commit()
    return redirect(url_for('main.categories'))
