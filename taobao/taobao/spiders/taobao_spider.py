# -*- coding: utf-8 -*-
import scrapy
import json
import re
import os
from taobao.items import TaobaoItem,TaobaoDetailItem
from scrapy import Request, Spider



class TaobaoSpiderSpider(Spider):
    name = 'taobao_spider'
    allowed_domains = ['s.taobao.com','detailskip.taobao.com','item.taobao.com']
    index_url = 'https://s.taobao.com/search?q={keyword}&s={num}'
    keyword = ['桌子']
    max_page = 2

    def start_requests(self):
        for key in self.keyword:
            #for i in range(self.max_page):
            for i in range(1):
                yield Request(self.index_url.format(keyword=key,num=i*44), callback=self.first_parse)


    def first_parse(self, response):
        self.logger.debug(response)
        #print(response.text)
        print('解析商品基本数据')
        #data = re.search(r"g_page_config = (.*?)}};", response.text).group(1)+r'}}'
        # 解析商品索引页的信息
        try:
            data = re.search(r"g_page_config = (.*?)}};", response.text).group(1)+r'}}'
        except Exception as e:
            print(e)
            print(response.text)
            os._exit(0)
        itemlist = json.loads(data)['mods']['itemlist']['data']['auctions']
        #print(itemlist)
        for i in itemlist:
            # 判断是否为淘宝商品
            if i['shopcard']['isTmall'] == False:
                print('it is taobao')
                item = TaobaoItem()
                item['goods_id'] = i['nid']
                item['goods_type'] = 'taobao'
                item['goods_title'] = i['raw_title']
                item['goods_pic_url'] = i['pic_url']
                item['goods_sales'] = i['view_sales']
                item['goods_price'] = i['view_price']
                item['goods_shop'] = i['nick']
                item['goods_addr'] = i['item_loc']
                if re.search(r'https',i['detail_url']):
                    item['goods_d_url'] = i['detail_url']
                else:
                    item['goods_d_url'] = 'https:'+i['detail_url']
                yield item
                
                url = item['goods_d_url']
                goods_id = item['goods_id']
                goods_d_names = item['goods_title']

                yield Request(url=url,callback=self.d_parse, meta={'goods_id':goods_id,'goods_d_names':goods_d_names,'refer_url':url})
            else:
                print('it is tmall')

    def d_parse(self,response):
        # 解析商品详细数据
        print('解析商品详细数据')
        goods_id = response.meta.get('goods_id')
        goods_d_names =response.meta.get('goods_d_names')
        refer_url = response.meta.get('refer_url')
        response_text = response.text

        skumap = '{' + re.search(r'skuMap.*?{(.*?)}}',response_text).group(1) + '}}'
        skumap = json.loads(skumap)
        for i in skumap:
            item=TaobaoDetailItem()
            item['goods_d_id'] = i
            item['goods_id'] = goods_id
            item['goods_d_skuid']=skumap[i]['skuId']
            item['goods_d_names']=goods_d_names

            data_value = i[1:-1]
            if re.search(r';',data_value):
                value = data_value.split(';')
                item['goods_d_title'] = ','.join([re.search(r'data-value="%s".*?span>(.*?)</span'% x ,response_text, re.S).group(1) for x in value])
            else:
                item['goods_d_title'] = re.search(r'data-value="%s".*?span>(.*?)</span'% data_value ,response_text, re.S).group(1)
            yield item
        d_price_url = 'https:'+re.search(r'g_config.*?sibUrl.*?\'(.*?)\',',response_text,re.S).group(1) +'&callback=onSibRequestSuccess'
        goods_d_id = item['goods_d_id']
        yield Request(url=d_price_url,callback=self.get_api_price,meta={'goods_id':goods_id})
        

    def get_api_price(self,response):
        print('解析商品详细价格')
        #print(response.request.headers)
        goods_id = response.meta.get('goods_id')
        try:
            body=json.loads(re.search(r'onSibRequestSuccess\((.*?)\);',response.text,re.S).group(1))
        except Exception as e:
            print(response.text)
            print(e)
            os._exit(0)
        quantity_dict = body['data']['dynStock']['sku']   # 库存dict组
        origin_price_dict = body['data']['originalPrice']
        pro_price_dict = body['data']['promotion']['promoData']  #促销价格dict组
        #print(quantity_dict)
        #print(origin_price_dict)
        #print(pro_price_dict)
        #os._exit(0)
        for i in quantity_dict:
            item = TaobaoDetailItem()
            item['goods_d_id'] = i 
            item['goods_id'] = goods_id
            try:
                item['goods_d_quantity']=quantity_dict[i]['sellableQuantity']
            except KeyError as e:
                item['goods_d_quantity'] = 'null'
                print('该商品型号无库存数据',e)
                
            try:
                item['goods_d_pre_price'] = origin_price_dict[i]['price']
            except KeyError as e:
                item['goods_d_pre_price'] = 'null'
                print('该商品无原价格信息',e)
                
            try:
                item['goods_d_now_price'] = pro_price_dict[i][0]['price']
            except KeyError as e:
                item['goods_d_now_price'] = 'null'
                print('该商品无促销价格',e)
                
            #print(item)
            yield item


