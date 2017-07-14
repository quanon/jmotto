import argparse
import re
from datetime import datetime as dt, date
from jmotto import login
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait as Wait

header = f'{"日付":>8}{"出社":>8}{"退社":>8}{"就業時間":>6}{"備考":>8}'


class Row(object):
  def __init__(self, date, start, end, note):
    self._date = date
    self._start = start
    self._end = end
    self._note = note

  def __str__(self):
    note = self.note or '  '
    return f'{self.date}{self.start or "":>10}' \
           + f'{self.end or "":>10}{self.hours or "":>10}{note or "":>8}'

  @property
  def date(self):
    return self._date

  @property
  def start(self):
    if self._start == '未入力':
      return None
    else:
      return self._start

  @property
  def end(self):
    if self._end == '未入力':
      return None
    else:
      return self._end

  @property
  def hours(self):
    if self.start and self.end:
      delta = dt.strptime(self.end, '%H:%M') - dt.strptime(self.start, '%H:%M')
      return ':'.join(str.zfill(2) for str in str(delta).split(':')[:2])
    else:
      return None

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

  driver = login()

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

  month_element = driver.find_element_by_css_selector('.jtcard-fld-targetdate')
  month = re.search(r'\d+(?=月)', month_element.text).group()

  print(header)

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

    print(Row(date, start, end, note))

  driver.quit()
