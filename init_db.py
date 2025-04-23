from app import create_app, db
from app.models import Category

app = create_app()

with app.app_context():
    db.create_all()

    if Category.query.count() == 0:
        db.session.add(Category(name='Смартфоны'))
        db.session.add(Category(name='Ноутбуки'))
        db.session.commit()
        print("✅ Категории добавлены!")
    else:
        print("Категории уже существуют.")
