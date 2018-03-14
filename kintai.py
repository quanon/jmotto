import argparse
from collections import namedtuple
from datetime import datetime as dt
from jmotto import login
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait as Wait

Kintai = namedtuple('Kintai', ('value', 'name'))

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('--shusha',
                      action='store_const', dest='kintai',
                      const=Kintai('start', '出社'))
  parser.add_argument('--taisha',
                      action='store_const', dest='kintai',
                      const=Kintai('end', '退社'))
  args = parser.parse_args()
  kintai = args.kintai

  if not kintai:
    exit()

  driver, display = login()

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
      display.stop()
  else:
    print(f'※ {kintai.name}時刻は打刻済みです。')

  start_time_selector = f'.portal-timecard-start .portal-timecard-time'
  start_time = driver.find_element_by_css_selector(start_time_selector).text
  if start_time == '---':
    start_time = None

  end_time_selector = '.portal-timecard-end .portal-timecard-time'
  end_time = driver.find_element_by_css_selector(end_time_selector).text
  if end_time == '---':
    end_time = None

  if start_time:
    print(f'出社時刻は {start_time} です。')

  if not start_time and end_time:
    print(f'※ 出社時刻を打刻し忘れています。')
    print(f'退社時刻は {end_time} です。')

  if start_time and end_time:
    delta = dt.strptime(end_time, '%H:%M') - dt.strptime(start_time, '%H:%M')
    hours = ':'.join(str.zfill(2) for str in str(delta).split(':')[:2])

    print(f'退社時刻は {end_time} です。')
    print(f'就業時間は {hours} です。')

  driver.quit()
  display.stop()
