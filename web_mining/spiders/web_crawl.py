import json
import Mongo
import scrapy
import unicodedata
import datetime
from scrapy.selector import Selector 
class WebSpider(scrapy.Spider):
    name = "web"
    glob_dic ={}

    custom_settings = {
        'USER_AGENT':'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36',
    }

    def xpath_element(self):
        self.glob_dic["http://batdongsan.com.vn"] = {"area" : "//*[@id='product-detail']/div[3]/span[2]/span[2]/strong/text()", "price":"//*[@id='product-detail']/div[3]/span[2]/span[1]/strong/text()","title":"//*[@id='product-detail']/div[1]/h1/text()"}

    def choose_xpath(self,response):            #chon xpath cho moi web
        self.xpath_element()
        for var in self.glob_dic:
            if var in response.url:
                return self.glob_dic[var]
                             
    def get_page(self, url):
        return scrapy.Request(url, self.parse)

    def start_requests(self):
        yield self.get_page('http://batdongsan.com.vn')
    
    def parse(self, response):
        All_link = Selector(text=response._body).xpath("//*/a/@href").extract() 
        for var in All_link:
            if "http://" in var:
                continue
            else:
                var = "http://batdongsan.com.vn" + var
                yield scrapy.Request(var, self.parseOtherwebs)
    
    def check_web(self,response):
        if "batdongsan.com.vn" not in response.url:
            return  1
        for i in range(0, Mongo.db.Coll.count()):
            if response.url == Mongo.db.Coll.find()[i]["link"]:
                return  1
        for j in range(0, Mongo.db.important.count()):
            if response.url == Mongo.db.important.find()[j]["link"]:
                return  1
                     
    def parseOtherwebs(self, response):
        flag = 0
        s_dict = {}
        if self.check_web(response):
            return
        for var in self.choose_xpath(response):
            criteria = Selector(text=response._body).xpath(self.choose_xpath(response)[var]).extract()
            if criteria == []:
                continue
            #store the transient data
            #store in dict:
            else:
                flag = 1
                s_dict[var] = unicodedata.normalize('NFKD', criteria[0]).encode('ascii','ignore') 
        s_dict["link"] = response.url
        s_dict["time"] = '{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())
        s_dict = json.dumps(s_dict)         #lenh nay de chuyen dict sang json_string
        data = json.loads(s_dict)           #phai chuyen tu kieu json_string sang json_dict moi insert duoc vao data     
        if flag == 0:
            Mongo.unnecessary_info(data)
        else:
            Mongo.necessary_info(data)
        Another_link =  Selector(text=response._body).xpath('//*/a/@href').extract()
        #query tat ca cac link trong cac trang ben trong
        for var in Another_link:
            if "http://" in var:
                continue
            else:
                var = "http://batdongsan.com.vn" + var
                yield scrapy.Request(var, self.parseOtherwebs) 
