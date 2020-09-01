### butian_urls

20200619爬取的补天公益src厂商列表（厂商名、域名或者ip）

过程中遇到的主要问题就是发现补天好像对爬虫出新策略了？访问频率过快的话，server端会回复一段混淆处理过的JS代码让client端执行并返回执行结果。
 原理大概就是client如果是浏览器的话自然就解析了JS并发送验证信息，但一般代码处理server回包无法自动解释执行JS，这样就区分了浏览器和爬虫代码。

 网上能找到相应的解决办法：https://blog.csdn.net/qq_36783371/article/details/90760914
 当然，，，，也能

 time.sleep(xxx)..........

 排除超时和异常的项，结果集总共爬到4919项，如下:

![数据样例](/root/PyProjects/enterspider/数据样例.png)
