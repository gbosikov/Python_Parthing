from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from pymongo.errors import DuplicateKeyError
import hashlib
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from pprint import pprint
import time


user = 'admin'
passw = '5moHizn3JvYLTDPY'
client = MongoClient(f"mongodb+srv://{user}:{passw}@cluster0.uxlpm.mongodb.net/vacancy?retryWrites=true&w=majority",
                     server_api=ServerApi('1'))
db = client['Lesson_05']  # создаю базу данных
mails_stats = db.mails_stats  # создаю коллекцию

options = Options()
options.add_argument("start-maximized")

serv = Service('./chromedriver')
driver = webdriver.Chrome(service=serv, options=options)
wait = WebDriverWait(driver, 15)
login = 'study.ai_172@mail.ru'
password = 'NextPassword172#'


driver.get('https://mail.ru/')
button = driver.find_element(By.XPATH, "//button[@class='resplash-btn resplash-btn_primary resplash-btn_mailbox-big svelte-prwih']")
button.click()

elem = wait.until(EC.presence_of_element_located((By.NAME, 'username')))
elem.send_keys(login)
elem.send_keys(Keys.ENTER)

elem = wait.until(EC.presence_of_element_located((By.NAME, 'password')))
elem.send_keys(password)
elem.send_keys(Keys.ENTER)

mail_links = []
last_link = ''
while True:
    elem = driver.find_elements(By.XPATH, "//a[contains(@href,'/inbox/0:')]")
    if last_link == elem[-1].get_attribute('href'):
        break
    for val in elem:
        mail_links.append(val.get_attribute('href'))
    actions = ActionChains(driver)
    last_link = f"{elem[-1].get_attribute('href')}"

unique_links = set(mail_links)
mails = []
for u_link in unique_links:
    mail_info = {}
    driver.get(u_link)
    time.sleep(15)
    sender = driver.find_element(By.XPATH, ".//div[@class='letter__author']").text
    subject = driver.find_element(By.XPATH, ".//h2[@class='thread-subject']").text
    date = driver.find_element(By.XPATH, ".//div[@class='letter__date']").text
    text = driver.find_element(By.XPATH, "//*[contains(@id, '_BODY')]").text
    encoding = u_link.encode()
    mail_info['_id'] = hashlib.md5(encoding).hexdigest()
    mail_info['sender'] = sender
    mail_info['letter_date'] = date
    mail_info['subject'] = subject
    mail_info['mail_text'] = text
    mail_info['_id'] = hashlib.md5(str(mail_info).encode('utf-8')).hexdigest()
    mails.append(mail_info)
    try:
        mails_stats.insert_one(mail_info)
    except DuplicateKeyError:
        print(f"Document  {mail_info['letter_subj']} already exist")


result = list(mails_stats.find({}))
pprint(result)
