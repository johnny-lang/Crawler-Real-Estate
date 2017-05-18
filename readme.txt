basic guide:
    *install Mongodb "https://docs.mongodb.com/manual/tutorial/install-mongodb-on-ubuntu/"
    *syntax: "mongo" in terminal to start
             "use DATABASE_name" to create your database
                Ex : "Webdb" is database
             "db.createCollection(name)" to create your collection. 
                Ex : "linking_page" and "info_page" are collections of Webdb
             "db.Collection_name.count() to count object in your collection
             "db.Collection_name.find() to show your collection    

    *install scrapy "https://doc.scrapy.org/en/latest/intro/install.html"
        note:
            + you must install python 2.7
            + syntax: "scrapy crawl web -o web.json to crawl web" to crawl web
            + cant change the name of function "parse" in quotes_spider.py
            

