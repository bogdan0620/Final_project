from database.models import User
from database import get_db


def register_user_db(username, password):
    db = next(get_db())
    checker = db.query(User).filter_by(username=username).first()

    if checker:
        return 'Пользователь уже зарегистрирован'
    new_user = User(username=username, password=password)
    db.add(new_user)
    db.commit()
    return 'Вы зарегистрировались'


def check_password_db(username, password):
    db = next(get_db())
    checker1 = db.query(User).filter_by(username=username, password=password).first()

    if checker1:
        checker = checker1.as_dict()
        return checker

    else:
        return 'Имя пользователя или пароль не правильный'
