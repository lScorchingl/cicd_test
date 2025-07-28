import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os

@pytest.fixture()
def browser():
    options = Options()

    # В CI (GitHub Actions) включаем headless режим
    if os.getenv("CI") == "true":
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

    browser = webdriver.Chrome(options=options)
    browser.maximize_window()
    browser.implicitly_wait(3)
    yield browser
    browser.quit()
