## 验证列表url是否正常，正常工作的网站域名放到up_target.txt

import requests

headers = {
    'Host': 'xxxx',
    'User-Agent': 'Mozilla/5.0 ; rv:60.0) Gecko/20100101 Firefox/60.0  ',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate',
    'Upgrade-Insecure-Requests': '1',
    'Cache-Control': 'max-age=0'
}

with open('urls_0619.txt', 'r') as f:
    for target in f.readlines():
        target = target.strip()
        headers['Host'] = target
        url = 'http://' + target
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
