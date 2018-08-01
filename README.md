# taobao_distributed

## 淘宝分布式爬虫,分布式依赖于scrapy_redis

## 逻辑:
1.获取商品搜索页面的详细商品URL
2.根据详细商品页面的html分析商品组合,并获取详细价格api
3.带上cookie访问api,获取详细价格

## 待改善:
1.cookies池未充足
2.由于淘宝登录需要手机验证码,未实现cookie池的自动生成与维护
3.仅添加proxy的中间件,完成了proxypool,但未实践使用
4.天猫的爬取逻辑与淘宝一致
