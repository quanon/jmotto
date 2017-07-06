import argparse
import re
from datetime import datetime, date
from jmotto import login
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait as Wait

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('--yyyymm', action='store', type=str)
  args = parser.parse_args()
  yyyymm = args.yyyymm or datetime.now().strftime('%Y%m')

  driver = login()

  header = []
  header.append('{:>8}'.format('日付'))
  header.append('{:>8}'.format('出社'))
  header.append('{:>8}'.format('退社'))
  header.append('{:>6}'.format('就業時間'))
  header.append('{:>8}'.format('備考'))

  rows = []
  url = 'https://gws45.j-motto.co.jp/cgi-bin/JM0213271/ztcard.cgi'
  url = f'{url}?cmd=tcardindex#date={yyyymm}01'

  driver.get(url)

  try:
    Wait(driver, 10).until(
      EC.text_to_be_present_in_element((By.CSS_SELECTOR, '.jtcard-fld-targetdate'), datetime.strptime(yyyymm, '%Y%m').strftime('%Y年%m月'))
    )
  except:
    driver.quit()

  month_element = driver.find_element_by_css_selector('.jtcard-fld-targetdate')
  month = re.search(r'\d+(?=月)', month_element.text).group()

  for tr in driver.find_elements_by_css_selector('table.tcard-month tr'):
    td_list = tr.find_elements_by_css_selector('td')

    if len(td_list) == 0:
      continue

    date, start, end, note = [td_list[i].text.strip() for i in (0, 1, 4, 5)]
    date = date.replace('(', ' (')
    hours = ''
    if start and end:
      delta = datetime.strptime(end, '%H:%M') - datetime.strptime(start, '%H:%M')
      hours = ':'.join(str.zfill(2) for str in str(delta).split(':')[:2])
    start = '{:>10}'.format(start)
    end = '{:>10}'.format(end)
    hours = '{:>10}'.format(hours)
    match = re.search(r'(?<=\[).+(?=\])', note)
    if match:
      note = match.group()
      if note == '承認済み':
        note = '修正'
      note = '{:>8}'.format(note)
    else:
      note = '{:>10}'.format(note)
    rows.append([f'{month}/{date}', start, end, hours, note])

  print(''.join(header))
  for row in rows:
    print(''.join(row))

  driver.quit()
