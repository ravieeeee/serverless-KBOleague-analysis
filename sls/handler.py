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
              if (duplication == 20):
                return "latest updated"
              print('중복 data : doosang' + gall_num)
    
    page_num += 1

  response = {
    "statusCode": 200,
    "body": {
      "Function executed successfully!"
    },
  }

  return response

def crawler_zum_news(event, context):
  page_num = 15
  date_num = datetime.datetime.today().strftime('%Y%m%d')
  # date_num = '20181112'

  while True:
    html = urlopen("http://news.zum.com/list?c=05&sc=38&d=" + str(date_num) + "&p=" + str(page_num))
    soup = BeautifulSoup(html, 'html.parser')

    links = []

    a_tags = soup.select('.newest1 > div > .news > li > .txt > .title > a')
    print('page ' + str(page_num))
    for a_tag in a_tags:
      links.append(a_tag['href'][10:])
    if (len(a_tags) == 0):
      return 'end'
    
    for link in links:
      html_news = urlopen("http://news.zum.com/articles/" + link)
      soup_news = BeautifulSoup(html_news, 'html.parser')
      
      title = soup_news.find(id = 'article').find('h2')
      date = soup_news.find(class_ = 'sponsor').find(class_ = 'date')
      content = soup_news.find(class_ = 'article_body')
      
      unwanted_content = content.find('a')
      while unwanted_content is not None:
        unwanted_content.extract()
        unwanted_content = content.find('a')

      news_id = link.find("?")
      
      try:
        dynamodb.put_item(
          TableName = 'kbo-data',
          Item = {
            'id': {
              'S': 'zumnews' + link[:news_id]
            },
            'dsrc': {
              'S': 'zumnews'
            },
            'num': {
              'S': link[:news_id]
            },
            'title': {
              'S': title.get_text()
            },
            'date': {
              'S': date.get_text()
            },
            'content': {
              'S': content.get_text().strip()
            }
          }
        )
        print('zumnews' + link[:news_id] + ' 데이터 저장')
      except Exception as e:
        return e
      
    page_num += 1

    return 'Function executed successfully!'