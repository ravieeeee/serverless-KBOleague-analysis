from selenium import webdriver
from bs4 import BeautifulSoup
import os
import json

def hello(event, context):
  driver = webdriver.PhantomJS(os.environ['phantomjs_loc'])
  driver.get("http://gall.dcinside.com/board/lists?id=skwyverns")

  html = driver.page_source
  soup = BeautifulSoup(html, 'html.parser')

  result = []
  gall_nums = soup.select('.gall_num')
  gall_tits = []
  for titles in soup.find_all(class_ = 'gall_tit'):
    for child in titles.find('a'):
      if (child.string is not None):
        gall_tits.append(child.string)
  gall_dates = soup.find_all(class_ = 'gall_date')
  
  for idx in range(len(gall_nums)):
    row = {}
    row['num'] = gall_nums[idx].get_text()
    row['title'] = gall_tits[idx]
    row['date'] = gall_dates[idx]['title']
    result.append(row)
    # print(json.dumps(result, ensure_ascii = False))

  # driver.find_element_by_class_name('bottom_paging_box').find_element_by_tag_name('a').click()

  body = {
    "message": "Go Serverless v1.0! Your function executed successfully!",
    "input": event
  }

  response = {
    "statusCode": 200,
    "body": json.dumps(body),
    "data": result,
  }

  return response