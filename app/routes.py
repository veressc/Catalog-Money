from flask import Blueprint, render_template, request, jsonify
from app.models import Category, Product

bp = Blueprint('main', __name__)

@bp.route("/")
def index():
    return render_template("index.html")

@bp.route("/categories")
def categories():
    categories = Category.query.all()
    return render_template("categories.html", categories=categories)

@bp.route("/category/<int:category_id>")
def category_products(category_id):
    category = Category.query.get_or_404(category_id)

    # Параметры из запроса
    search = request.args.get("search", "")
    price_min = request.args.get("price_min", type=float)
    price_max = request.args.get("price_max", type=float)
    sort_by = request.args.get("sort", "name")  # name / price

    query = Product.query.filter_by(category_id=category_id)

    if search:
        query = query.filter(Product.name.ilike(f"%{search}%"))
    if price_min is not None:
        query = query.filter(Product.price >= price_min)
    if price_max is not None:
        query = query.filter(Product.price <= price_max)
    if sort_by == "price":
        query = query.order_by(Product.price)
    else:
        query = query.order_by(Product.name)

    products = query.all()

    return render_template(
        "products.html",
        category=category,
        products=products,
        search=search,
        price_min=price_min,
        price_max=price_max,
        sort_by=sort_by
    )

@bp.route("/product/<int:product_id>")
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)
    return render_template("product_detail.html", product=product)

# НОВЫЙ маршрут для автокомплита
@bp.route("/autocomplete")
def autocomplete():
    query = request.args.get("query", "")
    if not query:
        return jsonify([])

    matching_products = Product.query.filter(Product.name.ilike(f"%{query}%")).limit(5).all()

    suggestions = [product.name for product in matching_products]
    return jsonify(suggestions)