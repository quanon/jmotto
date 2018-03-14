from datetime import datetime as dt, date
from jmotto import login
from prettytable import PrettyTable
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait as Wait
import argparse
import re


class Row(object):
  def __init__(self, date, start, end, note):
    self._date = date
    self._start = start
    self._end = end
    self._note = note

  @property
  def date(self):
    return self._date

  @property
  def start(self):
    if self._start == '未入力':
      return ''
    else:
      return self._start

  @property
  def end(self):
    if self._end == '未入力':
      return ''
    else:
      return self._end

  @property
  def hours(self):
    if self.start and self.end:
      delta = dt.strptime(self.end, '%H:%M') - dt.strptime(self.start, '%H:%M')
      return ':'.join(str.zfill(2) for str in str(delta).split(':')[:2])
    else:
      return ''

  @property
  def note(self):
    if self._note == '承認済み':
      return '修正'
    else:
      return self._note


if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('--yyyymm', action='store', type=str)
  args = parser.parse_args()
  yyyymm = args.yyyymm or dt.now().strftime('%Y%m')

  driver, display = login()

  url = 'https://gws45.j-motto.co.jp/cgi-bin/JM0213271/ztcard.cgi'
  url = f'{url}?cmd=tcardindex#date={yyyymm}01'

  driver.get(url)

  try:
    Wait(driver, 10).until(
      EC.text_to_be_present_in_element(
        (By.CSS_SELECTOR, '.jtcard-fld-targetdate'),
        dt.strptime(yyyymm, '%Y%m').strftime('%Y年%m月'))
    )
  except:
    driver.quit()
    display.stop()

  month_element = driver.find_element_by_css_selector('.jtcard-fld-targetdate')
  month = re.search(r'\d+(?=月)', month_element.text).group()

  table = PrettyTable(['日付', '出社', '退社', '就業時間', '備考'])

  for tr in driver.find_elements_by_css_selector('table.tcard-month tr'):
    td_list = tr.find_elements_by_css_selector('td')

    if len(td_list) == 0:
      continue

    date, start, end, note = [td_list[i].text.strip() for i in (0, 1, 4, 5)]
    date = date.replace('(', ' (')
    date = f'{month}/{date}'
    match = re.search(r'(?<=\[).+(?=\])', note)
    if match:
      note = match.group()

    row = Row(date, start, end, note)
    table.add_row([row.date, row.start, row.end, row.hours, row.note])

  print(table)

  driver.quit()
  display.stop()
