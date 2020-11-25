# coding=utf-8
# 1.导入主域名列表
# 2.调用oneforall查子域名，子域名数量大于60过滤
# 3.过滤cdn
# 扫端口
# 找出http，将http端口和子域名放在一起。
# 4.过滤waf
# 5.漏洞探测
import time
import os
import json
import requests
import socket
import nmap
import time
import urllib3
import yaml
from functools import reduce

from colorama import Fore, init

init(convert=True)
urllib3.disable_warnings()
no_waf_url_txt = open("no_waf_url.txt", "w+")
current_path = "xxxxxxx"  # 设置当前程序目录
# 创建当前日志目录
current_time = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
log_path = current_path + "log/" + current_time
os.mkdir(log_path)
max_subdomain = 10000  # 设置最大子域名
top_domain_file = current_path + "1112.txt"  # 设置主域名文件路径
nmapscanallport = False  # 设置是否扫描全端口


def ip_into_int(ip):
    # 先把 192.168.1.13 变成16进制的 c0.a8.01.0d ，再去了“.”后转成10进制的 3232235789 即可。
    # (((((192 * 256) + 168) * 256) + 1) * 256) + 13
    return reduce(lambda x, y: (x << 8) + y, map(int, ip.split('.')))


def is_intranet_ip(ip):
    ip = ip_into_int(ip)
    net_a = ip_into_int('10.255.255.255') >> 24
    net_b = ip_into_int('172.31.255.255') >> 20
    net_c = ip_into_int('192.168.255.255') >> 16
    return ip >> 24 == net_a or ip >> 20 == net_b or ip >> 16 == net_c


# xray
def startxray():
    startxray_cmd = "start xray/xray_windows_amd64.exe webscan --listen 127.0.0.1:7070 --html-output={}/xraylog.html".format(
        log_path)
    os.system(startxray_cmd)
    time.sleep(5)


# 爬网站
def crawlerurl(url):
    # print(url+" 开始爬虫啦")
    # yamlPath="rad_config.yml"
    # url_list=[url]
    # with open(yamlPath,'r',encoding='utf-8') as f:
    #     # print(f.read())
    #     result = f.read()
    #     x = yaml.load(result,Loader=yaml.FullLoader)
    #     # 修改的值
    #     x['restrictions-on-urls']['allowed-urls'] = url_list
    #     print(x)
    #     with open(yamlPath,'w',encoding='utf-8') as w_f:
    #         # 覆盖原先的配置文件
    #         yaml.dump(x,w_f)
    # crawler_cmd = "{}/crawlergo/rad_windows_amd64.exe -t  {}  -http-proxy 127.0.0.1:7070".format(current_path,url)
    crawler_cmd = "{}/crawlergo/crawlergo.exe -c crawlergo/chrome.exe --fuzz-path -t 5 --push-pool-max 10 -f smart --push-to-proxy   [url]http://127.0.0.1:7070/[/url] {}".format(
        current_path, url)
    os.system(crawler_cmd)
    os.system("taskkill /F /IM  chrome.exe")


# 检查有没有waf
def checkWAF(url):
    print(Fore.YELLOW + url + " 开始检查waf")
    oneforall_cmd = "python {}wafw00f/main.py  {}  ".format(
        current_path, url)
    tmp = os.popen(oneforall_cmd).read()
    if "No WAF " in tmp:
        print(Fore.GREEN + url + "没有waf")
        no_waf_url_txt.writelines(url + "\n")
        no_waf_url_txt.flush()
        crawlerurl(url)
    else:
        print(Fore.RED + url + "存在waf")


def checkHttps(domain):
    http_url = "http://" + domain
    https_url = "https://" + domain
    try:
        rg = requests.get(https_url, verify=False, timeout=8)
        return https_url
    except:
        try:
            rg = requests.get(http_url, verify=False, timeout=8)
            return http_url
        except:
            # print("网站打不开"+domain)
            return 0


def nmapscan(ip_subdomain_dict):
    for ip in ip_subdomain_dict:
        if is_intranet_ip(ip):
            print(Fore.RED + ip + "是内网IP,跳过")
            continue
        print(Fore.YELLOW + ip + "nmap 开始扫描端口")
        nm = nmap.PortScannerYield()
        try:
            for result in nm.scan(ip,
                                  "80,81,280,300,443,591,593,832,888,901,981,1010,1080,1100,1241,1311,1352,1434,1521,1527,1582,1583,1944,2082,2086,2087,2095,2096,2222,2301,2480,3000,3128,3333,4000,4001,4002,4100,4125,4243,4443,4444,4567,4711,4712,4848,4849,4993,5000,5104,5108,5432,5555,5800,5801,5802,5984,5985,5986,6082,6225,6346,6347,6443,6480,6543,6789,7000,7001,7002,7396,7474,7674,7675,7777,7778,8000,8001,8002,8003,8004,8005,8006,8008,8009,8010,8014,8042,8069,8075,8080,8081,8083,8088,8090,8091,8092,8093,8016,8118,8123,8172,8181,8200,8222,8243,8280,8281,8333,8384,8403,8443,8500,8530,8531,8800,8806,8834,8880,8887,8888,8910,8983,8989,8990,8991,9000,9043,9060,9080,9090,9091,9200,9294,9295,9443,9444,9800,9981,9988,9990,9999,10000,10880,11371,12043,12046,12443,15672,16225,16080,18091,18092,20000,20720,24465,28017,28080,30821,43110,61600",
                                  arguments="-Pn --host-timeout 3m"):
                # print(result)
                # print(Fore.YELLOW+ip+" 开放的web端口有：")
                for port_num in result[1]["scan"][ip]["tcp"]:
                    port = result[1]["scan"][ip]["tcp"][port_num]
                    if (port["state"] == "open" and (port["name"] == "http" or port["name"] == "https")):
                        webport = ip + ":" + str(port_num)
                        print(Fore.GREEN + webport)
                        ip_subdomain_dict[ip].append(webport)
            # print(ip_subdomain_dict)


        except:
            print(Fore.RED + ip + "未扫到开放的web端口")
            continue
        finally:
            print(Fore.YELLOW + ip + "端口扫描结束，开始检测网站协议")
            if len(ip_subdomain_dict[ip]) > 100:
                print(Fore.RED + ip + "绑定web系统太多，跳过")
                return
            for domain in ip_subdomain_dict[ip]:
                # pass #检查是否是http
                url = checkHttps(domain)
                if url == 0:
                    print(Fore.RED + domain + "网站打不开")
                else:
                    checkWAF(url)


def oneforallfindsubdomain(top_domain):
    oneforall_cmd = "python {}OneForAll/oneforall.py --target {}   run".format(
        current_path, top_domain)
    os.system(oneforall_cmd)
    oneforalllog = "{}/OneForAll/results/{}_resolve_result.json".format(
        current_path, top_domain)
    ip_subdomain_dict = {}
    with open(oneforalllog, 'r') as load_f:
        load_dicts = json.load(load_f)
        if len(load_dicts) > max_subdomain:  # 获取的子域名数量大于最大数量退出函数
            print(Fore.RED + top_domain + "子域名数量过多，跳过" + str(len(load_dicts)))
            return
        print(Fore.GREEN + top_domain + "共获取子域名" + str(len(load_dicts)) + "个")
        for load_dict in load_dicts:
            subdomain = load_dict["subdomain"]
            try:
                addrs = socket.getaddrinfo(subdomain, None)
                if len(addrs) == 1:
                    ip = addrs[0][4][0]
                    # print(ip, subdomain)
                    if ip not in ip_subdomain_dict:
                        ip_subdomain_dict[ip] = subdomain.split()
                    else:
                        ip_subdomain_dict[ip].append(subdomain)
            except:
                pass
                # ip_list = []
                # for item in addrs:
                #     if item[4][0] not in ip_list:
                #         ip_list.append(item[4][0])
                # print(ip_list)
    # print(ip_subdomain_dict)
    nmapscan(ip_subdomain_dict)
    # for ip in ip_subdomain_dict:
    #     print(ip)


if __name__ == "__main__":
    print(Fore.YELLOW + "自动挖漏洞脚本启动了")
    startxray_cmd = "start python -m http.server -b 0.0.0.0 43782"
    os.system(startxray_cmd)
    startxray()
    for top_domain in open(top_domain_file):
        try:
            top_domain = top_domain.strip()
            oneforallfindsubdomain(top_domain)
        except:
            print(Fore.RED + " 出现未知错误")
            continue
    no_waf_url_txt.close()