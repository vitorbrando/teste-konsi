import time
from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv
import os

load_dotenv()

def get_auth_token(usuario, senha):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(chrome_options=options)
    URL_TOKEN_LOGIN = os.getenv('URL_TOKEN_LOGIN')
    driver.get("{}{}".format("http://", URL_TOKEN_LOGIN))

    username = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'user')))
    password = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'pass')))

    username.send_keys(usuario)
    password.send_keys(senha)

    total_requests = len(driver.requests)
    botao = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'botao')))
    botao.click()

    while (len(driver.requests) <= total_requests):
        time.sleep(1)

    URL_EXTRATO = os.getenv('URL_EXTRATO')
    token = None
    for r in driver.requests:
        if r.method == 'POST' and r.host == URL_EXTRATO:
            if (r.response):
                token = r.response.headers['Authorization']
            break

    return token