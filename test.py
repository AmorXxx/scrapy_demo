from selenium import webdriver

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('headless')
chrome_options.add_argument('no-sandbox')
driver = webdriver.Chrome(chrome_options=chrome_options)
driver.get("http://zhaoyabei.github.io/")
driver.save_screenshot(driver.title+".png")