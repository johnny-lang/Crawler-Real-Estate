import json
import Mongo
from Mongo import *
import scrapy
import unicodedata
import datetime
from scrapy.selector import Selector 
class WebSpider(scrapy.Spider):
    name = "web"
    custom_settings = {
        'USER_AGENT':'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36',
    }

    with open('/home/vickyzhao/webmining/web_mining/spiders/web_xpath.json') as json_data:
        glob_dic = json.load(json_data)
    
    def get_page(self, url):
        return scrapy.Request(url, self.parse)

    def start_requests(self):
        for var in self.glob_dic:
            yield self.get_page(var)

    def choose_xpath(self, response):
        for web in self.glob_dic:
            if web in response.url:
                return self.glob_dic[web]  
    
# de lay ten dung cho cac trang web de crawl
    def home_page(self, response):
        for web in self.glob_dic:
            if web in response.url:
                return web

    def parse(self, response):
        All_links = Selector(text=response._body).xpath("//*/a/@href").extract()
        for link in All_links:
            if "http://" in link:
                continue
            else:
                link = self.home_page(response) + link
            yield scrapy.Request(link, self.parseOther)

    def check_web(self,response):
        flag_check = 0          #check if web need crawling 
        for web in self.glob_dic:
            if web in response.url:
                flag_check = 1
        if flag_check == 0:
            return 1
        # check if link in web have exist
        if Mongo.db.linking_page.find_one({"link":response.url}) != None or Mongo.db.info_page.find_one({"link": response.url}) != None:
            return 1
        #check if this web had been crawl
        #
         #   return 1

    def parseOther(self, response):
        flag_info = 0                               #check if web had infomation
        if self.check_web(response):
            return 
        dic_css = self.choose_xpath(response)       #this dictionary save css for this web
        info_dict = {}
        for criteria in dic_css:
            criteria_css = response.css(dic_css[criteria]).extract()
            if criteria_css == []:
                continue
            else:
                flag_info = 1
                str1 = ""
                for sentence in criteria_css:
                    str1 = str1 + sentence
                info_dict[criteria] = unicodedata.normalize('NFKD', str1).encode('ascii','ignore')
        info_dict["link"] = response.url
        info_dict["time"] = '{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())
        info_dict= json.dumps(info_dict)         #convert dictionary to json_string
        data = json.loads(info_dict)           #must convert json_string to json_dictionary to insert into database
        if flag_info == 0:
            Mongo.unnecessary_info(data)
        else:
            Mongo.necessary_info(data)
        Another_links =  Selector(text=response._body).xpath('//*/a/@href').extract()
        #query all links in this web
        for link in Another_links:
            if "http://" in link:
                pass
            else:
                link = self.home_page(response) + link 
            yield scrapy.Request(link, self.parseOther)
