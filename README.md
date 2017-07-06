# j-motto

## Preparations

1. Install Python 3.6.0+ and [ChromeDriver](https://sites.google.com/a/chromium.org/chromedriver/downloads).
1. `pip install -r requirements.txt`
1. `cp config.json{.example,}` and fill out config.json.

## How to use

* Click shusha button: `python kintai.py --start`
* Click taisha button: `python kintai.py --end`
* Show timecard of the current month: `python timecard.py`
* Show timecard of the past month: `python timecard.py --yyyymm 201701`
