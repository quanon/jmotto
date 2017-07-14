import json
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait as Wait


def login():
  driver = webdriver.Chrome()
  _open_login_window(driver)
  _submit_login_form(driver)

  return driver


def _open_login_window(driver):
  driver.get('https://www.j-motto.co.jp/')
  driver.find_element_by_id('loginAction').click()

  try:
    Wait(driver, 5).until(lambda d: len(d.window_handles) > 1)
  except:
    driver.quit()

  driver.switch_to.window(driver.window_handles[1])

  try:
    Wait(driver, 10).until(
      EC.visibility_of_element_located((By.ID, 'memberID'))
    )
  except:
    driver.quit()


def _submit_login_form(driver):
  config = _load_config()

  driver.find_element_by_id('memberID').send_keys(config['member_id'])
  driver.find_element_by_id('userID').send_keys(config['user_id'])
  driver.find_element_by_id('password').send_keys(config['password'])
  driver.find_element_by_name('NAME_DUMMY04').click()

  try:
    Wait(driver, 10).until(
      EC.presence_of_element_located((By.CSS_SELECTOR, '.portal-timecard'))
    )
  except:
    driver.quit()


def _load_config():
  config_path = os.path.join(os.path.dirname(__file__), 'config.json')
  with open(config_path) as json_data:
    config = json.load(json_data)

  return config
