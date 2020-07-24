# ЗАДАНИЕ 2
# Напишите модуль find_athlete.py поиска ближайшего к пользователю атлета. Логика работы модуля такова:
#
# 1) запросить идентификатор пользователя;
# 2) если пользователь с таким идентификатором существует в таблице user, то вывести на
#   экран двух атлетов: ближайшего по дате рождения к данному пользователю и ближайшего
#   по росту к данному пользователю;
# 3) если пользователя с таким идентификатором нет, вывести соответствующее сообщение.


import sqlalchemy as sql
from sqlalchemy import text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DB_PATH = "sqlite:///sochi_athletes.sqlite3"
Base = declarative_base()


class User(Base):
    """
    Описывает структуру таблицы user для хранения данных пользователей
    """
    __tablename__ = "user"
    id = sql.Column(sql.INTEGER, primary_key=True, autoincrement=True)
    first_name = sql.Column(sql.TEXT)
    last_name = sql.Column(sql.TEXT)
    gender = sql.Column(sql.TEXT)
    email = sql.Column(sql.TEXT)
    birthdate = sql.Column(sql.TEXT)
    height = sql.Column(sql.FLOAT)


class Athlete(Base):
    __tablename__ = "athelete"
    id = sql.Column(sql.INTEGER, primary_key=True, autoincrement=True)
    age = sql.Column(sql.INTEGER)
    birthdate = sql.Column(sql.TEXT)
    gender = sql.Column(sql.TEXT)
    height = sql.Column(sql.FLOAT)
    name = sql.Column(sql.TEXT)
    weight = sql.Column(sql.INTEGER)
    gold_medals = sql.Column(sql.INTEGER)
    silver_medals = sql.Column(sql.INTEGER)
    bronze_medals = sql.Column(sql.INTEGER)
    total_medals = sql.Column(sql.INTEGER)
    sport = sql.Column(sql.TEXT)
    country = sql.Column(sql.TEXT)


def find_closest_by_dob(dob_string, session):
    """
    Производит поиск по атлетам с ближайшим днем рождения к пользовательскому
    Возвращает объект класса 'sqlalchemy.util._collections.result' в виде кортежа
    :param dob_string: User date of_birth
    :param session: session obj
    :return: <class 'sqlalchemy.util._collections.result'> with (Athlete.name, Athlete.birthdate)
    """

    found_athlete = session.query(Athlete.name, Athlete.birthdate).order_by(
        text("abs(strftime('%s', '{}') - strftime('%s', birthdate))".format(dob_string))).limit(1);

    found_athlete = found_athlete[0]

    return found_athlete


def find_closest_by_height(height, session):
    """
    Производит поиск по атлетам с ближайшим ростом к пользовательскому
    Возвращает объект класса 'sqlalchemy.util._collections.result' в виде кортежа
    :param height: User height
    :param session: session obj
    :return:
    """
    found_athlete = session.query(Athlete.name, Athlete.height) \
        .filter(Athlete.height != 0) \
        .order_by(text("abs(height-%f)" % height)) \
        .limit(1)

    found_athlete = found_athlete[0]

    return found_athlete


def get_user_id(session):
    """
    Производит поиск по введеному АйДи, если таковых нет то выводит ошибку и просит АйДи заново
    пока не будет введен корректный Айди либо пользователь нажмет Ctrl + D
    :param session: session obj
    :return: user's object with following keys: first_name, last_name, height, birthdate)
    """

    uid = input("Введите ID пользователя:\n>>>>  ")
    user_query = session.query(User).filter(uid == User.id).first()
    try:
        while not user_query:
            print("Пользователь с таким ID не найден.")
            uid = input("Введите ID существующего пользователя или нажмите CTRL+D, чтобы выйти:\n>>>>  ")
            user_query = session.query(User.first_name, User.last_name, User.birthdate, User.height).filter(
                uid == User.id).first()
    except EOFError:
        print("exiting...")
        exit()

    return user_query


def connect_db():
    """
    Устанавливает соединение к базе данных, создает таблицы, если их еще нет и возвращает объект сессии
    :return: session object
    """

    engine = sql.create_engine(DB_PATH)
    Base.metadata.create_all(engine)
    session = sessionmaker(engine)
    return session()


def main():
    find_session = connect_db()
    user = get_user_id(session=find_session)
    user_full_name = user.first_name + " " + user.last_name
    height = user.height
    dob_string = user.birthdate
    del user
    close_height_athlete = find_closest_by_height(height=height, session=find_session)
    close_birth_athlete = find_closest_by_dob(dob_string=dob_string, session=find_session)
    print(
        f"Атлета с ближайшим ростом к пользователю {user_full_name} зовут {close_height_athlete.name}. "
        f"Его/Её рост составляет {close_height_athlete.height} метра")

    print(
        f"Атлета с ближайшей датой рождения к пользователю {user_full_name} зовут {close_birth_athlete.name}. "
        f"Его/Её дата рождения: {close_birth_athlete.birthdate} ")

    find_session.close()


if __name__ == "__main__":
    main()
