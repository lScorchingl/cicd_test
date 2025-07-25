import time
from pages.homepage import HomePage
from pages.product import ProductPage


def test_autorization(browser):
    homepage = HomePage(browser)
    homepage.open_passport()
    homepage.autorization()


def test_language_check(browser):
    homepage = HomePage(browser)
    homepage.open_passport()
    homepage.autorization()
    homepage.language_check()


def test_avatar_check(browser):
    homepage = HomePage(browser)
    homepage.open_passport()
    homepage.autorization()
    homepage.avatar_check()


def test_check_area(browser):
    homepage = HomePage(browser)
    homepage.open_passport()
    homepage.autorization()
    homepage.check_area()


def test_check_birthday(browser):
    homepage = HomePage(browser)
    homepage.open_passport()
    homepage.autorization()
    homepage.check_birthday()


def test_change_password(browser):
    homepage = HomePage(browser)
    homepage.open_passport()
    homepage.autorization()
    homepage.change_password()


def test_change_user_data(browser):
    homepage = HomePage(browser)
    homepage.open_passport()
    homepage.autorization()
    homepage.change_user_data()


# def test_change_busy_email(browser): ФУНКЦИЯ НЕ РАБОТАЕТ, ПАСПОРТ ПИШЕТ ЧТО ПОДОЗРИТЕЛЬНАЯ АКТИВНОСТЬ, И ДУШИТ. НЕ ИСКАЛ ПУТИ ОБХОДА.
#     homepage = HomePage(browser)
#     homepage.open_passport()
#     homepage.autorization()
#     homepage.change_busy_email()


def test_exit_account(browser):
    homepage = HomePage(browser)
    homepage.open_passport()
    homepage.autorization()
    homepage.exit_account()


def test_check_demo_mode(browser):
    homepage = HomePage(browser)
    homepage.check_demo_mode()
