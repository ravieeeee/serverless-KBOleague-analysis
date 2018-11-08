from urllib.request import urlopen
from bs4 import BeautifulSoup
import os
import json
import datetime

def hello(event, context):
  result = []
  page_num = 1
  loop_flag = True

  while loop_flag:
    html = urlopen("http://gall.dcinside.com/board/lists?id=skwyverns&page=" + str(page_num))
    soup = BeautifulSoup(html, 'html.parser')

    gall_nums = soup.select('.gall_num')
    gall_tits = []
    for titles in soup.find_all(class_ = 'gall_tit'):
      for child in titles.find('a'):
        if (child.string is not None):
          gall_tits.append(child.string)
    gall_dates = soup.find_all(class_ = 'gall_date')
    
    # page = soup.select('.bottom_paging_box > em', limit=1)[0].get_text()
    for idx in range(len(gall_nums)):
      row = {}
      gall_num = gall_nums[idx].get_text()
      if (gall_num != '공지'):
        row['num'] = gall_num
        row['title'] = gall_tits[idx]
        date = gall_dates[idx]['title']
        if (datetime.datetime(int(date[0:4]), int(date[5:7]), int(date[8:10]), int(date[11:13]), int(date[14:16]), int(date[17:19])) 
          < datetime.datetime(2018, 11, 2, 23, 23, 59)):
          loop_flag = False
        row['date'] = date
        if (loop_flag):
          result.append(row)
    
    print(json.dumps(result, ensure_ascii = False))
    page_num += 1

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