# from selenium import webdriver
# service_args = ['--proxy=localhost:9150', '--proxy-type=socks5', ]
# driver = webdriver.PhantomJS(executable_path=r'C:\Users\hosxh\Documents\phantomjs-2.1.1-windows\bin\phantomjs.exe',service_args=service_args)
# driver.get("http://icanhazip.com")
# print(driver.page_source)
# driver.close()



import socks
import socket
from urllib.request import urlopen
import threading

def hit():
    # print("Test")
    urlopen('http://www.realestate.co.nz/2994175').read()
    # print(urlopen('http://www.realestate.co.nz/2994175').read())
# http://icanhazip.com'

socks.set_default_proxy(socks.SOCKS5, "localhost", 9150)
socket.socket = socks.socksocket

# threads = []
# count = 1
# while count <= 4:
#     threads.append(threading.Thread(target=hit, args=()))
#     count = count + 1

# t1 = threading.Thread(target=hit,args=())
# threads.append(t1)t1)
# t2 = threading.Thread(target=hit,args=())
# threads.append(t2)

if __name__ == '__main__':
    # print(1)
    count = 1

    while count <= 10000:
        sub_count = 1
        threads = []
        while sub_count <= 16:
            threads.append(threading.Thread(target=hit, args=()))
            sub_count = sub_count + 1
        for t in threads:
            print(count)
            t.setDaemon(True)
            t.start()
        t.join()
        count = count + 1