import argparse
from collections import namedtuple
from jmotto import login
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait as Wait

if __name__ == '__main__':
  Kintai = namedtuple('Kintai', ('value', 'name'))

  parser = argparse.ArgumentParser()
  parser.add_argument('--start',
                      action='store_const', dest='kintai',
                      const=Kintai('start', '出社'))
  parser.add_argument('--end',
                      action='store_const', dest='kintai',
                      const=Kintai('end', '退社'))
  args = parser.parse_args()
  kintai = args.kintai

  if not kintai:
    exit()

  driver = login()

  btn_selector = f'.portal-timecard-{kintai.value} .portal-timecard-btn'
  btn = driver.find_element_by_css_selector(btn_selector)

  if btn.is_displayed():
    btn.click()

    try:
      Wait(driver, 10).until(
        EC.invisibility_of_element_located((By.CSS_SELECTOR, btn_selector))
      )
    except:
      driver.quit()
  else:
    print(f'{kintai.name}時刻は打刻済みです。')

  time_selector = f'.portal-timecard-{kintai.value} .portal-timecard-time'
  time = driver.find_element_by_css_selector(time_selector)

  print(f'{kintai.name}時刻は {time.text} です。')

  driver.quit()
