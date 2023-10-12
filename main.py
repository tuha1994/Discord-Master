import time
import requests
import openpyxl
import asyncio
import random
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from channel import CHANNEL_DISCORD ,CHANNEL_CHAT
from token_discord import TOKEN_DISCORD
from timer import time_start,time_stop
url = CHANNEL_DISCORD
url1 = CHANNEL_CHAT
headers = {
    "Authorization": TOKEN_DISCORD
}
chromium_binary_path = 'C:\\Program Files\\Chromium\\Application\\chrome.exe'
chromium_driver_path = './chromedriver/chromedriver.exe'
service = Service(executable_path=chromium_driver_path)
options = webdriver.ChromeOptions()
options.binary_location = chromium_binary_path
#options.add_argument('--headless')
options.add_argument('--disable-features=AutoUpdate')
options.add_argument('--no-sandbox')
user_data_dir = 'C:\\Users\\tuha\\AppData\\Local\\Chromium\\User Data\\'
options.add_argument(f'--user-data-dir={user_data_dir}')
driver = webdriver.Chrome(service=service, options=options)
driver.get(url1)
async def random_delay():
    delay_time = random.uniform(time_start, time_stop)
    await asyncio.sleep(delay_time)

async def send_message(content):
    await random_delay()
    payload = {
        "content": content
    }
    res = requests.post(url, payload, headers=headers)
    print(f'Tin nhắn đã được gửi: {content}')

async def main():
    wb = openpyxl.load_workbook('./Chat Discord.xlsx')
    sheet = wb.active
    for row in sheet.iter_rows(values_only=True):
        content = row[0]
        await send_message(content)
    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, 'message-username-1161880945872355378')))
    css_selector_message = 'messageListItem-ZZ7v6g'
    css_selector_label = 'message-delete'
    message_element = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '.messageListItem-ZZ7v6g'))
    )
    actions = ActionChains(driver)
    actions.context_click(message_element).perform()
    delete_element = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.ID, 'message-delete'))
    )
    actions = ActionChains(driver)
    actions.click(delete_element).perform()
    driver.switch_to.active_element.send_keys(Keys.RETURN)
    wb.close()
asyncio.run(main())
