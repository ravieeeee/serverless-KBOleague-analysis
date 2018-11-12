from urllib.request import urlopen
from bs4 import BeautifulSoup
import datetime
import boto3

dynamodb = boto3.client('dynamodb')

def crawler_sk_wyverns_gallery(event, context):
  page_num = 1
  duplication = 0
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
      gall_num = gall_nums[idx].get_text()
      if (gall_num.isdigit()):
        gall_date = gall_dates[idx]['title']
        if (datetime.datetime(int(gall_date[0:4]), int(gall_date[5:7]), int(gall_date[8:10]), int(gall_date[11:13]), int(gall_date[14:16]), int(gall_date[17:19])) 
          < datetime.datetime(2018, 11, 2, 23, 23, 59)):
          print('end point')
          loop_flag = False
        else:
          if (loop_flag):
            response = dynamodb.get_item(
              TableName = 'kbo-data',
              Key = {
                'id': {
                  'S': 'skg' + gall_num
                }
              }
            )
            if ('Item' not in response):
              try:
                dynamodb.put_item(
                  TableName = 'kbo-data',
                  Item = {
                    'id': {
                      'S': 'skg' + gall_num
                    },
                    'dsrc': {
                      'S': 'skgallery'
                    },
                    'num': {
                      'N': gall_num
                    },
                    'title': {
                      'S': gall_tits[idx]
                    },
                    'date': {
                      'S': gall_date
                    }
                  }
                )
                print('skg' + gall_num + ' 데이터 저장')
              except Exception as e:
                return e
            else:
              duplication += 1
              if (duplication == 20):
                return "latest updated"
              print('중복 data : skg' + gall_num)
    
    page_num += 1

  response = {
    "statusCode": 200,
    "body": {
      "Function executed successfully!"
    },
  }

  return response

def crawler_doosan_bears_gallery(event, context):
  page_num = 1
  duplication = 0
  loop_flag = True

  while loop_flag:
    html = urlopen("http://gall.dcinside.com/board/lists?id=doosanbears_new1&page=" + str(page_num))
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
      gall_num = gall_nums[idx].get_text()
      if (gall_num.isdigit()):
        gall_date = gall_dates[idx]['title']
        if (datetime.datetime(int(gall_date[0:4]), int(gall_date[5:7]), int(gall_date[8:10]), int(gall_date[11:13]), int(gall_date[14:16]), int(gall_date[17:19])) 
          < datetime.datetime(2018, 11, 2, 23, 23, 59)):
          print('end point')
          loop_flag = False
        else:
          if (loop_flag):
            response = dynamodb.get_item(
              TableName = 'kbo-data',
              Key = {
                'id': {
                  'S': 'doosang' + gall_num
                }
              }
            )
            if ('Item' not in response):
              try:
                dynamodb.put_item(
                  TableName = 'kbo-data',
                  Item = {
                    'id': {
                      'S': 'doosang' + gall_num
                    },
                    'dsrc': {
                      'S': 'doosangallery'
                    },
                    'num': {
                      'N': gall_num
                    },
                    'title': {
                      'S': gall_tits[idx]
                    },
                    'date': {
                      'S': gall_date
                    }
                  }
                )
                print('doosang' + gall_num + ' 데이터 저장')
              except Exception as e:
                return e
            else:
              duplication += 1
              # if (duplication == 20):
                # return "latest updated"
              print('중복 data : doosang' + gall_num)
    
    page_num += 1

  response = {
    "statusCode": 200,
    "body": {
      "Function executed successfully!"
    },
  }

  return response