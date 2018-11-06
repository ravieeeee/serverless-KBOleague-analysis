from selenium import webdriver
from bs4 import BeautifulSoup
import os

driver = webdriver.PhantomJS(os.environ['phantomjs_loc'])
driver.get("http://gall.dcinside.com/board/lists?id=skwyverns")

html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

def get_info_of_skwyverns_gall():
  gall_nums = soup.select('.gall_num')
  gall_tits = []
  for titles in soup.find_all(class_ = 'gall_tit'):
    for child in titles.find('a'):
      if (child.string is not None):
        gall_tits.append(child.string)
  gall_dates = soup.find_all(class_ = 'gall_date')
  
  for idx in range(len(gall_nums)):
    print('num:' + gall_nums[idx].get_text())
    print('title:' + gall_tits[idx])
    print('date:' + gall_dates[idx]['title'])
    print()
  
  # driver.find_element_by_class_name('bottom_paging_box').find_element_by_tag_name('a').click()
  get_info_of_skwyverns_gall()



if __name__ == '__main__':
  get_info_of_skwyverns_gall()
  driver.close()
  