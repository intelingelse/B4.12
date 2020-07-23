# ЗАДАНИЕ 1
# Напишите модуль users.py, который регистрирует новых пользователей. Скрипт должен запрашивать следующие данные:
#
#     -имя
#     -фамилию
#     -пол
#     -адрес электронной почты
#     -дату рождения
#     -рост
#
# Все данные о пользователях сохраните в таблице user нашей базы данных sochi_athletes.sqlite3.




import datetime
import sqlalchemy as sql
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DB_PATH = "sqlite:///sochi_athletes.sqlite3"

Base = declarative_base()


class User(Base):
    """
    Описывает структуру таблицы user для хранения регистрационных данных пользователей
    """
    __tablename__ = "user"
    id = sql.Column(sql.INTEGER, primary_key=True, autoincrement=True)
    first_name = sql.Column(sql.TEXT)
    last_name = sql.Column(sql.TEXT)
    gender = sql.Column(sql.TEXT)
    email = sql.Column(sql.TEXT)
    birthdate = sql.Column(sql.TEXT)
    height = sql.Column(sql.FLOAT)


def connect_db():
    """
    Устанавливает соединение к базе данных, создает таблицы, если их еще нет и возвращает объект сессии
    """
    engine = sql.create_engine(DB_PATH)
    Base.metadata.create_all(engine)
    session = sessionmaker(engine)

    return session()


def valid_email(email_string):
    """
    validates "email" string
    :param email_string
    :return: True or False
    """
    if "@" and "." in email_string:
        if email_string.rfind("@") > email_string.rfind(".") or email_string.count("@") > 1 \
                or not email_string.count("@") or not email_string.count("."):
            return False
        else:
            return True


def valid_dob(dob_string):
    """
    validates "date of birth" string
    :param dob_string: date of birth
    :return: True or False
    """
    now = datetime.datetime.now()
    if len(dob_string) != 10 \
            or dob_string.count("-") < 2 \
            or int(dob_string[0:4]) < now.year - 123 \
            or int(dob_string[5:7]) > 12 \
            or int(dob_string[8:10]) > 31:
        return False
    else:
        return True


def valid_gender(gender_string):
    """
    validates "gender" string
    :param gender_string:
    :return: true or false
    """
    return True if gender_string == "Female" or gender_string == "Male" else False


def request_data():
    """
    Запрашивает у пользователя данные и добавляет их в список users
    :return: returns user object
    """
    # выводим приветствие
    print("Пожалуйста, введите данные\n")
    first_name = input("Ваше имя:\n>>>>  ")
    last_name = input("Ваша фамилия:\n>>>>  ")
    gender = input("Ваш пол (Male/Female)\n>>>>  ").capitalize()

    while not valid_gender(gender):
        print("Пол введен неверно!\n")

        gender = input("Введите Ваш пол (Male/Female)\n>>>>  ")

    email = input("Адрес Вашей электронной почты:\n>>>>  ")

    while not valid_email(email):
        print("Адрес почты введен неверно!\n")

        email = input("Введите Адрес Вашей электронной почты:\n>>>>  ")

    birthdate = input("Введите Вашу дату рождения в формате: YYYY-mm-dd:\n>>>>  ")

    while not valid_dob(birthdate):
        print("Дата рождения указана неверно!\n")

        birthdate = input("Введите Вашу дату рождения в формате: YYYY-mm-dd:\n>>>>  ")

    height = float(input("Введите свой рост (в сантиметрах):\n>>>>  "))
    height /= 100

    user = User(
        first_name=first_name,
        last_name=last_name,
        gender=gender,
        email=email,
        birthdate=birthdate,
        height=height
    )
    return user


def main():
    reg_session = connect_db()
    new_user = request_data()
    reg_session.add(new_user)
    reg_session.commit()
    reg.session.close()
    print("Данные приняты!")
    print(f"Новый пользователь с ID: {new_user.id} создан!")


if __name__ == '__main__':
    main()
