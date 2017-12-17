from selenium import webdriver
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('headless')
chrome_options.add_argument('no-sandbox')
driver = webdriver.Chrome(chrome_options=chrome_options)
# driver = webdriver.Chrome(executable_path=r'/Users/billyshen/Documents/python_workspace/chromedriver')
# driver.get("https://www.baidu.com/")
# driver.save_screenshot(driver.title+".png")

driver.get("https://www.baidu.com/")
print (driver.title)
# print (1)