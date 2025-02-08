from fastapi import FastAPI
from sqladmin import Admin, ModelView
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import declarative_base


engine = create_engine(
    'sqlite:///../db/test.db',
    connect_args={'check_same_thread': False},
)
app = FastAPI()
admin = Admin(app, engine, title='Админка')
Base = declarative_base()
Base.metadata.create_all(engine)  # Create tables


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String)


class UserAdmin(ModelView, model=User):
    name = 'Пользователь'
    name_plural = 'Пользователи'
    icon = 'fa-solid fa-user'
    category = 'Аккаунты'
    column_list = [User.id, User.name]
    column_details_list = [User.id, User.name]
    # column_formatters_detail = {User.name: lambda m, a: m.name[:10]}
    column_formatters = {User.name: lambda m, a: m.name[:10]}
    column_searchable_list = [User.name]
    column_sortable_list = [User.id]


admin.add_view(UserAdmin)


if __name__ == '__main__':
    import uvicorn
    Base.metadata.create_all(engine)
    uvicorn.run(app, host='127.0.0.1', port=8000)
