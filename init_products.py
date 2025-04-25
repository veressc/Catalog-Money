from app import create_app, db
from app.models import Product, Category

app = create_app()

with app.app_context():
    # Пример добавления товара
    smartphone = Category.query.filter_by(name='Смартфоны').first()
    laptop = Category.query.filter_by(name='Ноутбуки').first()

    db.create_all()  # если не создавал ещё

    db.session.add_all([
        Product(name='iPhone 15 Pro', description='Apple A17 Pro, 256 ГБ', price=1399.0, category_id=smartphone.id),
        Product(name='Xiaomi 13T', description='256 ГБ, AMOLED 144Гц', price=549.0, category_id=smartphone.id),
        Product(name='ASUS TUF Gaming F15', description='RTX 4060, i7, 16ГБ RAM', price=1199.0, category_id=laptop.id),
    ])

    db.session.commit()
    print("✅ Товары добавлены!")
