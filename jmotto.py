from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait as Wait
import json
import os


def login():
  display = Display(visible=0, size=(800, 600))
  display.start()
  driver = webdriver.Chrome()
  _open_login_window(driver, display)
  _submit_login_form(driver, display)

  return (driver, display)


def _open_login_window(driver, display):
  driver.get('https://www.j-motto.co.jp/')
  driver.find_element_by_id('loginAction').click()

  try:
    Wait(driver, 5).until(lambda d: len(d.window_handles) > 1)
  except:
    driver.quit()
    display.stop()

  driver.switch_to.window(driver.window_handles[1])

  try:
    Wait(driver, 10).until(
      EC.visibility_of_element_located((By.ID, 'memberID'))
    )
  except:
    driver.quit()
    display.stop()


def _submit_login_form(driver, display):
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
    display.stop()


def _load_config():
  config_path = os.path.join(os.path.dirname(__file__), 'config.json')
  with open(config_path) as json_data:
    config = json.load(json_data)

  return config
