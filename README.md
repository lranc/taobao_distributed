## 淘宝爬虫,分布式依赖于scrapy_redis
## 逻辑:
1.获取商品搜索页面的详细商品URL
<br>2.根据详细商品页面的html分析商品组合,并获取详细价格api
<br>3.带上cookie访问api,获取详细价格

## 待改善:
1.cookies池未充足
<br>2.由于淘宝登录需要手机验证码,未实现cookie池的自动生成与维护
<br>3.添加了proxymiddleware,未实践测试对爬取的影响
<br>4.天猫的爬取逻辑与淘宝一致
