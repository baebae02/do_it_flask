from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import requests
import time 
import macro_config as mc

def all_cookies(url):
  chrome_options = webdriver.ChromeOptions()
  chrome_options.add_argument('--no-sandbox')
  chrome_options.add_argument('--disable-dev-shm-usage')
  chrome_options.add_argument('--disable-gpu')
  chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])

  driver = webdriver.Chrome('chromedriver', options=chrome_options)
  driver.get(url)

  current_url = driver.current_url
  sw = -1
  # while sw:
  #   question = input('/ID와 PW 입력하셨나요?')
  #   if question == 'y':
  #     sw = 0
  #     break
  #   else:
  #    print("y입력하세요!!")

  driver.find_element(By.ID, 'id').send_keys(mc.portal_id)  # ID
  driver.find_element(By.ID, 'pw').send_keys(mc.portal_pw)  # PW
  driver.find_element(By.CLASS_NAME, "btn_login").click()
  all_cookies = driver.get_cookies()
  print("=====================================")
  print(f'all_cookies before login: {all_cookies}')
  driver.switch_to.window(driver.window_handles[-3])
  driver.get_window_position(driver.window_handles[-3])
  driver.find_element(By.LINK_TEXT, "WISE").click()    
  print("\n\n\n\n=====================================")
  print(f"URI 이동 중 . . . . . . . \n 현재 URI : {driver.current_url}")
  driver.switch_to.window(driver.window_handles[-1])
  driver.get_window_position(driver.window_handles[-1])
  print(f"URI 이동 중 . . . . . . . \n 현재 URI : {driver.current_url}")
  time.sleep(2)
  all_cookies = driver.get_cookies()
  print("\n\n\n\n\n\n=====================================")
  print(f'all_cookies after login: {all_cookies}')


  res = {}
  for i in range(len(all_cookies)):
    res[all_cookies[i]['name']] = all_cookies[i]['value']
  
  print("\n\n\n\n=====================================")
  print((key, value) for (key, value) in res)

  text_cookies=f'JSESSIONID={res["JSESSIONID"]};WT_FPCid=23d187ff9090d2d65dc1666330881810:lv=1673238331063:ss=1673238316228;NetFunnel_ID=;'
  credit_url = 'https://wise.uos.ac.kr/uosdoc/ugd.UgdOtcmSheetInq.do'
  body = 'requestList=&strStudId=2020920048&&_COMMAND_=list&&_XML_=XML&_strMenuId=stud00300&'
  header = {
    'Host': 'wise.uos.ac.kr',
    'Connection': 'keep-alive',
    'Content-Length': '0',
    'Accept-Encoding': 'gzip, deflate, br',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Referer': 'https://wise.uos.ac.kr/uosdoc/include/contentXf.jsp?xtmPagego=ugd/UgdOtcmSheetInq.xtm&strMenuId=STUD00300&PgmId=UgdOtcmSheetInq&callProc=UgdOtcmSheetInq&pgmType=undefined&workInfoYn=undefined',
    'Accept-Language': 'en-US,en;q=0.9,ko;q=0.8',
    'req-protocol': 'application/x-www-form-urlencoded',
    'Cookie': text_cookies
  }
  response = requests.post(credit_url, headers=header, data=body)
  print("\n\n\n\n=====================================")
  print("학점 정보 업로드 완료 . . . . . . . . . . . . . . . \n")
  print(response.content)

  cookies_dict = {}
  for cookie in all_cookies:
    cookies_dict[cookie['name']] = cookie['value']

  string = ''
  for key in cookies_dict:
    string += f'{key}={cookies_dict[key]}; '
  print(string)

  with open("all_cookies.txt", 'w') as f:
    f.write(string)

  with open("credit_res.txt", 'w') as f:
    f.write(str(response.content))
  driver.quit()

  return current_url



if __name__ == '__main__':
  url = "https://portal.uos.ac.kr/user/login.face"
  result = all_cookies(url)
  print(f'쿠키 추출이 완료되었습니다. \n 현재 URL: {result}\n\n')