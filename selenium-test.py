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
import zipfile
import os
import coloredlogs
from time import sleep

# Third party library
from selenium import webdriver

# customs
from setting import proxy_ip_with_pwd

# 代理IP
proxy_ip = "144.34.185.120:42369"

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
show = True
# URL
# url_list = ["https://ip.cn/", "https://www.baidu.com/s?ie=UTF-8&wd=ip", "http://ip-check.info/?lang=en", "https://httpbin.org/ip"]
url = "http://httpbin.org/ip"
# 预计每页产品数目（用于向下浏览，加载DOM）
predict_per_num = 40


# logging
coloredlogs.install(level="DEBUG")
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
logger.info("#" * 50)
logger.info("#{0: ^48}#".format("Welcome to the " + __software__))
logger.info("#{0: ^48}#".format("Version : " + __version__))
logger.info("#{0: ^48}#".format("Author : " + __author__))
logger.info("#" * 50)
logger.info("输入的产品关键字: {0}".format(input_msg))


CUSTOM_CHROME_PROXY_EXTENSIONS_DIR = "proxy"


def get_chrome_proxy_extension(proxy):
    """获取一个Chrome代理扩展,里面配置有指定的代理(带用户名密码认证)
    proxy - 指定的代理,格式: username:password@ip:port
    """
    m = re.compile('([^:]+):([^\@]+)\@([\d\.]+):(\d+)').search(proxy)
    if m:
        # 提取代理的各项参数
        username = m.groups()[0]
        password = m.groups()[1]
        ip = m.groups()[2]
        port = m.groups()[3]
        # 创建一个定制Chrome代理扩展(zip文件)
        if not os.path.exists(CUSTOM_CHROME_PROXY_EXTENSIONS_DIR):
            os.mkdir(CUSTOM_CHROME_PROXY_EXTENSIONS_DIR)
        extension_file_path = os.path.join(CUSTOM_CHROME_PROXY_EXTENSIONS_DIR, '{}.zip'.format(proxy.replace(':', '_')))
        if not os.path.exists(extension_file_path):
            # 扩展文件不存在，创建
            zf = zipfile.ZipFile(extension_file_path, mode='w')
            zf.write(os.path.join(CUSTOM_CHROME_PROXY_EXTENSIONS_DIR, 'manifest.json'), 'manifest.json')
            # 替换模板中的代理参数
            background_content = open(os.path.join(CUSTOM_CHROME_PROXY_EXTENSIONS_DIR, 'background.js')).read()
            background_content = background_content.replace('%proxy_host', ip)
            background_content = background_content.replace('%proxy_port', port)
            background_content = background_content.replace('%username', username)
            background_content = background_content.replace('%password', password)
            zf.writestr('background.js', background_content)
            zf.close()
        return extension_file_path
    else:
        raise Exception('Invalid proxy format. Should be username:password@ip:port')


# 设置
if my_browser == 1:
    opt = webdriver.FirefoxOptions()
    if not show:
        opt.headless = True
    browser = webdriver.Firefox(options=opt)
elif my_browser == 2:
    opt = webdriver.ChromeOptions()
    opt.add_extension(get_chrome_proxy_extension(proxy=proxy_ip_with_pwd))
    # opt.add_argument('--proxy-server=http://{0}'.format(proxy_ip))
    if not show:
        opt.headless = True
    browser = webdriver.Chrome(options=opt)
else:
    raise Exception("浏览器选择错误")

browser.implicitly_wait(20)
window = browser.window_handles  # 获取当前页句柄

# 搜索
if globals().get("url_list"):
    for url in url_list:
        browser.get(url)
        sleep(2)
else:
    browser.get(url)


