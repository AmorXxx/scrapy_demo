from selenium import webdriver

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('headless')
chrome_options.add_argument('no-sandbox')
driver = webdriver.Chrome(chrome_options=chrome_options)
driver.get("https://www.baidu.com/")
driver.save_screenshot(driver.title+".png")