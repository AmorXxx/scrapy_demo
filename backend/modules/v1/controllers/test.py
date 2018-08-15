#!/usr/bin/env python3
# coding=utf-8

def requests_package_inquiry(num):  # 通过模拟requests查询的方法
    from MySQLCommand import MySQLCommand
    import json
    import requests

    urlparse = 'http://www.kuaidi100.com/autonumber/autoComNum?resultv2=1&text={}'
    page = requests.get(urlparse.format(num))
    mysqlCommand = MySQLCommand()
    mysqlCommand.connectMysql()
    # 这里每次查询数据库中最后一条数据的id，新加的数据每成功插入一条id+1
    dataCount = int(mysqlCommand.getLastId()) + 1
    jsonb = json.loads(page.text)
    if len(jsonb.get('auto')) < 1:
        print('单号不存在，查询失败！')
    else:
        shunfeng = jsonb.get('auto')[0]
        if shunfeng.get('comCode') == 'shunfeng':
            print('暂不支持顺丰单号查询。')
        else:
            jsonb = json.loads(page.text)

            for item in jsonb.get('auto'):
                com = item.get('comCode')
                url = 'https://www.kuaidi100.com/query?type={}&postid={}'.format(com, num)
                response = requests.get(url)
                if response.status_code != 200:
                    print('查询失败!')
                else:
                    mes = json.loads(response.text)

                    if mes.get('message') == 'ok':
                        mes.get('data')
                        '''
                        一个包裹占用一行
                        list_time = []
                        for i in range(len(mes.get('data'))):
                            list_time.append(mes.get('data')[i]['time'])
                            list_context = []
                        for i in range(len(mes.get('data'))):
                            list_context.append(mes.get('data')[i]['context'])
                            news_dict = dict(id=str(dataCount), package_id=str(num), time=str(list_time),
                                             context=str(list_context))
                            try:
                                # 插入数据，如果已经存在就进行更新
                                res = mysqlCommand.insertData(news_dict)
                                if res:
                                    dataCount = res
                            except Exception as e:
                                print("插入数据失败", str(e))  # 输出插入失败的报错语句
                        '''
                        # 一条信息占用一行
                        for i in range(len(mes.get('data'))):
                            time = mes.get('data')[i]['time']
                            context = mes.get('data')[i]['context']
                            news_dict = dict(id=str(dataCount), package_id=str(num), time=str(time),
                                             context=str(context))
                            try:
                                # 插入数据，如果已经存在就进行更新
                                res = mysqlCommand.insertData(news_dict)
                                if res:
                                    dataCount = res
                            except Exception as e:
                                print("插入数据失败", str(e))  # 输出插入失败的报错语句
    mysqlCommand.closeMysql()
    dataCount = 0


def selenium_package_inquiry(num):  # 通过selenium查询的方法
    from selenium import webdriver
    from MySQLCommand import MySQLCommand
    import time

    browser = webdriver.Chrome()
    browser.get('http://www.kuaidi100.com/')
    mysqlCommand = MySQLCommand()
    mysqlCommand.connectMysql()
    # 这里每次查询数据库中最后一条数据的id，新加的数据每成功插入一条id+1
    dataCount = int(mysqlCommand.getLastId()) + 1
    search_box = browser.find_element_by_name('postid')  # 物流单号输入框
    search_box.send_keys(num)
    search_btn = browser.find_element_by_id('query')  # 物流查询按钮
    search_btn.click()
    time.sleep(4)
    try:
        browser.find_elements_by_class_name('query-code')
        lastest_time_day = \
            browser.find_elements_by_xpath('//*[@id="queryResult"]/div[3]/div[3]/table/tbody/tr[1]/td[1]/span[1]')[
                0].text  # time中的日期
        lastest_time_time = \
            browser.find_elements_by_xpath('//*[@id="queryResult"]/div[3]/div[3]/table/tbody/tr[1]/td[1]/span[2]')[
                0].text  # time中的时间
        lastest_time = lastest_time_day + " " + lastest_time_time  # 时间日期拼接
        lastest_context = \
            browser.find_elements_by_xpath('//*[@id="queryResult"]/div[3]/div[3]/table/tbody/tr[1]/td[3]')[
                0].text
        lastest_dic = dict(id=str(dataCount), package_id=str(num), time=str(lastest_time),
                           context=str(lastest_context))  # 组建字典
        try:
            # 插入数据，如果已经存在就进行更新
            res = mysqlCommand.insertData(lastest_dic)  # 插入字典
            if res:
                dataCount = res
        except Exception as e:
            print("插入数据失败", str(e))  # 输出插入失败的报错语句
        for i in range(len(browser.find_elements_by_class_name('context'))):
            time_day = browser.find_elements_by_class_name('day')[i].text
            time_time = browser.find_elements_by_class_name('time')[i].text
            time = time_day + " " + time_time  # 时间日期拼接
            context = browser.find_elements_by_class_name('context')[i].text
            news_dic = dict(id=str(dataCount), package_id=str(num), time=str(time), context=str(context))

            try:
                # 插入数据，如果已经存在就进行更新
                res = mysqlCommand.insertData(news_dic)
                if res:
                    dataCount = res
            except Exception as e:
                print("插入数据失败", str(e))  # 输出插入失败的报错语句

    except:
        print('抱歉，暂无查询记录。')
    mysqlCommand.closeMysql()
    dataCount = 0
    browser.quit()
