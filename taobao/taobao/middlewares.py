# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html
import random
import logging
import redis 
from scrapy import signals
import json

class CookiesMiddleware():
    def __init__(self, REDIS_HOST,REDIS_PORT,REDIS_PASSWORD,REDIS_KEY):
        self.logger = logging.getLogger(__name__)
        self.REDIS_HOST = REDIS_HOST
        self.REDIS_PORT = REDIS_PORT
        self.REDIS_PASSWORD = REDIS_PASSWORD
        self.REDIS_KEY = REDIS_KEY
        self.db = redis.StrictRedis(host=REDIS_HOST,port=REDIS_PORT,password=REDIS_PASSWORD,decode_responses=True)
    
    #def connect_redis(self):
    #    db = redis.StrictRedis(host=REDIS_HOST,port=REDIS_PORT,password=REDIS_PASSWORD,decode_responses=True)

    def get_random_cookies(self): 
        username = random.choice(self.db.hkeys(self.REDIS_KEY))
        value = self.db.hget(self.REDIS_KEY,username)
        return username,value

    def process_request(self, request, spider):
        self.logger.debug('正在获取Cookies')
        username,cookies = self.get_random_cookies()
        if cookies:
            #print((cookies))
            request.cookies = eval(cookies)
            self.logger.debug('使用Cookies ' + username)
    
    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        return cls(
            REDIS_HOST=settings.get('REDIS_HOST'),
            REDIS_PORT=settings.get('REDIS_PORT'),
            REDIS_PASSWORD=settings.get('REDIS_PASSWORD'),
            REDIS_KEY=settings.get('REDIS_KEY'),
        )


