# 验证列表url是否正常，正常工作的网站域名放到up_target.txt
# TODO: Fix HTTPConnectionPool(host='https', port=80): Max retries exceeded

import requests

headers = {
    'User-Agent': 'Mozilla/5.0 ; rv:60.0) Gecko/20100101 Firefox/60.0  ',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate',
    'Upgrade-Insecure-Requests': '1',
    'Connection': 'Close',
    'Cache-Control': 'max-age=0'
}
def domain_hunt():
    pass

def http_formatter(target):  # add http or https for awvs scan
    if target.startswith("http"):
        return target
    # elif target.startswith("www"):  # the www site is http or https
    else:
        try:
            https_url = 'https://' + target
            requests.get(https_url, verify=False, timeout=8)
            return https_url
        except:
            try:
                http_url = 'http://' + target
                requests.get(http_url, verify=False, timeout=8)
                return http_url
            except:
                # print("网站打不开"+domain)
                return 0
    # else:        # domain website is not clear
    #     return 0  # TODO: hunt domain website

with open('urls_0619.txt', 'r') as f:
    for target in f.readlines():
        target = target.strip()
        if target.startswith("http") or target.startswith("www"):
        headers['Host'] = target
        try:
            if requests.get(url, headers=headers, timeout=5).ok:
                with open('up_target.txt', 'a') as t:
                    t.write(target + '\n')
            else:
                print(target + ' is online, But it\'s not ok(status_code>400)')
        except Exception as e:
            print(e)
t.close()
f.close()
print('All done')
