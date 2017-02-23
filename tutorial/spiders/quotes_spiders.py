import json
import Mongo
import scrapy
import unicodedata
from scrapy.selector import Selector 
class QuotesSpider(scrapy.Spider):
    name = "quotes"
    dic ={}

    def add_xpath(self):
        self.dic ["http://batdongsan.com.vn"] = {"url":"//*[@id='ctl40_BodyContainer']/div[1]/div[*]/div/div[2]/div/h3/a/@href", "area" : "//*[@id='product-detail']/div[3]/span[2]/span[2]/strong/text()", "price":"//*[@id='product-detail']/div[3]/span[2]/span[1]/strong/text()", "title" : "//title/text()"}
        return     

    def choose_xpath(self,response):            #chon xpath cho moi web
        self.add_xpath()
        for var in self.dic:
            if var in response.url:
                return self.dic[var]
                             
    def get_page(self, url):
        return scrapy.Request(url, self.parse)

    def start_requests(self):
        yield self.get_page('http://batdongsan.com.vn')
    
    def parse(self, response):
        title = Selector(text=response._body).xpath(self.choose_xpath(response)["url"]).extract() #lay xpath cho link moi 
        new_url = []
        for element in title : 
            new_url.append(element)
            new_url[len(new_url) - 1] = 'http://batdongsan.com.vn'+ new_url[len(new_url) - 1]
            yield scrapy.Request(new_url[len(new_url) - 1], self.parse_childweb)
        Mongo.check()
                 
    def parse_childweb(self, response):
        s_dict = {}
        for i in range(0, Mongo.db.Coll.count()):
            if response.url == Mongo.db.Coll.find()[i]["link"]:
                print"tautologic"           #in ra xem co bi lap hay khong
                return
        for var in self.choose_xpath(response):
            criteria = Selector(text=response._body).xpath(self.choose_xpath(response)[var]).extract()
            if (criteria == []):
                continue
            #store the transient data
            #store in dict:
            else:
                s_dict[var] = unicodedata.normalize('NFKD', criteria[0]).encode('ascii','ignore') 
        s_dict["link"] = response.url
        s_dict = json.dumps(s_dict)         #lenh nay de chuyen dict sang json_string
        data = json.loads(s_dict)           #phai chuyen tu kieu json_string sang json_dict moi insert duoc vao data     
        Mongo.insert(data)
        Another_link =  Selector(text=response._body).xpath('//*[@id="lstProductSimilar"]/div[*]/div[1]/h3/a/@href').extract()
        #query trong cac trang ben trong
        for var in Another_link:
            var = "http://batdongsan.com.vn" + var
            #print "Thang", var
            yield scrapy.Request(var, self.parse_childweb)
        
         
#//*[@id="lstProductSimilar"]/div[2]/div[1]/h3/a
#//*[@id="lstProductSimilar"]/div[8]/div[1]/h3/a
#//*[@id="lstProductSimilar"]/div[9]/div[1]/h3/a
#//*[@id="lstProductSimilar"]/div[2]/div[1]/h3/a
