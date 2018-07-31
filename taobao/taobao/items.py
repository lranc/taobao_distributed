# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TaobaoItem(scrapy.Item):
    collection = 'taobao_goods'
    goods_id = scrapy.Field()      #商品id
    goods_type = scrapy.Field()    #商品类型
    goods_title = scrapy.Field()   #商品名称
    goods_pic_url = scrapy.Field() #商品图片链接
    goods_d_url = scrapy.Field()     #商品链接
    goods_sales = scrapy.Field()   #付款人数
    goods_price = scrapy.Field()   #首页价格
    goods_shop = scrapy.Field()    #商家
    goods_addr = scrapy.Field()    #商家地区
    #shop_url 
    
class TaobaoDetailItem(scrapy.Item):
    collection = 'taobao_detail_goods'
    goods_d_id = scrapy.Field()
    goods_id = scrapy.Field()      #商品id
    goods_d_skuid =scrapy.Field()   #商品详细型号id
    goods_d_title = scrapy.Field()#商品详细型号标题
    goods_d_names = scrapy.Field() #商品详细name

    goods_d_pre_price = scrapy.Field() #商品详细原格
    goods_d_now_price = scrapy.Field() #商品详细现价
    goods_d_quantity = scrapy.Field() #商品库存
