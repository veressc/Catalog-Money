from flask import Blueprint, render_template, request, redirect
from app.models import Category, Product

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/categories')
def categories():
    categories = Category.query.all()
    return render_template('categories.html', categories=categories)

@bp.route('/category/<int:category_id>')
def category_products(category_id):
    category = Category.query.get_or_404(category_id)

    search = request.args.get('search', '')
    price_min = request.args.get('price_min', type=float)
    price_max = request.args.get('price_max', type=float)
    sort_by = request.args.get('sort', 'name')

    query = Product.query.filter_by(category_id=category_id)

    if search:
        query = query.filter(Product.name.ilike(f'%{search}%'))
    if price_min is not None:
        query = query.filter(Product.price >= price_min)
    if price_max is not None:
        query = query.filter(Product.price <= price_max)
    if sort_by == 'price':
        query = query.order_by(Product.price)
    else:
        query = query.order_by(Product.name)

    products = query.all()

    return render_template(
        'products.html',
        category=category,
        products=products,
        search=search,
        price_min=price_min,
        price_max=price_max,
        sort_by=sort_by
    )

@bp.route('/product/<int:product_id>')
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)
    return render_template('product_detail.html', product=product)

# 🔥 Новый маршрут для удаления товара
@bp.route('/delete-product/<int:product_id>', methods=['POST'])
def delete_product(product_id):
    from app import db
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    return redirect(f'/categories/{product.category_id}')
