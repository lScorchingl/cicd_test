import time
import pyautogui
from bs4 import BeautifulSoup
from selenium.common import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
import re
from pathlib import Path
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class HomePage:

    def __init__(self, browser):
        self.browser = browser
        self.wait = WebDriverWait(self.browser, 10)

    def open_passport(self):
        self.browser.get('https://passport.tecel.ru/profile')

    def autorization(self):
        login_input = self.browser.find_element(By.ID, "inp-login-1")
        login_input.send_keys('teceltest@mail.ru')

        button_next = self.browser.find_element(By.XPATH, "//button[@id='btn-submit-1']")
        button_next.click()

        # Правила политики и конфиденциальность
        # terms = self.browser.find_element(By.XPATH, "//span[contains(text(),'Принимаю')]")
        # terms.click()
        #
        # privacy = self.browser.find_element(By.XPATH, "//span[contains(text(),'Соглашаюсь c')]")
        # privacy.click()

        password_input = self.browser.find_element(By.ID, "inp-pass-1")
        password_input.send_keys('qwe123')

        button_enter = self.browser.find_element(By.XPATH, "//button[@id='btn-submit-2']")
        button_enter.click()

        profile_text = self.browser.find_element(By.XPATH, "//p[@class='logo-desc']")

        assert profile_text.is_displayed(), f"{' ' * 79}Авторизация провалена"  # ПРОВЕРИТЬ ЭТОТ АССЕРТ ВБИТЬ В profile_text НЕВЕРНЫЙ ИКСПАС
        print(f"{' ' * 79}Авторизация успешна")

    def language_check(self):
        language_button = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//span[@class='lang-switcher']"))
        )
    
        # Меняем язык на EN и обратно на RU
        language_button.click()  # EN
        language_button.click()  # RU
    
        # Получаем текст страницы
        page_source = self.browser.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        page_text = soup.get_text()
    
        # Ищем английские слова (только латинские буквы)
        english_words = set(re.findall(r'\b[a-zA-Z]+\b', page_text))
    
        # Исключения (допустимые английские слова)
        exceptions = {"EN", "teceltest@mail.ru", "TECEL", "teceltest", "mail"}
    
        # Убираем исключения из найденных слов
        untranslated_words = english_words - exceptions
    
        # Проверяем, что нет лишних английских слов
        assert not untranslated_words, f"На сайте присутствуют следующие английские слова: {untranslated_words}"
        print("На сайте нет английских слов (кроме исключений).")

    def avatar_check(self):

        # Путь к файлам относительно директории текущего скрипта
        project_dir = Path(__file__).resolve().parent.parent
        audi_image_path = project_dir / 'test' / 'avatar' / 'audi.jpeg'
        flame_image_path = project_dir / 'test' / 'avatar' / 'flame.jpg'

        # Добавляем аву
        self.browser.find_element(By.ID, 'p-set-avatar-1')

        # Выбор файла (audi.jpeg)
        upload_input = self.wait.until(EC.presence_of_element_located((By.XPATH, '//input[@type="file"]')))
        upload_input.send_keys(str(audi_image_path))

        # Подтверждение
        self.wait.until(EC.presence_of_element_located((By.ID, 'p-cropper-ok-1'))).click()

        self.browser.refresh()

        try:
            self.browser.find_element(By.XPATH, '//*[@src="https://passport.tecel.ru/api/avatars/Default/140.jpg"]')
            print("Аватарка не добавилась")
        except NoSuchElementException:
            print("Аватарка добавилась!")

        self.browser.refresh()

        self.browser.implicitly_wait(10)

        # Находим элемент с изображением аватара
        avatar_element1 = self.browser.find_element(By.XPATH, '//img[contains(@src, "/api/avatars/")]')

        # Получаем значение атрибута src
        src_value1 = avatar_element1.get_attribute('src')

        # Извлекаем уникальную часть из src аватарки
        extracted_value1 = src_value1.split('/api/avatars/')[1]

        # Меняем аву
        self.browser.find_element(By.ID, 'p-set-avatar-1')

        # Выбор файла (flame.jpeg)
        upload_input = self.wait.until(EC.presence_of_element_located((By.XPATH, '//input[@type="file"]')))
        upload_input.send_keys(str(flame_image_path))

        # Подтверждение загрузки
        self.wait.until(EC.presence_of_element_located((By.ID, 'p-set-avatar-1')))

        self.wait.until(EC.element_to_be_clickable((By.ID, 'p-cropper-ok-1'))).click()

        self.browser.refresh()

        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! ОТСЮДА ТЕСТ СРАВНЕНИЯ SRC АВАТАРКИ
        # Находим элемент с изображением аватара
        avatar_element2 = self.browser.find_element(By.XPATH, '//img[contains(@src, "/api/avatars/")]')

        # Получаем значение атрибута src
        src_value2 = avatar_element2.get_attribute('src')

        # Извлекаем уникальную часть из src аватарки
        extracted_value2 = src_value2.split('/api/avatars/')[1]
        self.browser.refresh()
# АВАТАРКА НЕ МЕНЯЕТСЯ ПОФИКСИТЬ ЭТО. НЕ ПРОЖИМАЕТСЯ КНОПКА ОК ПРИ СМНЕ АВЫ

        if extracted_value1 != extracted_value2:
            print(f"{' ' * 79}Аватарка изменилась")
        else:
            print(f"{' ' * 79}Аватарка не изменилась")

        # Удаление аватарки
        delete_button = self.wait.until(EC.presence_of_element_located((By.XPATH, '//span[@class="delete"]')))
        delete_button.click()

        ok_button = self.wait.until(EC.element_to_be_clickable((By.CSS, "div[class='modal-confirm'] button:nth-child(3)")))
        ok_button.click()

        self.browser.refresh()

        default_ava = self.browser.find_element(By.XPATH, '//*[@src="https://passport.tecel.ru/api/avatars/Default/140.jpg"]')

        assert default_ava, print(f"{' ' * 79}Аватарка не удалена")
        print(f"{' ' * 79}Аватарка удалена")

    def check_area(self):

        # Изменение никнейма
        nickname = self.browser.find_element(By.ID, 'p-inp-nickname-1')
        nickname.send_keys('1')

        pyautogui.press('tab')

        # Ожидание надписи 'Сохранено'
        if self.browser.find_element(By.XPATH, '//*[@class="notification success show"]'):
            print("Кнопка 'Сохранено' появилась!")
        else:
            print("Кнопка 'Сохранено' не появилась!")

        self.browser.implicitly_wait(10)
        nickname = self.browser.find_element(By.ID, 'p-inp-nickname-1')

        nickname.clear()

    def check_birthday(self):

        # Очистка поля ДР перед проверкой
        try:
            clear_DR = self.browser.find_element(By.XPATH, "//button[@aria-label='Clear value']//*[name()='svg']")
            if clear_DR.is_displayed():  # Проверка, отображается ли крестик удаления ДР на экране
                clear_DR.click()  # Удаляем ДР, если оно есть
        except NoSuchElementException:
            pass  # Ничего не делаем, если элемент не найден

        self.browser.refresh()

        # Добавление ДР из выпадающего списка:
        self.browser.find_element(By.XPATH, '//input[@class="dp__input"]').click()

        # открытие месяцев
        self.browser.find_element(By.XPATH, "(//button[@class='dp__btn dp__month_year_select'])[1]").click()

        # выбор января
        month = WebDriverWait(self.browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//*[@class='dp__overlay_cell dp__overlay_cell_pad'][contains(., 'Янв.')]")))
        self.browser.execute_script("arguments[0].click();", month)

        # открытие списка с годами
        year_list = self.browser.find_element(By.XPATH, "//button[@aria-label='2025-Open years overlay']")
        year_list.click()

        # тот самый
        year = self.browser.find_element(By.XPATH,
                                   "//div[@class='dp__overlay_cell dp__overlay_cell_pad'][normalize-space()='2007']")
        year.click()

        # выбор числа
        day = self.browser.find_element(By.XPATH,
                                  "//div[@class='dp__cell_inner dp__pointer dp--past dp__date_hover'][normalize-space()='1']")
        day.click()

        # Ожидание надписи 'Сохранено'
        try:
            self.browser.find_element(By.XPATH, '//*[@class="notification success show"]')
            print(f"{' ' * 79}Добавление ДР из выпадающего списка: Успешно")
        except NoSuchElementException:
            print(f"{' ' * 79}Добавление ДР из выпадающего списка: Провал")

        self.browser.refresh()

        # Удаление ДР
        clear_DR = self.browser.find_element(By.XPATH, "//button[@aria-label='Clear value']//*[name()='svg']")
        clear_DR.click()

        try:
            self.browser.find_element(By.XPATH, '//*[@class="notification success show"]')
            print(f"{' ' * 79}Удаление ДР: Успешно")
        except NoSuchElementException:
            print(f"{' ' * 79}Удаление ДР: Провалено")

        # Добавление ДР вручную

        self.browser.find_element(By.XPATH, '//input[@class="dp__input"]').click()

        pyautogui.write('01012007')
        pyautogui.press('tab')

        try:
            self.browser.find_element(By.XPATH, '//*[@class="notification success show"]')
            print(f"{' ' * 79}Добавление ДР вручную: Успешно")
            print(f"{' ' * 79}Проверка корректности работы поля: Успешна")
        except NoSuchElementException:
            print(f"{' ' * 79}Добавление ДР вручную: Провалено")
            print(f"{' ' * 79}Проверка корректности работы поля: Провалена")

    def change_password(self):

        self.browser.find_element(By.XPATH, "//a[@id='p-change-pass-link-1']").click()

        self.browser.find_element(By.XPATH, "//input[@id='p-inp-passchange-1']").send_keys('qwe123')
        pyautogui.press('tab')

        self.browser.find_element(By.XPATH, "//input[@id='p-inp-passchange-2']").send_keys('qwerty')
        pyautogui.press('tab')

        self.browser.find_element(By.XPATH, "//input[@id='p-inp-passchange-3']").send_keys('qwerty')

        self.browser.find_element(By.XPATH, "//button[@id='p-btn-passchange-ok-1']").click()

        # Выходим из профиля и идём проверять старый пароль qwe123
        self.browser.find_element(By.XPATH, "//span[@id='p-top-title-1']").click()

        self.browser.find_element(By.XPATH, "//*[contains(text(), 'ыход')]").click()

        login_input = self.browser.find_element(By.ID, "inp-login-1")
        login_input.send_keys('teceltest@mail.ru')

        button_next = self.browser.find_element(By.XPATH, "//button[@id='btn-submit-1']")
        button_next.click()

        password_input = self.browser.find_element(By.ID, "inp-pass-1")
        password_input.send_keys('qwe123')

        button_enter = self.browser.find_element(By.XPATH, "//button[@id='btn-submit-2']")
        button_enter.click()

        wrong_password = self.browser.find_element(By.XPATH, "//span[contains(text(),'Неверный пароль')]")

        if wrong_password:
            print(f"{' ' * 79}Пароль сменился")
        else:
            print(f"{' ' * 79}Пароль не изменился")

        self.browser.get('https://passport.tecel.ru/profile')

        self.browser.refresh()

        login_input = self.browser.find_element(By.ID, "inp-login-1")
        login_input.send_keys('teceltest@mail.ru')

        button_next = self.browser.find_element(By.XPATH, "//button[@id='btn-submit-1']")
        button_next.click()

        password_input = self.browser.find_element(By.ID, "inp-pass-1")
        password_input.send_keys('qwerty')

        button_enter = self.browser.find_element(By.XPATH, "//button[@id='btn-submit-2']")
        button_enter.click()

        # Возвращаем старый пароль
        self.browser.find_element(By.XPATH, "//a[@id='p-change-pass-link-1']").click()

        self.browser.find_element(By.XPATH, "//input[@id='p-inp-passchange-1']").send_keys('qwerty')
        pyautogui.press('tab')

        self.browser.find_element(By.XPATH, "//input[@id='p-inp-passchange-2']").send_keys('qwe123')
        pyautogui.press('tab')

        self.browser.find_element(By.XPATH, "//input[@id='p-inp-passchange-3']").send_keys('qwe123')

        self.browser.find_element(By.XPATH, "//button[@id='p-btn-passchange-ok-1']").click()

        # Ожидание надписи 'Сохранено' при смене пароля
        if self.browser.find_element(By.XPATH, '//*[@class="notification success show"]'):
            print(f"{' ' * 79}Пароль обратно изменён на 'qwe123'!")
        else:
            print(f"{' ' * 79}Ошибка возвращения старого пароля")

    def change_user_data(self):

        # Для работоспособности этой проверки в мониторинге не должно быть установленных систем!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

        nickname = self.browser.find_element(By.XPATH, "//input[@id='p-inp-nickname-1']")
        nickname.clear()

        # Находим элемент с изображением аватара
        avatar_element1 = self.browser.find_element(By.XPATH, '//img[contains(@src, "/api/avatars/")]')

        # Получаем значение атрибута src
        src_value1 = avatar_element1.get_attribute('src')

        # Извлекаем уникальную часть из src аватарки
        extracted_value1 = src_value1.split('/api/avatars/')[1]

        # print("Извлечённое значение 1:", extracted_value1)

        # Можно чекнуть src авы для сравнения с extracted_value2
        # print(extracted_value1)

        # pyautogui.press('backspace', 10, 0.02)

        nickname.send_keys('Testim123')

        pyautogui.press('tab')

        # Меняем аву
        # Путь к файлам относительно директории текущего скрипта
        project_dir = Path(__file__).resolve().parent.parent
        audi_image_path = project_dir / 'test' / 'avatar' / 'audi.jpeg'
        flame_image_path = project_dir / 'test' / 'avatar' / 'flame.jpg'

        # Добавляем аву
        self.browser.find_element(By.ID, 'p-set-avatar-1')

        # Выбор файла (audi.jpeg)
        upload_input = self.wait.until(EC.presence_of_element_located((By.XPATH, '//input[@type="file"]')))
        upload_input.send_keys(str(audi_image_path))

        # Добавляем аву
        self.browser.find_element(By.ID, 'p-set-avatar-1')

        # Выбор файла (audi.jpeg)
        upload_input = self.wait.until(EC.presence_of_element_located((By.XPATH, '//input[@type="file"]')))
        upload_input.send_keys(str(audi_image_path))

        # Подтверждение
        self.wait.until(EC.presence_of_element_located((By.ID, 'p-cropper-ok-1'))).click()

        # Идём в мониторинг чтобы чекнуть изменения никнейма и авы

        self.browser.find_element(By.XPATH, "//*[text() = 'Продукты']").click()

        self.browser.find_element(By.XPATH, "//*[text() = 'Призрак мониторинг']").click()
        # time.sleep(2)

        self.browser.switch_to.window(self.browser.window_handles[-1])

        if self.wait.until(EC.visibility_of_element_located((By.XPATH, "//*[text() = 'Testim123']"))):
            print(f"{' ' * 102}Никнейм сохраняется")
        else:
            print(f"{' ' * 102}Никнейм не сохраняется")

        # time.sleep(1)

        # Находим элемент с изображением аватара
        avatar_element1 = self.browser.find_element(By.XPATH, '//img[contains(@src, "/api/avatars/")]')

        # Получаем значение атрибута src
        src_value2 = avatar_element1.get_attribute('src')

        # Извлекаем уникальную часть из src аватарки
        extracted_value2 = src_value2.split('/api/avatars/')[1]

        # print("Извлечённое значение 1:", extracted_value1)

        # Вторая часть src аватарки
        # print(extracted_value2)

        if extracted_value1 != extracted_value2:
            print(f"{' ' * 102}Аватарка сохраняется")
        else:
            print(f"{' ' * 102}Аватарка не сохраняется")

        # time.sleep(2)

        pyautogui.hotkey('ctrl', 'w')

        # Мы на странице паспорта

    def change_busy_email(self):
        # Нестабильный тест. При автопрогоне пишет что подозрительная активность.
        # Попытка смены мыла на занятое другим пользователем
        self.browser.find_element(By.XPATH, '//a[@id="p-change-mail-link-1"]').click()  # кнопка "изменить" для смены почты

        self.browser.find_element(By.ID, "p-inp-mail_change-1").click()

        pyautogui.press('backspace', 20, 0.05)

        clear = self.browser.find_element(By.ID, "p-inp-mail_change-1")
        clear.send_keys('ngruzdkov@tecel.ru')

        self.browser.find_element(By.XPATH, '//input[@id="p-inp-mail_change-2"]').click()
        pyautogui.hotkey('q', 'w', 'e', '1', '2', '3')

        self.browser.find_element(By.XPATH, '//button[@id="p-btn-ok-mail_change-1"]').click()

        # Ожидание надписи 'Уже используется'
        elements = self.browser.find_elements(By.XPATH, '//span[@class="message text-alert" and contains(text(),"Уже используется")]')

        if elements:
            print("Проверка пройдена, при смене почты написало: Уже используется")
        else:
            print("Проверка провалена")

    def exit_account(self):

        element = self.browser.find_element(By.XPATH, "//span[@id='p-top-title-1']")
        element.click()

        self.browser.find_element(By.XPATH, "//*[@class='drop-menu']").click()

        if self.browser.find_element(By.XPATH, "//p[@class='fs-20 text-center text-white mb-30 title']"):
            print("Выход из профиля работает")
        else:
            print("Выход из профиля не работает")

    def check_demo_mode(self):

        # Открытие профиля
        self.browser.get("https://monitoring.tecel.ru/#!/garage")

        # Уходим в демо режим
        self.browser.find_element(By.XPATH, "//span[@id='btn-demo-1']").click()

        # Открываем, и считаем поездки и стоянки
        self.browser.find_element(By.XPATH,
                            "//div[@class='device device__warning_blue']//span[@class='MSG__DEVICE__TRACKS']").click()
        poezdki = self.browser.find_elements(By.XPATH, '//div[@class="track-new-title MSG__TRACKS__TRACK_TITLE"]')
        stoyanka = self.browser.find_elements(By.XPATH,
                                        "//div[@class='track-new-title MSG__TRACKS__TRACK_TITLE_PARKING']")

        # Тыкаем кнопку "Журнал" и ищем основные команды
        self.browser.find_element(By.XPATH,
                            "//div[@class='device device__warning_blue tec-color__border_red']//span[@class='MSG__DEVICE__JOURNAL']").click()
        rejim_ohrani_on = self.browser.find_elements(By.XPATH, "//*[text() = 'Включен режим охраны']")
        rejim_ohrani_off = self.browser.find_elements(By.XPATH, "//*[text() = 'Выключен режим охраны']")

        # Чекаем работу АЗ
        # Тык в иконку машины
        self.browser.find_element(By.XPATH,
                            "//div[@class='device device__warning_blue tec-color__border_red']//div[@class='device__card device__card_clickable']").click()
        self.browser.find_element(By.XPATH,
                            "//span[@class='control-commands__button-text MSG__CONTROL__BUTTON_AUTOLAUNCH']").click()
        self.browser.find_element(By.XPATH, "//button[contains(text(),'Выполнить')]").click()
        AZ = self.browser.find_element(By.XPATH, "//*[text() = 'Автозапуск вкл.']")
        vremya = self.browser.find_element(By.XPATH, "//*[text() = '1 из 30 мин.']")

        def check_condition(condition, success_message, failure_message):
            if condition:
                print(success_message)
                return True
            else:
                print(failure_message)
                return False

        # Выполнение всех проверок
        poezdki_check = check_condition(
            len(poezdki) + len(stoyanka) > 0,
            success_message='{:>1}'.format('Поездки работают'),
            failure_message='{:>1}'.format('Поездки не работают')
        )

        rejim_ohrani_check = check_condition(
            rejim_ohrani_on or rejim_ohrani_off,
            success_message='{:>98}'.format('Журнал отображается'),
            failure_message='{:>98}'.format('Журнал не отображается')
        )

        az_check = check_condition(
            AZ and vremya,
            success_message='{:>90}'.format('АЗ работает'),
            failure_message='{:>90}'.format('АЗ не работает')
        )

        demo_check = check_condition(
            poezdki_check and rejim_ohrani_check and az_check,
            success_message='Демо режим работает'.rjust(98),  # Смещение на 98 символов вправо
            failure_message='Демо режим не работает'.rjust(98)  # Смещение на 98 символов вправо
        )
