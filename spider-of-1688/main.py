#!/usr/bin/env python
# -*- coding: utf-8 -*-
__software__ = 'Spider'
__version__ = '1.0.2'
__author__ = 'Yao'

""" Update massage
    version 1.0.1
        1> 完善logging日志信息，良好的交互
        2> 异常捕获URL，任何异常都会及时生成文件
    version 1.0.2
        1> 自动x掉主页活动的JS动画
        2> 增加预估每页产品数量predict_per_num
"""

# Standard library
import logging
import re
import coloredlogs
from time import sleep


# Third party library
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# 搜索内容
input_msg = 'mini UV lamp'
# 等待时间倍数增长,default = 1（网络不好可以增大这个数字）
wait_time = 0.5
# 每个文件大约放多少个产品信息
max_num = 200
# 结果文件名称前缀
filename_prefix = "_".join(input_msg.split())
# 从第几页开始（防止中间意外中断）
start_page = 2
# 第几页结束
end_page = 3
# 选择浏览器(1: 火狐， 2：谷歌)
my_browser = 2
# 显示浏览器页面与否(True or False)
show = False
# URL
url = 'https://www.alibaba.com/'
# 预计每页产品数目（用于向下浏览，加载DOM）
predict_per_num = 40


# logging
coloredlogs.install(level="INFO")
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
logger.info("#" * 50)
logger.info("#{0: ^48}#".format("Welcome to the " + __software__))
logger.info("#{0: ^48}#".format("Version : " + __version__))
logger.info("#{0: ^48}#".format("Author : " + __author__))
logger.info("#" * 50)
logger.info("输入的产品关键字: {0}".format(input_msg))


# 存储
chart = pd.DataFrame(columns=["product title", "price", "keyword"])

# 设置
if my_browser == 1:
    opt = webdriver.FirefoxOptions()
    if not show:
        opt.headless = True
    browser = webdriver.Firefox(options=opt)
elif my_browser == 2:
    opt = webdriver.ChromeOptions()
    if not show:
        opt.headless = True
    browser = webdriver.Chrome(options=opt)
else:
    raise Exception("浏览器选择错误")

browser.implicitly_wait(20)
window = browser.window_handles  # 获取当前页句柄

# 搜索
browser.get(url)

# 关闭主页活动JS插画
browser.find_element_by_class_name("double-close").click()

browser.find_element_by_name("SearchText").click()
browser.find_element_by_name("SearchText").send_keys(input_msg)
browser.find_element_by_class_name("ui-searchbar-submit").submit()
sleep(2 * wait_time)
browser.get(browser.current_url + "&page={0}".format(start_page))


# 提取信息
keyword_patten = re.compile('productKeywords.+?productKeywords.+?value\":\"(.+?)\"')


# 页面滑动
def slip():
    x = 0
    for i in range(int(predict_per_num/2)):
        x = x + (i + 1) * 100
        sleep(0.5)
        js = 'window.scrollTo(0,{0})'.format(x)
        browser.execute_script(js)


# 结果存储
def save(logger, name, chart):
    filename = filename_prefix + "_" + str(name) + ".csv"
    import os
    i = 1
    while os.path.exists(filename):
        filename = str(i) + filename
        i += 1
    logger.info("===存储为文件:{0}".format(filename))
    chart.to_csv(filename, sep=",")


num = 0
name = 0
try:
    while start_page <= end_page:
        if num > max_num:
            name += 1
            save(logger, name, chart)
            chart = pd.DataFrame(columns=["product title", "price", "keyword"])
        slip()
        products = browser.find_elements_by_class_name('J-img-switcher-item')
        next_element = browser.find_element_by_class_name('pages-next')
        logger.info("第{0}页共发现{1}个产品(预计每页{2}个产品)".format(start_page, len(products), predict_per_num))
        for product in products:
            num += 1
            product.click()
            window = browser.window_handles  # 获取当前页句柄
            browser.switch_to.window(window[-1])  # 跳转到新页面
            sleep(2 * wait_time)  # 每个网页等待时间，增加DOM树的加载
            x = WebDriverWait(browser, 10, 1).until(
                EC.presence_of_element_located((By.CLASS_NAME, "ma-title"))
            )
            title = x.get_attribute("title")
            print("\r正在爬取第{0}个产品信息...".format(num), end="", flush=True)
            if title == "#SPURETEXT($!productSubject.value)":
                print("\r", end="", flush=True)
                logger.warning("网络延迟，第{0}个产品信息爬取失败，请增大等待时间，URL：{1}".format(num, browser.current_url))
            try:
                spec_price = browser.find_element_by_class_name('ma-ref-price').text
                spec_packs = browser.find_element_by_class_name('ma-min-order').text
                price = ":".join([spec_packs, spec_price])
            except Exception:
                spec_packs = browser.find_elements_by_class_name('ma-quantity-range')
                spec_price = browser.find_elements_by_class_name('ma-spec-price')
                price = ";".join([":".join([spec_packs[i].text, spec_price[i].text]) for i in range(len(spec_packs))])
            html = browser.execute_script("return document.documentElement.outerHTML")
            keyword = re.search(keyword_patten, html).groups()[0]

            new_row = pd.Series(
                {"product title": title, "price": price, "keyword": keyword})
            chart = chart.append(new_row, ignore_index=True)
            browser.close()
            browser.switch_to.window(window[0])  # 跳转到首页

        print("\r", end="", flush=True)
        logger.info("第{0}页爬取完成！".format(start_page))
        next_element.click()  # 点击下一页
        start_page += 1
except Exception as e:
    logger.error(e)
    logger.error(browser.current_url)
finally:
    name += 1
    save(logger, name, chart)
    logger.info("Congratulations!!")
