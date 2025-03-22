from flask_admin import Admin, AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from flask_admin.menu import MenuLink
from models import User, Book, db

admin = Admin(
    name="Адмінка магазину",
    template_mode="bootstrap4",
)


    
admin.add_link(MenuLink(name="Вийти", url="/logout"))

admin.add_view(ModelView(Book, db.session))
admin.add_view(ModelView(User, db.session))

